from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(max_length=16)),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Fact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="FixturesCache",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cache_key", models.CharField(db_index=True, max_length=120)),
                ("match_id", models.CharField(blank=True, max_length=60)),
                ("payload", models.JSONField()),
                ("fetched_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Fragment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("category", models.CharField(choices=[("opener", "opener"), ("praise", "praise"), ("tactical", "tactical"), ("nostalgia", "nostalgia"), ("closer", "closer"), ("emoji", "emoji")], max_length=32)),
                ("text", models.TextField()),
                ("weight", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Honor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("count", models.CharField(max_length=40)),
                ("subtitle", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="InfoLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="KeywordResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("keyword", models.CharField(max_length=80, unique=True)),
                ("response", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("position", models.CharField(blank=True, max_length=60)),
                ("image_url", models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="PreGeneratedLine",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("intensity", models.CharField(choices=[("low", "low"), ("medium", "medium"), ("high", "high")], max_length=16)),
                ("player", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.player")),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("favorite_club", models.CharField(choices=[("Arsenal", "Arsenal"), ("Aston Villa", "Aston Villa"), ("AFC Bournemouth", "AFC Bournemouth"), ("Brentford", "Brentford"), ("Brighton & Hove Albion", "Brighton & Hove Albion"), ("Burnley", "Burnley"), ("Chelsea", "Chelsea"), ("Crystal Palace", "Crystal Palace"), ("Everton", "Everton"), ("Fulham", "Fulham"), ("Leeds United", "Leeds United"), ("Liverpool", "Liverpool"), ("Manchester City", "Manchester City"), ("Manchester United", "Manchester United"), ("Newcastle United", "Newcastle United"), ("Nottingham Forest", "Nottingham Forest"), ("Sunderland", "Sunderland"), ("Tottenham Hotspur", "Tottenham Hotspur"), ("West Ham United", "West Ham United"), ("Wolverhampton Wanderers", "Wolverhampton Wanderers")], max_length=64)),
                ("banter_mode", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TimelineItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("period", models.CharField(max_length=80)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="UserStats",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_points", models.IntegerField(default=0)),
                ("streak", models.IntegerField(default=0)),
                ("accuracy", models.FloatField(default=0.0)),
                ("total_predictions", models.IntegerField(default=0)),
                ("correct_predictions", models.IntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="GeneratorHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("output_text", models.TextField()),
                ("mode", models.CharField(max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("player", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.player")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Prediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("match_id", models.CharField(db_index=True, max_length=60)),
                ("opponent", models.CharField(max_length=120)),
                ("arsenal_is_home", models.BooleanField(default=True)),
                ("kickoff", models.DateTimeField()),
                ("predicted_home", models.IntegerField()),
                ("predicted_away", models.IntegerField()),
                ("locked", models.BooleanField(default=False)),
                ("checked_at", models.DateTimeField(blank=True, null=True)),
                ("actual_home", models.IntegerField(blank=True, null=True)),
                ("actual_away", models.IntegerField(blank=True, null=True)),
                ("points", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
