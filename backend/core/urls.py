from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    RefreshView,
    BootstrapAdminView,
    MeView,
    PlayersView,
    ModesView,
    GenerateView,
    NextFixtureView,
    PredictionCreateView,
    PredictionLatestView,
    PredictionCheckView,
    HonorsView,
    TimelineView,
    InfoLinksView,
    ChatView,
)


urlpatterns = [
    path("auth/register", RegisterView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/refresh", RefreshView.as_view()),
    path("auth/bootstrap", BootstrapAdminView.as_view()),
    path("me", MeView.as_view()),
    path("players", PlayersView.as_view()),
    path("modes", ModesView.as_view()),
    path("generate", GenerateView.as_view()),
    path("fixtures/next", NextFixtureView.as_view()),
    path("predictions", PredictionCreateView.as_view()),
    path("predictions/latest", PredictionLatestView.as_view()),
    path("predictions/<int:pk>/check", PredictionCheckView.as_view()),
    path("info/honors", HonorsView.as_view()),
    path("info/timeline", TimelineView.as_view()),
    path("info/links", InfoLinksView.as_view()),
    path("chat", ChatView.as_view()),
]
