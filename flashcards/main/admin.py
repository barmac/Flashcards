from django.contrib import admin

# Register your models here.
from main.models import Flashcard, Deck

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    pass


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    pass