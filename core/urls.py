from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True, next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('game/', views.game_view, name='game'),
    path('words/', views.word_list, name='word_list'),
    path('words/add/', views.add_word, name='add_word'),
    path('words/edit/<int:word_id>/', views.edit_word, name='edit_word'),
    path('words/delete/<int:word_id>/', views.delete_word, name='delete_word'),
    path('practice/', views.practice_menu, name='practice'),
    path('practice/difficulty/', views.practice_difficulty, name='practice_difficulty'),
    path('practice/start/<str:level>/', views.practice_start, name='practice_start'),
    path('practice/game/<str:level>/', views.practice_game, name='practice_game'),
]
