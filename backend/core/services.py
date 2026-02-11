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


def fetch_football_data(path, params=None):
    if not settings.FOOTBALL_DATA_API_KEY:
        return {"error": "Missing API key"}
    url = f"https://api.football-data.org/v4{path}"
    headers = {"X-Auth-Token": settings.FOOTBALL_DATA_API_KEY}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code >= 400:
            return {"error": "Upstream error", "status": response.status_code, "body": response.text}
        return response.json()
    except requests.RequestException:
        return {"error": "Network error"}


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
    data = fetch_football_data("/competitions/PL/teams")
    if data.get("error"):
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale:
            return stale.get("team_id")
        return None
    teams = data.get("teams", [])
    arsenal = next((t for t in teams if t.get("name") == "Arsenal FC"), None)
    if not arsenal:
        return None
    team_id = arsenal.get("id")
    set_cache_value(cache_key, {"team_id": team_id}, settings.CACHE_TTL_MINUTES)
    return team_id


def get_next_match():
    cache_key = "arsenal_next_match"
    cached = get_cached_value(cache_key)
    if cached:
        return {**cached, "stale": False}
    team_id = get_arsenal_team_id()
    if not team_id:
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale:
            return {**stale, "stale": True}
        return {"error": "Could not find Arsenal team id"}
    data = fetch_football_data(f"/teams/{team_id}/matches", params={"status": "SCHEDULED", "limit": 10})
    if data.get("error"):
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale:
            return {**stale, "stale": True}
        return data
    matches = data.get("matches", [])
    if not matches:
        stale = get_cached_value(cache_key, allow_expired=True)
        if stale:
            return {**stale, "stale": True}
        return {"error": "No scheduled matches found"}
    matches_sorted = sorted(matches, key=lambda m: m.get("utcDate") or "")
    match = matches_sorted[0]
    payload = {
        "match_id": str(match.get("id")),
        "utcDate": match.get("utcDate"),
        "competition": match.get("competition", {}).get("name"),
        "homeTeam": match.get("homeTeam", {}).get("name"),
        "awayTeam": match.get("awayTeam", {}).get("name"),
        "status": match.get("status"),
    }
    set_cache_value(cache_key, payload, settings.CACHE_TTL_MINUTES, match_id=str(match.get("id", "")))
    return {**payload, "stale": False}


def get_match_result(match_id):
    cache_key = f"match_result_{match_id}"
    cached = get_cached_value(cache_key)
    if cached:
        return cached
    data = fetch_football_data(f"/matches/{match_id}")
    if data.get("error"):
        return data
    match = data.get("match")
    if not match:
        return {"error": "No match data"}
    set_cache_value(cache_key, match, settings.CACHE_TTL_MINUTES, match_id=str(match_id))
    return match


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
