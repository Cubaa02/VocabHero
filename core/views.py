from django.shortcuts import render
import random
from django.shortcuts import render
from .models import Word
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from .models import Word
from django.http import HttpResponse
from django.http import HttpResponseForbidden
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

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
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


def home(request):
    return render(request, 'core/home.html')


def practice_menu(request):
    return render(request, 'core/practice.html')


def practice_difficulty(request):
    return render(request, 'core/practice_difficulty.html')


def practice_start(request, level):
    words = Word.objects.filter(difficulty=level)
    return render(request, 'core/practice_start.html', {
        'words': words,
        'level': level
    })


def practice_game(request, level):
    # Všechna slovíčka podle zvolené obtížnosti
    words = list(Word.objects.filter(difficulty=level))

    if len(words) < 4:
        return render(request, 'core/practice_game.html', {
            'error': 'Tahle sada potřebuje alespoň 4 slovíčka!'
        })

    # Vyber náhodné hlavní slovíčko
    current_word = random.choice(words)

    # Vytvoř možnosti (včetně správné)
    choices = [current_word]
    while len(choices) < 4:
        option = random.choice(words)
        if option not in choices:
            choices.append(option)

    # Zamíchej možnosti
    random.shuffle(choices)

    return render(request, 'core/practice_game.html', {
        'word': current_word,
        'choices': choices,
        'level': level
    })