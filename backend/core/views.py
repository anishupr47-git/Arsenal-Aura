from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Profile,
    Player,
    Prediction,
    UserStats,
    Honor,
    TimelineItem,
    InfoLink,
    KeywordResponse,
    ChatMessage,
    FAVORITE_CLUB_CHOICES,
)
from .serializers import (
    RegisterSerializer,
    PlayerSerializer,
    PredictionCreateSerializer,
    PredictionSerializer,
    HonorSerializer,
    TimelineSerializer,
    InfoLinkSerializer,
    ChatRequestSerializer,
    GenerateSerializer,
)
from .permissions import IsArsenalAllowed
from .services import generate_output, get_next_match, get_match_result, get_team_badge


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "favorite_club": user.profile.favorite_club,
                    "banter_mode": user.profile.banter_mode,
                },
            },
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
        )
        return response


class BootstrapAdminView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token") or request.query_params.get("token")
        if not settings.ADMIN_BOOTSTRAP_TOKEN or token != settings.ADMIN_BOOTSTRAP_TOKEN:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        email = (settings.ADMIN_BOOTSTRAP_EMAIL or request.data.get("email") or "").lower()
        password = settings.ADMIN_BOOTSTRAP_PASSWORD or request.data.get("password")
        if not email or not password:
            return Response({"detail": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)
        user, _ = User.objects.get_or_create(username=email, defaults={"email": email})
        user.email = email
        user.username = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        Profile.objects.get_or_create(user=user, defaults={"favorite_club": "Arsenal", "banter_mode": False})
        UserStats.objects.get_or_create(user=user)
        return Response({"ok": True})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower()
        password = request.data.get("password") or ""
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={"favorite_club": "Arsenal", "banter_mode": False},
        )
        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "favorite_club": profile.favorite_club,
                    "banter_mode": profile.banter_mode,
                },
            }
        )
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
        )
        return response


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
        if not token:
            return Response({"detail": "Missing refresh token."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(token)
            access = str(refresh.access_token)
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"access": access})


class MeView(APIView):
    def get(self, request):
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={"favorite_club": "Arsenal", "banter_mode": False},
        )
        data = {
            "id": request.user.id,
            "email": request.user.email,
            "favorite_club": profile.favorite_club,
            "banter_mode": profile.banter_mode,
        }
        return Response(data)

    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={"favorite_club": "Arsenal", "banter_mode": False},
        )
        favorite_club = request.data.get("favorite_club")
        if favorite_club:
            valid_clubs = [c[0] for c in FAVORITE_CLUB_CHOICES]
            if favorite_club not in valid_clubs:
                return Response({"detail": "Invalid club."}, status=status.HTTP_400_BAD_REQUEST)
            profile.favorite_club = favorite_club
            profile.banter_mode = favorite_club in ["Tottenham Hotspur", "Chelsea"]
            profile.save()
        data = {
            "id": request.user.id,
            "email": request.user.email,
            "favorite_club": profile.favorite_club,
            "banter_mode": profile.banter_mode,
        }
        return Response(data)


class PlayersView(APIView):
    permission_classes = [IsArsenalAllowed]

    def get(self, request):
        players = Player.objects.order_by("name")
        return Response(PlayerSerializer(players, many=True).data)


class ModesView(APIView):
    permission_classes = [IsArsenalAllowed]

    def get(self, request):
        return Response(
            [
                {"id": "fact", "label": "Random Arsenal Fact"},
                {"id": "praise", "label": "Player Praise"},
                {"id": "nostalgia", "label": "Deep Fan / Nostalgia"},
            ]
        )


class GenerateView(APIView):
    permission_classes = [IsArsenalAllowed]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "generate"

    def get(self, request):
        serializer = GenerateSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mode = serializer.validated_data["mode"]
        intensity = serializer.validated_data["intensity"]
        player = serializer.validated_data.get("player")
        text = generate_output(request.user, mode, player, intensity)
        return Response({"text": text})


