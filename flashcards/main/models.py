from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# Create your models here.
class Flashcard(models.Model):
    question = models.CharField(max_length=256, verbose_name="Pytanie")
    answer = models.CharField(max_length=256, verbose_name="Odpowiedź")
    repeat = models.DateField(default=now, verbose_name="Dzień powtórki")
    repeated = models.BooleanField(default=False)
    interval = models.IntegerField(default=1, verbose_name="Interwał")
    ef = models.FloatField(default=2.5)
    user = models.ForeignKey(User, verbose_name="Użytkownik")

    def __str__(self):
        return self.question
