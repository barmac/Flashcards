from django.forms import ModelForm

from .models import Flashcard


class FlashcardForm(ModelForm):

    class Meta:
        model = Flashcard
        exclude = ['repeat', 'repeated', 'interval', 'ef', 'user', 'type']

    def __init__(self, *args, **kwargs):
        super(FlashcardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