class NextFixtureView(APIView):
    permission_classes = [IsArsenalAllowed]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "fixtures"

    def get(self, request):
        data = get_next_match()
        if data.get("error"):
            return Response({"unavailable": True, "detail": data["error"]})
        home_team = data.get("homeTeam")
        away_team = data.get("awayTeam")
        utc_date = data.get("utcDate")
        if not data.get("match_id") or not home_team or not away_team or not utc_date:
            return Response({"unavailable": True, "detail": "Match data incomplete."})

        def is_arsenal(name):
            return name and "Arsenal" in name

        arsenal_is_home = is_arsenal(home_team)
        opponent = away_team if arsenal_is_home else home_team
        if is_arsenal(opponent):
            return Response({"unavailable": True, "detail": "Opponent data unavailable."})
        home_badge = get_team_badge(home_team)
        away_badge = get_team_badge(away_team)
        return Response(
            {
                "match_id": data.get("match_id"),
                "utcDate": utc_date,
                "competition": data.get("competition"),
                "homeTeam": home_team,
                "awayTeam": away_team,
                "homeBadge": home_badge,
                "awayBadge": away_badge,
                "status": data.get("status"),
                "arsenal_is_home": arsenal_is_home,
                "opponent": opponent,
                "stale": data.get("stale", False),
            }
        )


class PredictionCreateView(APIView):
    permission_classes = [IsArsenalAllowed]

    def post(self, request):
        serializer = PredictionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        kickoff = data["kickoff"]
        if kickoff <= timezone.now():
            return Response({"detail": "Kickoff already passed."}, status=status.HTTP_400_BAD_REQUEST)
        predicted_home = max(0, data["predicted_home"])
        predicted_away = max(0, data["predicted_away"])
        prediction = Prediction.objects.filter(user=request.user, match_id=data["match_id"]).first()
        if prediction:
            if prediction.kickoff <= timezone.now() or prediction.locked:
                return Response({"detail": "Prediction is locked."}, status=status.HTTP_400_BAD_REQUEST)
            prediction.predicted_home = predicted_home
            prediction.predicted_away = predicted_away
            prediction.arsenal_is_home = data["arsenal_is_home"]
            prediction.opponent = data["opponent"]
            prediction.kickoff = kickoff
            prediction.save()
            return Response(PredictionSerializer(prediction).data)
        prediction = Prediction.objects.create(
            user=request.user,
            match_id=data["match_id"],
            opponent=data["opponent"],
            arsenal_is_home=data["arsenal_is_home"],
            kickoff=kickoff,
            predicted_home=predicted_home,
            predicted_away=predicted_away,
            locked=False,
        )
        return Response(PredictionSerializer(prediction).data, status=status.HTTP_201_CREATED)


class PredictionLatestView(APIView):
    permission_classes = [IsArsenalAllowed]

    def get(self, request):
        prediction = Prediction.objects.filter(user=request.user).order_by("-created_at").first()
        if not prediction:
            return Response({})
        return Response(PredictionSerializer(prediction).data)


class PredictionCheckView(APIView):
    permission_classes = [IsArsenalAllowed]

    def post(self, request, pk):
        prediction = Prediction.objects.filter(id=pk, user=request.user).first()
        if not prediction:
            return Response({"detail": "Prediction not found."}, status=status.HTTP_404_NOT_FOUND)
        if prediction.kickoff <= timezone.now():
            prediction.locked = True
            prediction.save()
        match = get_match_result(prediction.match_id)
        if match.get("error"):
            return Response({"detail": match["error"]}, status=status.HTTP_502_BAD_GATEWAY)
        if match.get("status") != "FINISHED":
            return Response({"detail": "Match not finished yet."}, status=status.HTTP_400_BAD_REQUEST)
        score = match.get("score", {}).get("fullTime", {})
        home_score = score.get("home")
        away_score = score.get("away")
        if home_score is None or away_score is None:
            return Response({"detail": "Score not available."}, status=status.HTTP_400_BAD_REQUEST)
        prediction.actual_home = home_score
        prediction.actual_away = away_score
        prediction.checked_at = timezone.now()

        arsenal_goals = home_score if prediction.arsenal_is_home else away_score
        opponent_goals = away_score if prediction.arsenal_is_home else home_score
        predicted_arsenal = prediction.predicted_home
        predicted_opponent = prediction.predicted_away

        exact = arsenal_goals == predicted_arsenal and opponent_goals == predicted_opponent
        outcome = (
            (arsenal_goals > opponent_goals and predicted_arsenal > predicted_opponent)
            or (arsenal_goals == opponent_goals and predicted_arsenal == predicted_opponent)
            or (arsenal_goals < opponent_goals and predicted_arsenal < predicted_opponent)
        )
        if exact:
            points = 3
        elif outcome:
            points = 1
        else:
            points = 0
        prediction.points = points
        prediction.save()

        stats = UserStats.objects.get(user=request.user)
        stats.total_predictions += 1
        if points > 0:
            stats.correct_predictions += 1
            stats.streak += 1
        else:
            stats.streak = 0
        stats.total_points += points
        stats.accuracy = round((stats.correct_predictions / stats.total_predictions) * 100, 2)
        stats.save()

        arsenal_won = arsenal_goals > opponent_goals
        arsenal_draw = arsenal_goals == opponent_goals
        if arsenal_won:
            if exact:
                message = "Emirates prophet. You saw it all coming."
            elif outcome:
                message = "Ball knowledge detected. You called the result."
            else:
                message = "Win secured, but the scoreline got away from you."
        elif arsenal_draw:
            if exact:
                message = "You read the stalemate perfectly."
            elif outcome:
                message = "Draw vibes felt. Solid call."
            else:
                message = "The draw came, but your numbers were bold."
        else:
            if exact:
                message = "Unlucky exact call. You sensed the wrong way."
            elif outcome:
                message = "You predicted the pain. Gooner resilience."
            else:
                message = "You jinxed it, gooner. We go again."

        color = "green" if points == 3 else "yellow" if points == 1 else "red"
        return Response(
            {
                "prediction": PredictionSerializer(prediction).data,
                "points": points,
                "message": message,
                "result_color": color,
            }
        )


