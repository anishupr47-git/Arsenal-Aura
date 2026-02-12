import random
import requests
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from .models import FixturesCache, Player, Fact, Fragment, PreGeneratedLine, GeneratorHistory


EMOJI_CHARS = ["🔴", "⚪", "🔥", "💫", "🎯", "🧠", "⚡", "🛡️", "🚀", "🏟️", "🌟", "👑", "💥", "🧩", "🔝", "🫶", "🏆"]


def clean_text(text):
    cleaned = text
    for ch in EMOJI_CHARS:
        cleaned = cleaned.replace(ch, "")
    return " ".join(cleaned.split())


def get_cached_value(cache_key, allow_expired=False):
    now = timezone.now()
    qs = FixturesCache.objects.filter(cache_key=cache_key)
    if not allow_expired:
        qs = qs.filter(expires_at__gt=now)
    cached = qs.order_by("-expires_at").first()
    if cached:
        return cached.payload
    return None


def set_cache_value(cache_key, payload, ttl_minutes, match_id=""):
    expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
    FixturesCache.objects.create(
        cache_key=cache_key,
        match_id=match_id,
        payload=payload,
        expires_at=expires_at,
    )

def is_complete_match_payload(payload):
    if not payload:
        return False
    required = ["match_id", "utcDate", "homeTeam", "awayTeam"]
    for key in required:
        value = payload.get(key)
        if not value:
            return False
    return True


