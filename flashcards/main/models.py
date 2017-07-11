from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Flashcard(models.Model):
    question = models.CharField(max_length=256)
    answer = models.TextField()
    users = models.ManyToManyField(User)


class Deck(models.Model):
    name = models.CharField(max_length=64)
    flashcards = models.ManyToManyField('Flashcard')
    user = models.ForeignKey(User)