class HonorsView(APIView):
    permission_classes = [IsArsenalAllowed]

    def get(self, request):
        honors = Honor.objects.all()
        if not honors.exists():
            return Response(
                [
                    {"id": 1, "title": "League Titles", "count": "13x", "subtitle": "Top-flight Champions"},
                    {"id": 2, "title": "FA Cup Trophies", "count": "14x", "subtitle": "Record Winners"},
                    {"id": 3, "title": "The Invincibles", "count": "2003/04", "subtitle": "Unbeaten League Season"},
                ]
            )
        return Response(HonorSerializer(honors, many=True).data)


class TimelineView(APIView):
    permission_classes = [IsArsenalAllowed]

    def get(self, request):
        items = TimelineItem.objects.all()
        if not items.exists():
            return Response(
                [
                    {"id": 1, "title": "Woolwich Origins", "period": "1886", "description": "Founded in Woolwich and built from humble roots."},
                    {"id": 2, "title": "Highbury Era", "period": "1913–2006", "description": "A historic home that shaped the club's identity."},
                    {"id": 3, "title": "Emirates Stadium", "period": "2006–Present", "description": "Modern home with elite ambitions."},
                    {"id": 4, "title": "Wenger Era", "period": "1996–2018", "description": "Style, trophies, and a global football legacy."},
                    {"id": 5, "title": "Arteta Era", "period": "2019–Present", "description": "Control, youth, and a new Arsenal standard."},
                ]
            )
        return Response(TimelineSerializer(items, many=True).data)


class InfoLinksView(APIView):
    permission_classes = [IsArsenalAllowed]

    def get(self, request):
        links = InfoLink.objects.all()
        if not links.exists():
            return Response(
                [
                    {"id": 1, "title": "Arsenal Official Website", "url": "https://www.arsenal.com/"},
                    {"id": 2, "title": "Arsenal on BBC Sport", "url": "https://www.bbc.com/sport/football/teams/arsenal"},
                    {"id": 3, "title": "Arsenal on Sky Sports", "url": "https://www.skysports.com/arsenal"},
                    {"id": 4, "title": "Arsenal Fixtures and Results", "url": "https://www.premierleague.com/clubs/1/Arsenal/fixtures"},
                ]
            )
        return Response(InfoLinkSerializer(links, many=True).data)


class ChatView(APIView):
    permission_classes = [IsArsenalAllowed]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "chat"

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = serializer.validated_data["message"].lower()
        matches = []
        for item in KeywordResponse.objects.all():
            if item.keyword.lower() in message:
                matches.append(item)
        if matches:
            matches_sorted = sorted(matches, key=lambda x: len(x.keyword), reverse=True)
            best = matches_sorted[:2]
            response_text = " ".join([b.response for b in best])
        else:
            response_text = "Arsenal is the best club."
        ChatMessage.objects.create(user=request.user, role="user", text=serializer.validated_data["message"])
        ChatMessage.objects.create(user=request.user, role="bot", text=response_text)
        return Response({"reply": response_text})
