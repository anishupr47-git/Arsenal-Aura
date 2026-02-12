from django.contrib import admin
from .models import (
    Profile,
    Player,
    Fact,
    Fragment,
    PreGeneratedLine,
    GeneratorHistory,
    FixturesCache,
    Prediction,
    UserStats,
    KeywordResponse,
    ChatMessage,
    Honor,
    TimelineItem,
    InfoLink,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "favorite_club", "banter_mode", "created_at")
    search_fields = ("user__username", "favorite_club")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "position")
    search_fields = ("name",)


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ("text",)
    search_fields = ("text",)


@admin.register(Fragment)
class FragmentAdmin(admin.ModelAdmin):
    list_display = ("category", "text", "weight")
    list_filter = ("category",)
    search_fields = ("text",)


@admin.register(PreGeneratedLine)
class PreGeneratedLineAdmin(admin.ModelAdmin):
    list_display = ("id", "intensity", "player")
    list_filter = ("intensity",)
    search_fields = ("text",)


@admin.register(GeneratorHistory)
class GeneratorHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "mode", "player", "created_at")
    list_filter = ("mode",)
    search_fields = ("output_text", "user__username")


@admin.register(FixturesCache)
class FixturesCacheAdmin(admin.ModelAdmin):
    list_display = ("cache_key", "match_id", "expires_at")
    search_fields = ("cache_key", "match_id")


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "match_id", "opponent", "kickoff", "points")
    list_filter = ("points",)
    search_fields = ("user__username", "opponent", "match_id")


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "total_points", "streak", "accuracy")


@admin.register(KeywordResponse)
class KeywordResponseAdmin(admin.ModelAdmin):
    list_display = ("keyword", "response")
    search_fields = ("keyword",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    search_fields = ("text", "user__username")


@admin.register(Honor)
class HonorAdmin(admin.ModelAdmin):
    list_display = ("title", "count", "subtitle")


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ("title", "period")


@admin.register(InfoLink)
class InfoLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
