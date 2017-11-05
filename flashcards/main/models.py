from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# To use in future
FLASHCARD_TYPES = (
    (1, "Klasyczna fiszka"),
    (2, "Zdanie do uzupełnienia"),
)

# Create your models here.
class Flashcard(models.Model):
    question = models.CharField(max_length=256, verbose_name="Pytanie")
    answer = models.CharField(max_length=256, verbose_name="Odpowiedź")
    repeat = models.DateField(default=now, verbose_name="Dzień powtórki")
    repeated = models.BooleanField(default=False)
    interval = models.IntegerField(default=0, verbose_name="Interwał")
    ef = models.FloatField(default=2.5)
    type = models.IntegerField(choices=FLASHCARD_TYPES, default=1, verbose_name="Typ")
    deck = models.ForeignKey('Deck', verbose_name="Talia")

    def __str__(self):
        return self.question


class Language(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nazwa")
    special_characters = models.CharField(default="", max_length=64, verbose_name="Znaki specjalne")

    def __str__(self):
        return self.name


class Deck(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nazwa")
    desc = models.CharField(default="", blank=True, max_length=256, verbose_name="Opis")
    user = models.ForeignKey(User, verbose_name="Użytkownik")
    language = models.ForeignKey(Language, verbose_name="Język")

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User)
    daily_limit = models.BooleanField(default=False)
    daily_limit_count = models.IntegerField(default=50)
