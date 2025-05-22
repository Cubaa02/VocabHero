from django.shortcuts import render

import random
from django.shortcuts import render
from .models import Word

def game_view(request):
    word = random.choice(Word.objects.all())  # náhodné slovo z databáze
    return render(request, 'core/game.html', {'word': word})
