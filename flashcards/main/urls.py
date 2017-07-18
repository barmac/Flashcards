from django.conf.urls import url, include
from .views import MainView, LogoutView, FlashcardsView, PlayView, NewIntervalView


urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^flashcards/$', FlashcardsView.as_view(), name='flashcards'),
    url(r'^play/$', PlayView.as_view(), name='play'),
    url(r'^flashcard/(?P<id>\d+)/(?P<grade>\d+)/$', NewIntervalView.as_view()),
]