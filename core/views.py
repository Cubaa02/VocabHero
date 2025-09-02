from django.shortcuts import render
import random
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from .models import Word, Category
from django.http import HttpResponse, HttpResponseForbidden
from .forms import WordForm  
from django.http import JsonResponse
from django.core.serializers import serialize
from django.forms.models import model_to_dict


@login_required
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word_list')  
    else:
        form = WordForm()
    return render(request, 'core/add_word.html', {'form': form})


def hero_mode(request):
    easy_words = list(Word.objects.filter(difficulty="easy").values("english", "czech"))
    medium_words = list(Word.objects.filter(difficulty="medium").values("english", "czech"))
    hard_words = list(Word.objects.filter(difficulty="hard").values("english", "czech"))

    level_data = {
        "easy": easy_words,
        "medium": medium_words,
        "hard": hard_words
    }

    return render(request, "core/hero_mode.html", {
        "level_data": json.dumps(level_data, ensure_ascii=False)
    })



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


def get_mode_label(mode, value):
    if mode == 'difficulty':
        labels = {
            'easy': '🟢 Začátečník',
            'medium': '🟡 Pokročilý',
            'hard': '🔴 Expert',
        }
        return labels.get(value, 'Neznámá obtížnost')
    elif mode == 'category':
        category = Category.objects.filter(pk=value).first()
        return f'📚 {category.name}' if category else 'Neznámá kategorie'
    elif mode == 'remix':
        return '🎧 reMIX'
    else:
        return 'Neznámý režim'
    

def practice_game(request, mode, value=None):
    if mode == 'difficulty':
        words = list(Word.objects.filter(difficulty=value).values("id", "english", "czech"))
        mode_label = get_mode_label(mode, value)
    elif mode == 'category':
        category = get_object_or_404(Category, pk=value)
        words = list(Word.objects.filter(category=category).values("id", "english", "czech"))
        mode_label = get_mode_label(mode, value)
    elif mode == 'remix':
        words = list(Word.objects.all().values("id", "english", "czech"))
        mode_label = '🎧 reMIX'
    else:
        return render(request, 'core/practice.html', {'error': 'Neplatný režim!'})

    if len(words) < 4:
        return render(request, 'core/practice.html', {
            'error': 'Tahle sada potřebuje alespoň 4 slovíčka!'
        })

    return render(request, 'core/practice_game.html', {
        "words": json.dumps(words, ensure_ascii=False),
        "mode": mode,
        "value": value,
        "mode_label": mode_label
    })


def practice_category(request):
    categories = Category.objects.all()
    return render(request, 'core/practice_category.html', {
        'categories': categories
    })


def unified_practice_start(request, mode, value=None):
    progress_key = ''
    words = []
    context = {}

    if mode == 'difficulty':
        progress_key = f'practice_progress_{value}'
        request.session[progress_key] = []
        words = Word.objects.filter(difficulty=value)
        context['level'] = value

    elif mode == 'category':
        category = get_object_or_404(Category, pk=value)
        progress_key = f'practice_category_progress_{value}'
        request.session[progress_key] = []
        words = Word.ordered_by_difficulty().filter(category=category)
        context['category'] = category

    elif mode == 'remix':
        progress_key = 'practice_remix_progress'
        request.session[progress_key] = []
        words = Word.ordered_by_difficulty()
        context['remix'] = True

    else:
        return render(request, 'core/practice.html', {'error': 'Neplatný režim!'})

    context['words'] = words
    context['mode'] = mode
    context['value'] = value
    context['mode_label'] = get_mode_label(mode, value)
    return render(request, 'core/practice_start.html', context)

def practice_difficulty(request):
    return render(request, 'core/practice_difficulty.html')
