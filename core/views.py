from django.shortcuts import render

import random
from django.shortcuts import render
from .models import Word
from django.db.models import Q

def game_view(request):
    word = random.choice(Word.objects.all())  # náhodné slovo z databáze
    return render(request, 'core/game.html', {'word': word})

def word_list(request):
    query = request.GET.get("q", "")
    difficulty = request.GET.get("difficulty", "")

    words = Word.objects.all()

    if query:
        words = words.filter(
            Q(english__icontains=query) |
            Q(czech__icontains=query)
        )

    if difficulty:
        words = words.filter(difficulty=difficulty)

    return render(request, 'core/word_list.html', {'words': words})