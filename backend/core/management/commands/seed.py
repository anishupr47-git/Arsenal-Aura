import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Player,
    Fact,
    Fragment,
    PreGeneratedLine,
    KeywordResponse,
    Honor,
    TimelineItem,
    InfoLink,
    UserStats,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **options):
        if options["reset"]:
            Player.objects.all().delete()
            Fact.objects.all().delete()
            Fragment.objects.all().delete()
            PreGeneratedLine.objects.all().delete()
            KeywordResponse.objects.all().delete()
            Honor.objects.all().delete()
            TimelineItem.objects.all().delete()
            InfoLink.objects.all().delete()

        for user in User.objects.all():
            UserStats.objects.get_or_create(user=user)

        player_names = [
            "Bukayo Saka",
            "Martin Odegaard",
            "Declan Rice",
            "William Saliba",
            "Gabriel Magalhaes",
            "Ben White",
            "Gabriel Martinelli",
            "Kai Havertz",
            "Leandro Trossard",
            "Jurrien Timber",
            "Thomas Partey",
            "Oleksandr Zinchenko",
            "Aaron Ramsdale",
            "David Raya",
            "Eddie Nketiah",
            "Reiss Nelson",
            "Emile Smith Rowe",
            "Fabio Vieira",
            "Jakub Kiwior",
            "Takehiro Tomiyasu",
            "Jorginho",
            "Mohamed Elneny",
            "Gabriel Jesus",
            "Kieran Tierney",
            "Myles Lewis-Skelly",
            "Ethan Nwaneri",
            "Thierry Henry",
            "Dennis Bergkamp",
            "Patrick Vieira",
            "Robert Pires",
            "Freddie Ljungberg",
            "Sol Campbell",
            "Tony Adams",
            "Ian Wright",
            "Ray Parlour",
            "Gilberto Silva",
            "Ashley Cole",
            "David Seaman",
            "Cesc Fabregas",
            "Robin van Persie",
            "Santi Cazorla",
            "Mesut Ozil",
            "Alexis Sanchez",
            "Jack Wilshere",
            "Theo Walcott",
            "Per Mertesacker",
            "Laurent Koscielny",
            "Gael Clichy",
            "Kolo Toure",
            "Lee Dixon",
            "Paul Merson",
            "Nigel Winterburn",
            "Martin Keown",
            "Nicolas Anelka",
            "Edu Gaspar",
        ]
        for name in player_names:
            Player.objects.get_or_create(name=name)

        fact_prefixes = [
            "Fact:",
            "Did you know?",
            "Arsenal note:",
            "Classic Arsenal:",
            "Gooner fact:",
            "History bite:",
            "Club note:",
            "North London fact:",
            "Red and white fact:",
            "Arsenal identity:",
        ]
        fact_bodies = [
            "Arsenal are based in North London.",
            "Arsenal are nicknamed The Gunners.",
            "Arsenal play home matches at Emirates Stadium.",
            "Arsenal were founded in 1886 in Woolwich.",
            "Arsenal moved to Highbury in the early 1900s.",
            "Arsenal have one of the richest histories in English football.",
            "Arsenal are known for their red and white colors.",
            "The club has a storied rivalry in the North London derby.",
            "Arsenal won the league unbeaten in 2003/04.",
            "The club has lifted the FA Cup on many occasions.",
            "Highbury was Arsenal's home for most of the 20th century.",
            "Arsenal moved to the Emirates Stadium in 2006.",
            "The club is famous for stylish, possession-based play.",
            "Arsenal have fielded many legendary strikers.",
            "Arsenal have produced elite academy talent.",
            "The club crest features a cannon.",
            "Arsenal have won English league titles.",
            "The Invincibles season remains iconic in football history.",
            "Arsenal have featured in European competitions for decades.",
            "Arsenal are a cornerstone of London football culture.",
            "The club has worn red shirts for over a century.",
            "Arsenal have been led by iconic managers.",
            "The club has a global fanbase.",
            "Arsenal's home is in the borough of Islington.",
            "The Arsenal motto is rooted in tradition and pride.",
        ]
        facts = []
        for prefix in fact_prefixes:
            for body in fact_bodies:
                facts.append(f"{prefix} {body}")
        for text in set(facts):
            Fact.objects.get_or_create(text=text)

        openers = [
            "No debate:",
            "Pure class:",
            "Every week:",
            "Straight from the stands:",
            "From the first whistle:",
            "Stadium-level energy:",
            "North London truth:",
            "Gooner eyes see it:",
            "This is the standard:",
            "Locked in:",
            "Aura check:",
            "Cannon-level vibes:",
            "Top flight glow:",
            "Elite heartbeat:",
            "Matchday energy:",
            "Red pulse:",
            "Calm authority:",
            "Football art:",
            "Arsenal rhythm:",
            "Pure control:",
        ]

        praise_adjectives = [
            "silky",
            "electric",
            "calm",
            "sharp",
            "ruthless",
            "precise",
            "clinical",
            "smooth",
            "fearless",
            "composed",
            "elegant",
            "explosive",
            "relentless",
            "clever",
            "creative",
            "clinical",
            "dominant",
            "brave",
            "fast",
            "confident",
            "ice-cold",
            "fluid",
            "measured",
            "balanced",
            "disciplined",
            "brilliant",
            "classy",
            "elite",
            "smart",
            "decisive",
            "inventive",
            "direct",
            "patient",
            "agile",
            "powerful",
            "elevated",
            "refined",
            "focused",
            "steady",
            "unshakeable",
            "authoritative",
            "daring",
            "unstoppable",
            "special",
            "fearless",
            "timeless",
            "gliding",
            "surgical",
            "poised",
            "dominant",
        ]

        praise_nouns = [
            "touch",
            "passing",
            "vision",
            "movement",
            "first step",
            "finish",
            "decision-making",
            "control",
            "dribble",
            "press",
            "tempo",
            "instincts",
            "timing",
            "reading of the game",
            "duel strength",
            "leadership",
            "balance",
            "positioning",
            "composure",
            "engine",
            "work rate",
            "flair",
            "gravity",
            "presence",
            "intelligence",
            "swagger",
            "link-up",
            "shift",
            "pace",
            "drive",
            "calmness",
            "awareness",
            "angle",
            "technique",
            "accuracy",
            "flow",
            "authority",
            "edge",
            "spark",
            "craft",
        ]

        praise_fragments = set()
        for adj in praise_adjectives:
            for noun in praise_nouns:
                praise_fragments.add(f"is {adj} with their {noun}")
                praise_fragments.add(f"brings {adj} {noun} every time")

        tactical_verbs = [
            "sets",
            "controls",
            "dictates",
            "pushes",
            "threads",
            "opens",
            "closes",
            "squeezes",
            "breaks",
            "anchors",
            "leads",
            "drives",
            "organizes",
            "balances",
            "accelerates",
            "slows",
            "transforms",
            "tilts",
            "switches",
            "stitches",
        ]
        tactical_nouns = [
            "the tempo",
            "the press",
            "the build-up",
            "the midfield",
            "the half-space",
            "the counter",
            "the rhythm",
            "the shape",
            "the back line",
            "the transition",
            "the passing lanes",
            "the final third",
            "the wide overload",
            "the triangles",
            "the patterns",
            "the blocks",
            "the triggers",
            "the rest defense",
            "the press resistance",
            "the second ball",
        ]
        tactical_fragments = set()
        for verb in tactical_verbs:
            for noun in tactical_nouns:
                tactical_fragments.add(f"{verb} {noun} with total confidence.")

        nostalgia_fragments = [
            "It feels like Highbury echoing again.",
            "That is classic Arsenal elegance.",
            "Invincibles-level composure in the bloodstream.",
            "Pure Wengerball memories in motion.",
            "North London heritage written in every touch.",
            "A nod to the old Arsenal soul.",
            "You can feel the club history in the way it flows.",
            "Emirates nights with a Highbury heart.",
            "The cannon on the crest is alive.",
            "Gooner nostalgia hits hard with that style.",
            "Legacy stuff. It breathes Arsenal.",
            "You can see the heritage in the movement.",
            "That is a Highbury-era kind of grace.",
            "Pure Arsenal identity from first touch to last.",
            "Invincibles energy without the noise.",
            "That is the Arsenal code.",
            "It is the North London signature.",
            "History and swagger in one.",
            "A throwback to the golden eras.",
            "The tradition is loud in this performance.",
        ]

        closers = [
            "Keep it rolling.",
            "The aura is real.",
            "North London is smiling.",
            "That is Arsenal DNA.",
            "Straight class, no debate.",
            "Elite levels only.",
            "That is the standard.",
            "Keep the cannon firing.",
            "We move.",
            "Gooner joy secured.",
            "Stay locked in.",
            "Sharp and ruthless.",
            "That is pure Arsenal.",
            "The vibe is perfect.",
            "The shirt is heavy with history.",
            "This is why we watch.",
            "Make it a legacy performance.",
            "Emirates crowd approves.",
            "Stay on that level.",
            "Top shelf only.",
        ]

        def ensure_fragment(category, text, weight):
            if not Fragment.objects.filter(category=category, text=text).exists():
                Fragment.objects.create(category=category, text=text, weight=weight)

        for text in openers:
            ensure_fragment("opener", text, 2)
        for text in praise_fragments:
            ensure_fragment("praise", text, 1)
        for text in tactical_fragments:
            ensure_fragment("tactical", text, 1)
        for text in nostalgia_fragments:
            ensure_fragment("nostalgia", text, 2)
        for text in closers:
            ensure_fragment("closer", text, 2)
        Fragment.objects.filter(category="emoji").delete()

        if PreGeneratedLine.objects.count() < 10000:
            openers_list = list(Fragment.objects.filter(category="opener").values_list("text", flat=True))
            praise_list = list(Fragment.objects.filter(category="praise").values_list("text", flat=True))
            tactical_list = list(Fragment.objects.filter(category="tactical").values_list("text", flat=True))
            nostalgia_list = list(Fragment.objects.filter(category="nostalgia").values_list("text", flat=True))
            closers_list = list(Fragment.objects.filter(category="closer").values_list("text", flat=True))
            players = list(Player.objects.all())
            lines = []
            for _ in range(10000):
                intensity = random.choice(["low", "medium", "high"])
                player = random.choice(players) if players else None
                name = player.name if player else "Arsenal"
                opener = random.choice(openers_list)
                praise = random.choice(praise_list)
                tactical = random.choice(tactical_list)
                nostalgia = random.choice(nostalgia_list)
                closer = random.choice(closers_list)
                if intensity == "low":
                    text = f"{opener} {name} {praise}. {closer}"
                elif intensity == "medium":
                    text = f"{opener} {name} {praise}. {tactical} {closer}"
                else:
                    text = f"{opener} {name} {praise}. {tactical} {nostalgia} {closer}"
                lines.append(PreGeneratedLine(text=text, intensity=intensity, player=player))
            PreGeneratedLine.objects.bulk_create(lines, batch_size=500)

        emoji_chars = ["🔴", "⚪", "🔥", "💫", "🎯", "🧠", "⚡", "🛡️", "🚀", "🏟️", "🌟", "👑", "💥", "🧩", "🔝", "🫶", "🏆"]
        for line in PreGeneratedLine.objects.all():
            cleaned = line.text
            for ch in emoji_chars:
                cleaned = cleaned.replace(ch, "")
            cleaned = " ".join(cleaned.split())
            if cleaned != line.text:
                line.text = cleaned
                line.save(update_fields=["text"])

        keywords = {
            "invincibles": "The Invincibles went unbeaten in the 2003/04 league season.",
            "wenger": "Arsene Wenger changed English football with style and belief.",
            "highbury": "Highbury was Arsenal's historic home with pure character.",
            "emirates": "The Emirates Stadium has been Arsenal's home since 2006.",
            "arteta": "Mikel Arteta has restored structure and belief.",
            "saka": "Saka is pure Hale End quality and heart.",
            "odegaard": "Odegaard sets the tempo with class.",
            "saliba": "Saliba is calm, strong, and elite.",
            "rice": "Declan Rice brings control and drive.",
            "henry": "Thierry Henry is Arsenal royalty.",
            "bergkamp": "Bergkamp made football look like art.",
            "fa cup": "Arsenal have a deep love affair with the FA Cup.",
            "premier league": "Arsenal are a historic force in the Premier League.",
            "north london derby": "The North London derby is pure intensity.",
            "cannon": "The cannon crest is Arsenal identity in one symbol.",
            "high press": "Arsenal's press is bold and coordinated.",
            "hale end": "Hale End produces special talent.",
            "wengerball": "Wengerball is beauty in motion.",
            "invincible": "Unbeaten. Immortal. Arsenal.",
            "gooner": "Gooners live for moments like this.",
            "arteta era": "The Arteta era is about control and standards.",
            "emirates nights": "Emirates nights can be electric.",
            "legend": "Arsenal legends built the culture.",
            "classic": "Classic Arsenal style never fades.",
        }

        for player in Player.objects.all():
            keywords[player.name.lower()] = f"{player.name} brings Arsenal quality every time."
            last = player.name.split()[-1].lower()
            if last not in keywords:
                keywords[last] = f"{player.name} is pure class in red and white."

        for key, response in keywords.items():
            KeywordResponse.objects.get_or_create(keyword=key, defaults={"response": response})

        if Honor.objects.count() == 0:
            Honor.objects.bulk_create(
                [
                    Honor(title="League Titles", count="13x", subtitle="Top-flight Champions"),
                    Honor(title="FA Cup Trophies", count="14x", subtitle="Record Winners"),
                    Honor(title="The Invincibles", count="2003/04", subtitle="Unbeaten League Season"),
                ]
            )

        if TimelineItem.objects.count() == 0:
            TimelineItem.objects.bulk_create(
                [
                    TimelineItem(title="Woolwich Origins", period="1886", description="Founded in Woolwich and built from humble roots."),
                    TimelineItem(title="Highbury Era", period="1913–2006", description="A historic home that shaped the club's identity."),
                    TimelineItem(title="Emirates Stadium", period="2006–Present", description="Modern home with elite ambitions."),
                    TimelineItem(title="Wenger Era", period="1996–2018", description="Style, trophies, and a global football legacy."),
                    TimelineItem(title="Arteta Era", period="2019–Present", description="Control, youth, and a new Arsenal standard."),
                ]
            )

        if InfoLink.objects.count() == 0:
            InfoLink.objects.bulk_create(
                [
                    InfoLink(title="Arsenal Official Website", url="https://www.arsenal.com/"),
                    InfoLink(title="Arsenal on BBC Sport", url="https://www.bbc.com/sport/football/teams/arsenal"),
                    InfoLink(title="Arsenal on Sky Sports", url="https://www.skysports.com/arsenal"),
                    InfoLink(title="Arsenal Fixtures and Results", url="https://www.premierleague.com/clubs/1/Arsenal/fixtures"),
                ]
            )

        self.stdout.write(self.style.SUCCESS("Seed complete"))
