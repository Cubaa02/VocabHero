from django.shortcuts import render
import random
from django.shortcuts import render
from .models import Word
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Word
from django.http import HttpResponse
from .forms import WordForm  

@login_required
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word_list')  # název url pro /words
    else:
        form = WordForm()
    return render(request, 'core/add_word.html', {'form': form})

def game_view(request):
    word = random.choice(Word.objects.all())  
    return render(request, 'core/game.html', {'word': word})

def word_list(request):
    query = request.GET.get("q", "")
    difficulty = request.GET.get("difficulty", "")  

    words = Word.ordered_by_difficulty()  

    if query:
        words = words.filter(
            Q(english__icontains=query) |
            Q(czech__icontains=query)
        )

    if difficulty:
        words = words.filter(difficulty=difficulty)

    return render(request, 'core/word_list.html', {
        'words': words,
        'selected_difficulty': difficulty
    })

@login_required
def edit_word(request, word_id):
    word = Word.objects.get(id=word_id)
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('word_list')
    else:
        form = WordForm(instance=word)
    
    return render(request, 'core/edit_word.html', {'form': form, 'word': word})

def delete_word(request, word_id):
    return HttpResponse("Mazání slovíčka zatím není hotové.")