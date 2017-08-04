from django.forms import ModelForm

from .models import Flashcard, Deck


class FlashcardForm(ModelForm):

    class Meta:
        model = Flashcard
        exclude = ['repeat', 'repeated', 'interval', 'ef', 'type']

    def __init__(self, *args, **kwargs):
        super(FlashcardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class DeckForm(ModelForm):

    class Meta:
        model = Deck
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(DeckForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })