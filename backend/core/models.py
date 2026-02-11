from django.db import models
from django.contrib.auth.models import User


FAVORITE_CLUB_CHOICES = [
    ("Arsenal", "Arsenal"),
    ("Aston Villa", "Aston Villa"),
    ("AFC Bournemouth", "AFC Bournemouth"),
    ("Brentford", "Brentford"),
    ("Brighton & Hove Albion", "Brighton & Hove Albion"),
    ("Burnley", "Burnley"),
    ("Chelsea", "Chelsea"),
    ("Crystal Palace", "Crystal Palace"),
    ("Everton", "Everton"),
    ("Fulham", "Fulham"),
    ("Leeds United", "Leeds United"),
    ("Liverpool", "Liverpool"),
    ("Manchester City", "Manchester City"),
    ("Manchester United", "Manchester United"),
    ("Newcastle United", "Newcastle United"),
    ("Nottingham Forest", "Nottingham Forest"),
    ("Sunderland", "Sunderland"),
    ("Tottenham Hotspur", "Tottenham Hotspur"),
    ("West Ham United", "West Ham United"),
    ("Wolverhampton Wanderers", "Wolverhampton Wanderers"),
]


FRAGMENT_CATEGORIES = [
    ("opener", "opener"),
    ("praise", "praise"),
    ("tactical", "tactical"),
    ("nostalgia", "nostalgia"),
    ("closer", "closer"),
    ("emoji", "emoji"),
]


INTENSITY_CHOICES = [
    ("low", "low"),
    ("medium", "medium"),
    ("high", "high"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_club = models.CharField(max_length=64, choices=FAVORITE_CLUB_CHOICES)
    banter_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Player(models.Model):
    name = models.CharField(max_length=120, unique=True)
    position = models.CharField(max_length=60, blank=True)
    image_url = models.URLField(blank=True)


class Fact(models.Model):
    text = models.TextField(unique=True)


class Fragment(models.Model):
    category = models.CharField(max_length=32, choices=FRAGMENT_CATEGORIES)
    text = models.TextField()
    weight = models.IntegerField(default=1)


class PreGeneratedLine(models.Model):
    text = models.TextField()
    intensity = models.CharField(max_length=16, choices=INTENSITY_CHOICES)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)


class GeneratorHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    output_text = models.TextField()
    mode = models.CharField(max_length=32)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FixturesCache(models.Model):
    cache_key = models.CharField(max_length=120, db_index=True)
    match_id = models.CharField(max_length=60, blank=True)
    payload = models.JSONField()
    fetched_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=60, db_index=True)
    opponent = models.CharField(max_length=120)
    arsenal_is_home = models.BooleanField(default=True)
    kickoff = models.DateTimeField()
    predicted_home = models.IntegerField()
    predicted_away = models.IntegerField()
    locked = models.BooleanField(default=False)
    checked_at = models.DateTimeField(null=True, blank=True)
    actual_home = models.IntegerField(null=True, blank=True)
    actual_away = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)
    total_predictions = models.IntegerField(default=0)
    correct_predictions = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)


class KeywordResponse(models.Model):
    keyword = models.CharField(max_length=80, unique=True)
    response = models.TextField()


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=16)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Honor(models.Model):
    title = models.CharField(max_length=120)
    count = models.CharField(max_length=40)
    subtitle = models.CharField(max_length=120)


class TimelineItem(models.Model):
    title = models.CharField(max_length=120)
    period = models.CharField(max_length=80)
    description = models.TextField()


class InfoLink(models.Model):
    title = models.CharField(max_length=160)
    url = models.URLField()
