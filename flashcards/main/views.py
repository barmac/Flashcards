import datetime
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils.timezone import now

from .models import Flashcard


class MainView(View):

    def get(self, request):
        return render(request, "main/index.html")


class FlashcardsListView(ListView):
    model = Flashcard
    context_object_name = 'flashcards'


class AddFlashcardView(CreateView):
    model = Flashcard
    fields = ['question', 'answer', 'deck']
    success_url = reverse_lazy('main')


class PlayView(View):

    def get(self, request):
        query = Flashcard.objects.filter(repeat__lte=datetime.datetime.now())
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


