import datetime
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from django.utils.timezone import now

from .forms import FlashcardForm, DeckForm, ProfileForm
from .models import Flashcard, Deck, Language


class MainView(View):

    def get(self, request):
        if request.user.is_authenticated:
            username = " ".join([request.user.first_name, request.user.last_name])
            return render(request, "main/index.html", {'username': username})
        else:
            return render(request, "main/index.html")


class FlashcardsView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user = User.objects.get(username=request.user.get_username())
        deck = get_object_or_404(Deck, pk=pk)
        form = FlashcardForm(initial={'deck': deck.pk})

        if deck.user != user:
            return HttpResponseForbidden()

        flashcards = deck.flashcard_set.order_by('repeat')
        username = " ".join([user.first_name, user.last_name])
        paginator = Paginator(flashcards, 15)

        page = request.GET.get('page')
        try :
            flashcards = paginator.page(page)
        except PageNotAnInteger:
            flashcards = paginator.page(1)
        except EmptyPage:
            flashcards = paginator.page(paginator.num_pages)

        ctx = {'flashcards': flashcards, 'form': form, 'username': username, 'deck': deck}
        return render(request, 'main/flashcards.html', ctx)

    def post(self, request, pk):
        form = FlashcardForm(request.POST)

        if form.is_valid():
            flashcard = form.save(commit=False)
            user = request.user
            deck = get_object_or_404(Deck, pk=pk)

            if deck.user != user:
                return HttpResponseForbidden()

            flashcard.deck = deck
            flashcard.save()

        return redirect('flashcards', pk)


class PlayView(LoginRequiredMixin, View):

    def get(self, request, pk):
        deck = get_object_or_404(Deck, pk=pk)
        user = User.objects.get(username=request.user.get_username())

        if deck.user != user:
            return HttpResponseForbidden()

        query = deck.flashcard_set.filter(repeat__lte=datetime.datetime.now())
        username = " ".join([user.first_name, user.last_name])
        ctx = {'username': username}

        if query:
            if user.profile.session_limit and request.session.get('limit', 0) > 0:
                ctx['flashcard'] = query[randint(0, query.count()-1)]
                ctx['count'] = request.session['limit']
            elif not user.profile.session_limit:
                ctx['flashcard'] = query[randint(0, query.count() - 1)]
                ctx['count'] = query.count()

        return render(request, 'main/play.html', ctx)


class NewIntervalView(LoginRequiredMixin, View):
    """
    Implement Supermemo 2 algorithm (based on https://www.supermemo.com/english/ol/sm2.htm).
    """
    def get(self, request, pk, grade):
        user = request.user
        flashcard = get_object_or_404(Flashcard, pk=pk)
        deck = flashcard.deck

        if deck.user != user:
            return HttpResponseForbidden()

        grade = int(grade)
        if grade < 3:
            flashcard.interval = 1
        else:
            if not flashcard.repeated:
                if flashcard.interval == 0:
                    flashcard.interval = 1
                elif flashcard.interval == 1:
                    flashcard.interval = 6
                else:
                    flashcard.interval = flashcard.interval * flashcard.ef
                flashcard.ef = flashcard.ef + (0.1 - (5-grade)*(0.08 + (5-grade)*0.02))
                if flashcard.ef < 1.3:
                    flashcard.ef = 1.3
        flashcard.repeated = True

        if grade >= 4:
            flashcard.repeat = now().date() + datetime.timedelta(days=flashcard.interval)
            flashcard.repeated = False
            if user.profile.session_limit and request.session.get('limit'):
                request.session['limit'] -= 1

        flashcard.save()

        return redirect('play', deck.pk)


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        username = " ".join([request.user.first_name, request.user.last_name])
        count = sum([deck.flashcard_set.count() for deck in Deck.objects.filter(user=request.user)])
        form = ProfileForm(initial=model_to_dict(request.user.profile))
        ctx = {'username': username, 'count': count, 'form': form}
        return render(request, 'main/profile.html', ctx)

    def post(self, request):
        username = " ".join([request.user.first_name, request.user.last_name])
        count = sum([deck.flashcard_set.count() for deck in Deck.objects.filter(user=request.user)])
        form = ProfileForm(request.POST)
        profile = request.user.profile

        if form.is_valid():
            profile.session_limit = form.cleaned_data.get('session_limit', profile.session_limit)
            profile.session_limit_count = form.cleaned_data.get('session_limit_count', profile.session_limit_count)
            profile.save()

        return redirect('profile')



class FlashcardDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user = request.user
        flashcard = get_object_or_404(Flashcard, pk=pk)
        deck = flashcard.deck

        if deck.user != user:
            return HttpResponseForbidden()

        flashcard.delete()
        return redirect('flashcards', deck.pk)


class FlashcardEditView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user = request.user
        flashcard = get_object_or_404(Flashcard, pk=pk)
        deck = flashcard.deck
        decks = user.deck_set.all()

        if deck.user != user:
            return HttpResponseForbidden()

        username = " ".join([user.first_name, user.last_name])
        form = FlashcardForm(initial={'question': flashcard.question, 'answer': flashcard.answer})
        ctx = {'flashcard': flashcard, 'form': form, 'username': username, 'deck': deck, 'decks': decks}

        return render(request, 'main/flashcard_edit.html', ctx)

    def post(self, request, pk):
        user = request.user
        flashcard = Flashcard.objects.get(pk=pk)
        deck = flashcard.deck

        if deck.user != user:
            return HttpResponseForbidden()

        form = FlashcardForm(request.POST)
        new_deck = get_object_or_404(Deck, pk=request.POST.get('deck'))

        if new_deck.user != user:
            return HttpResponseForbidden()

        if form.is_valid():
            flashcard.question = form.cleaned_data['question']
            flashcard.answer = form.cleaned_data['answer']
            flashcard.deck = new_deck
            flashcard.save()

        return redirect('flashcards', deck.pk)


class DeckChoiceView(LoginRequiredMixin, View):

    def get(self, request, current_view):
        user = request.user
        username = " ".join([user.first_name, user.last_name])
        form = DeckForm()
        ctx = {'decks': user.deck_set.all(), 'username': username, 'form': form, 'current_view': current_view}
        if current_view == 'play' and user.profile.session_limit:
            request.session['limit'] = user.profile.session_limit_count
        return render(request, 'main/deck_choice.html', ctx)

    def post(self, request, current_view):
        form = DeckForm(request.POST)
        user = request.user

        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = user
            deck.save()

        return redirect('deck_choice', current_view)