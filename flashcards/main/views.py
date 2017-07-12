from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from main.models import Flashcard, Deck


class MainView(View):

    def get(self, request):
        return render(request, "main/index.html")


class FlashcardsListView(ListView):
    model = Flashcard
    context_object_name = 'flashcards'


class DecksListView(ListView):
    model = Deck
    context_object_name = 'decks'


class AddFlashcardView(CreateView):
    model = Flashcard
    fields = '__all__'
    success_url = reverse_lazy('main')


class AddDeckView(CreateView):
    model = Deck
    fields = '__all__'
    success_url = reverse_lazy('main')


class PlayView(View):

    def get(self, request):
        ctx = {'flashcards': Flashcard.objects.all()}
        return render(request, 'main/play.html', ctx)