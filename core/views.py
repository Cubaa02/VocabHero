from django.shortcuts import render
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from .models import Word, Category, Mistake, UserProfile
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .forms import WordForm  
from django.http import JsonResponse


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
    def words_with_alts(qs):
        qs = qs.prefetch_related('accepted_translations')
        return [
            {
                "id": w.id,
                "english": w.english,
                "czech": w.czech,
                "alts": [t.text for t in w.accepted_translations.all()],
            }
            for w in qs
        ]

    easy_words = words_with_alts(Word.objects.filter(difficulty="easy"))
    medium_words = words_with_alts(Word.objects.filter(difficulty="medium"))
    hard_words = words_with_alts(Word.objects.filter(difficulty="hard"))

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

    words = Word.ordered_by_difficulty().prefetch_related('accepted_translations', 'category')

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

@login_required
@require_POST
def record_mistake(request):
    """
    Endpoint: POST JSON { word_id: <int> } 
    Inkrementuje nebo vytvoří Mistake pro přihlášeného uživatele a dané slovo.
    """
    # načíst JSON tělo
    try:
        data = json.loads(request.body.decode('utf-8') or "{}")
    except Exception:
        data = {}

    word_id = data.get('word_id') or data.get('id')
    english = data.get('english')

    # vyřešit koho použít do FK (User vs UserProfile)
    user_field_model = Mistake._meta.get_field('user').remote_field.model
    if user_field_model.__name__ == 'UserProfile':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_for_fk = profile
    else:
        user_for_fk = request.user

    # najít Word
    word = None
    if word_id:
        try:
            word = Word.objects.get(pk=word_id)
        except Word.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'word not found (id)'}, status=404)
    elif english:
        word = Word.objects.filter(english__iexact=english).first()
        if not word:
            return JsonResponse({'ok': False, 'error': 'word not found (english)'}, status=404)
    else:
        return JsonResponse({'ok': False, 'error': 'no word identifier provided'}, status=400)

    # get_or_create Mistake a bump
    mistake, created = Mistake.objects.get_or_create(user=user_for_fk, word=word)
    mistake.bump()

    return JsonResponse({'ok': True, 'incorrect_count': mistake.incorrect_count})

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    total_mistakes = Mistake.objects.filter(user=profile).count()
    total_words = Word.objects.count()
    top_mistakes = Mistake.objects.filter(user=profile).select_related('word').order_by('-incorrect_count')[:5]

    return render(request, 'core/profile.html', {
        'profile': profile,
        'total_mistakes': total_mistakes,
        'total_words': total_words,
        'top_mistakes': top_mistakes
    })