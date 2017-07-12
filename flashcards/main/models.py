from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Flashcard(models.Model):
    question = models.CharField(max_length=256)
    answer = models.TextField()
    users = models.ManyToManyField(User)
    deck = models.ForeignKey('Deck')


class Deck(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User)