from django.contrib import admin

# Register your models here.
from .models import Flashcard

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    pass
