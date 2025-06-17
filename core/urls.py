from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='word_list'), name='logout'),
    path('game/', views.game_view, name='game'),
    path('words/', views.word_list, name='word_list'),
    path('words/add/', views.add_word, name='add_word'),
    path('words/edit/<int:word_id>/', views.edit_word, name='edit_word'),
    path('words/delete/<int:word_id>/', views.delete_word, name='delete_word'),
]
