from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import (
    Profile,
    Player,
    Prediction,
    Honor,
    TimelineItem,
    InfoLink,
    UserStats,
    FAVORITE_CLUB_CHOICES,
    INTENSITY_CHOICES,
)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    favorite_club = serializers.ChoiceField(choices=FAVORITE_CLUB_CHOICES)

    def create(self, validated_data):
        email = validated_data["email"].lower()
        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=validated_data["password"])
            Profile.objects.create(
                user=user,
                favorite_club=validated_data["favorite_club"],
                banter_mode=validated_data["favorite_club"] in ["Tottenham Hotspur", "Chelsea"],
            )
            UserStats.objects.create(user=user)
        return user

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["favorite_club", "banter_mode", "created_at"]


class MeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    favorite_club = serializers.CharField()
    banter_mode = serializers.BooleanField()


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "position", "image_url"]


class PredictionCreateSerializer(serializers.Serializer):
    match_id = serializers.CharField()
    opponent = serializers.CharField()
    arsenal_is_home = serializers.BooleanField()
    kickoff = serializers.DateTimeField()
    predicted_home = serializers.IntegerField()
    predicted_away = serializers.IntegerField()


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            "id",
            "match_id",
            "opponent",
            "arsenal_is_home",
            "kickoff",
            "predicted_home",
            "predicted_away",
            "locked",
            "checked_at",
            "actual_home",
            "actual_away",
            "points",
            "created_at",
        ]


class HonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Honor
        fields = ["id", "title", "count", "subtitle"]


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineItem
        fields = ["id", "title", "period", "description"]


class InfoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoLink
        fields = ["id", "title", "url"]


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()


class GenerateSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=[("fact", "fact"), ("praise", "praise"), ("nostalgia", "nostalgia")])
    player = serializers.CharField(required=False, allow_blank=True)
    intensity = serializers.ChoiceField(choices=INTENSITY_CHOICES)
