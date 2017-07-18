import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.utils.timezone import now

from .forms import FlashcardForm
from .models import Flashcard


class MainView(View):

    def get(self, request):
        return render(request, "main/index.html")


class FlashcardsView(View):

    def get(self, request):
        form = FlashcardForm()
        user = User.objects.get(username=request.user.get_username())
        flashcards = Flashcard.objects.filter(user=user)
        ctx = {'flashcards': flashcards, 'form': form}
        return render(request, 'main/flashcards.html', ctx)

    def post(self, request):
        form = FlashcardForm(request.POST)
        user = User.objects.get(username=request.user.get_username())
        flashcards = Flashcard.objects.filter(user=user)

        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = user
            flashcard.save()

        ctx = {'flashcards': flashcards, 'form': form}
        return render(request, 'main/flashcards.html', ctx)


class PlayView(View):

    def get(self, request):
        query = Flashcard.objects.filter(repeat__lte=datetime.datetime.now()).order_by('repeated')
        if query:
            return render(request, 'main/play.html', {'flashcard': query[0]})
        else:
            return render(request, 'main/play.html')


class NewIntervalView(View):

    """
    Implement Supermemo 2 algorithm (based on https://www.supermemo.com/english/ol/sm2.htm).
    """

    def get(self, request, id, grade):
        flashcard = Flashcard.objects.get(id=id)
        grade = int(grade)
        if grade < 3:
            flashcard.interval = 1
        else:
            if not flashcard.repeated:
                if flashcard.interval == 1:
                    flashcard.interval = 6
                else:
                    flashcard.interval = flashcard.interval * flashcard.ef
                flashcard.ef = flashcard.ef + (0.1 - (5-grade)*(0.08 + (5-grade)*0.02))
        flashcard.repeated = True

        if grade == 5:
            flashcard.repeat = now().date() + datetime.timedelta(days=flashcard.interval)
            flashcard.repeated = False

        flashcard.save()

        return redirect('play')


