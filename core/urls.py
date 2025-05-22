from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.game_view, name='game'),
    path('words/', views.word_list, name='word_list'),
]
