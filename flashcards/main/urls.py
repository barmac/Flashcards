from django.conf.urls import url, include
from .views import MainView, FlashcardsView, PlayView, NewIntervalView


urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^flashcards/$', FlashcardsView.as_view(), name='flashcards'),
    url(r'^play/$', PlayView.as_view(), name='play'),
    url(r'^flashcard/(?P<id>\d+)/(?P<grade>\d+)/$', NewIntervalView.as_view()),
]