def fetch_api_football(path, params=None):
    if not settings.API_FOOTBALL_KEY:
        return {"error": "Missing API key"}
    base_url = settings.API_FOOTBALL_BASE_URL.rstrip("/")
    url = f"{base_url}{path}"
    headers = {
        "x-apisports-key": settings.API_FOOTBALL_KEY,
        "User-Agent": "ArsenalAura/1.0 (+https://arsenalaura.vercel.app/)",
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code >= 400:
            return {"error": "Upstream error", "status": response.status_code, "body": response.text}
        data = response.json()
        if data.get("errors"):
            return {"error": "Upstream error", "body": data.get("errors")}
        return data
    except requests.RequestException:
        return {"error": "Network error"}


def map_api_football_status(short_code):
    if not short_code:
        return "SCHEDULED"
    finished = {"FT", "AET", "PEN"}
    scheduled = {"NS", "TBD"}
    postponed = {"PST"}
    in_play = {"1H", "2H", "HT", "ET", "BT", "INT"}
    cancelled = {"CANC", "ABD", "SUSP"}
    if short_code in finished:
        return "FINISHED"
    if short_code in scheduled:
        return "SCHEDULED"
    if short_code in postponed:
        return "POSTPONED"
    if short_code in in_play:
        return "IN_PLAY"
    if short_code in cancelled:
        return "CANCELLED"
    return short_code


def fetch_sportsdb(path, params=None):
    if not settings.SPORTS_DB_API_KEY:
        return None
    url = f"https://www.thesportsdb.com/api/v1/json/{settings.SPORTS_DB_API_KEY}{path}"
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code >= 400:
            return None
        return response.json()
    except requests.RequestException:
        return None


def get_team_badge(team_name):
    if not team_name:
        return None
    normalized = team_name.replace(" FC", "").strip()
    cache_key = f"badge_{normalized.lower()}"
    cached = get_cached_value(cache_key)
    if cached:
        return cached.get("badge")
    data = fetch_sportsdb("/searchteams.php", params={"t": normalized})
    if not data or not data.get("teams"):
        return None
    badge = data["teams"][0].get("strTeamBadge")
    if badge:
        set_cache_value(cache_key, {"badge": badge}, settings.CACHE_TTL_MINUTES, match_id="")
    return badge


def get_arsenal_team_id():
    cache_key = "pl_team_id_arsenal"
    cached = get_cached_value(cache_key)
    if cached:
        return cached.get("team_id")
    if settings.ARSENAL_TEAM_ID:
        try:
            team_id = int(settings.ARSENAL_TEAM_ID)
            set_cache_value(cache_key, {"team_id": team_id}, settings.CACHE_TTL_MINUTES)
            return team_id
        except ValueError:
            pass
    data = fetch_api_football("/teams", params={"search": "Arsenal"})
    if data.get("error"):
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale:
            return stale.get("team_id")
        return None
    teams = data.get("response", [])
    arsenal = None
    for entry in teams:
        team = entry.get("team") or {}
        name = team.get("name") or ""
        if name == "Arsenal" or "Arsenal" in name:
            arsenal = team
            break
    if not arsenal:
        return None
    team_id = arsenal.get("id")
    set_cache_value(cache_key, {"team_id": team_id}, settings.CACHE_TTL_MINUTES)
    return team_id


def get_next_match():
    cache_key = "arsenal_next_match"
    cached = get_cached_value(cache_key)
    if cached and is_complete_match_payload(cached):
        return {**cached, "stale": False}
    team_id = get_arsenal_team_id()
    if not team_id:
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale and is_complete_match_payload(stale):
            return {**stale, "stale": True}
        return {"error": "Could not find Arsenal team id"}
    now = timezone.now()
    season = now.year if now.month >= 7 else now.year - 1
    attempts = [
        {"team": team_id, "next": 10},
        {"team": team_id, "status": "NS"},
        {"team": team_id, "status": "NS", "season": season},
    ]
    data = None
    for params in attempts:
        data = fetch_api_football("/fixtures", params=params)
        if not data.get("error"):
            break
    if data.get("error"):
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale and is_complete_match_payload(stale):
            return {**stale, "stale": True}
        return data
    matches = data.get("response", [])
    if not matches:
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale and is_complete_match_payload(stale):
            return {**stale, "stale": True}
        return {"error": "No scheduled matches found"}
    matches_sorted = sorted(
        matches,
        key=lambda m: (m.get("fixture") or {}).get("date") or "",
    )
    match = None
    for candidate in matches_sorted:
        fixture = candidate.get("fixture") or {}
        teams = candidate.get("teams") or {}
        home = (teams.get("home") or {}).get("name")
        away = (teams.get("away") or {}).get("name")
        if fixture.get("id") and fixture.get("date") and home and away:
            match = candidate
            break
    if not match:
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale and is_complete_match_payload(stale):
            return {**stale, "stale": True}
        return {"error": "Match data incomplete"}
    fixture = match.get("fixture") or {}
    teams = match.get("teams") or {}
    league = match.get("league") or {}
    status = map_api_football_status((fixture.get("status") or {}).get("short"))
    payload = {
        "match_id": str(fixture.get("id")),
        "utcDate": fixture.get("date"),
        "competition": league.get("name"),
        "homeTeam": (teams.get("home") or {}).get("name"),
        "awayTeam": (teams.get("away") or {}).get("name"),
        "status": status,
    }
    if is_complete_match_payload(payload):
        set_cache_value(cache_key, payload, settings.CACHE_TTL_MINUTES, match_id=str(fixture.get("id", "")))
    return {**payload, "stale": False}


def get_match_result(match_id):
    cache_key = f"match_result_{match_id}"
    cached = get_cached_value(cache_key)
    if cached:
        return cached
    data = fetch_api_football("/fixtures", params={"ids": match_id})
    if data.get("error"):
        return data
    response = data.get("response", [])
    if not response:
        return {"error": "No match data"}
    match = response[0]
    fixture = match.get("fixture") or {}
    status_short = (fixture.get("status") or {}).get("short")
    status = map_api_football_status(status_short)
    goals = match.get("goals") or {}
    normalized = {
        "status": status,
        "score": {"fullTime": {"home": goals.get("home"), "away": goals.get("away")}},
    }
    set_cache_value(cache_key, normalized, settings.CACHE_TTL_MINUTES, match_id=str(match_id))
    return normalized


def pick_fragment(category):
    fragments = Fragment.objects.filter(category=category)
    if not fragments.exists():
        return ""
    texts = [f.text for f in fragments]
    weights = [f.weight for f in fragments]
    return random.choices(texts, weights=weights, k=1)[0]


def pick_player(player_name=None):
    if player_name:
        player = Player.objects.filter(name=player_name).first()
        if player:
            return player
    return Player.objects.order_by("?").first()


def assemble_praise(player_name, intensity, force_nostalgia=False):
    player = pick_player(player_name)
    name = player.name if player else "Arsenal"
    opener = pick_fragment("opener")
    praise = pick_fragment("praise")
    tactical = pick_fragment("tactical")
    nostalgia = pick_fragment("nostalgia")
    closer = pick_fragment("closer")
    emoji = pick_fragment("emoji")
    if intensity == "low":
        text = f"{opener} {name} {praise}. {closer}"
    elif intensity == "medium":
        text = f"{opener} {name} {praise}. {tactical} {closer} {emoji}"
    else:
        text = f"{opener} {name} {praise}. {tactical} {nostalgia} {closer} {emoji}"
    if force_nostalgia and nostalgia:
        text = f"{opener} {name} {praise}. {nostalgia} {closer} {emoji}"
    return clean_text(text.strip()), player


def generate_output(user, mode, player_name, intensity):
    recent = list(
        GeneratorHistory.objects.filter(user=user).order_by("-created_at").values_list("output_text", flat=True)[:20]
    )
    recent_set = set(recent)
    attempt = 0
    while attempt < 10:
        attempt += 1
        player = None
        if mode == "fact":
            fact = Fact.objects.order_by("?").first()
            text = fact.text if fact else "Arsenal is the best club."
        elif mode == "nostalgia":
            text, player = assemble_praise(player_name, intensity, force_nostalgia=True)
        else:
            lines = PreGeneratedLine.objects.filter(intensity=intensity)
            if player_name:
                lines = lines.filter(player__name=player_name)
            line = lines.order_by("?").first()
            if line:
                text = line.text
                player = line.player
            else:
                text, player = assemble_praise(player_name, intensity, force_nostalgia=False)
        text = clean_text(text)
        if text not in recent_set:
            GeneratorHistory.objects.create(user=user, output_text=text, mode=mode, player=player)
            return text
    GeneratorHistory.objects.create(user=user, output_text=text, mode=mode, player=player)
    return text
