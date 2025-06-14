from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Case, When, Value, IntegerField, QuerySet
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Word(models.Model):
    english = models.CharField(
        max_length=100,
        verbose_name="Anglické slovo",
        help_text="Zadej slovo v angličtině (bez speciálních znaků)",
        validators=[RegexValidator(r'^[a-zA-Z\s\-]+$', 'Pouze písmena, mezery a pomlčky')]
    )
    czech = models.CharField(
        max_length=100,
        verbose_name="Český překlad",
        help_text="Zadej český překlad"
    )
    difficulty = models.CharField(
        max_length=10,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ],
        verbose_name="Obtížnost",
        help_text="Vyber obtížnost slova"
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Kategorie",
        help_text="Vyber kategorii (nepovinné)"
    )

    example_sentence = models.TextField(
        blank=True,
        null=True,
        verbose_name="Příklad věty",
        help_text="Věta, kde se používá anglické slovo"
    )
    
    class Meta:
        verbose_name = "Slovo"
        verbose_name_plural = "Slova"
        ordering = ['difficulty']   

    def __str__(self):
        return self.english

    @classmethod
    def ordered_by_difficulty(cls) -> QuerySet:
        return cls.objects.annotate(
            difficulty_order=Case(
                When(difficulty='easy', then=Value(1)),
                When(difficulty='medium', then=Value(2)),
                When(difficulty='hard', then=Value(3)),
                output_field=IntegerField()
            )
        ).order_by('difficulty_order', 'english')
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorie"
        ordering = ['name']

    def __str__(self):
        return self.name
    
class GameResult(models.Model):
    user = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name="Uživatel",
        help_text="Profil uživatele, který hrál hru",
        null=True,  # ← dočasné!
        blank=True  # ← pro admin rozhraní, nepovinné
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Skóre",
        help_text="Počet bodů získaných ve hře"
    )
    duration = models.DurationField(
        verbose_name="Délka hry",
        help_text="Jak dlouho hra trvala",
        null=True,
        blank=True
    )
    mistakes = models.PositiveIntegerField(
        default=0,
        verbose_name="Počet chyb",
        help_text="Kolik chyb udělal hráč"
    )
    mode = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium',
        verbose_name="Režim hry",
        help_text="Zvolená obtížnost hry"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Datum a čas",
        help_text="Kdy byla hra dokončena"
    )

    class Meta:
        verbose_name = "Výsledek hry"
        verbose_name_plural = "Výsledky her"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.score} pts @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Uživatel",
        null=True,  # ← dočasné!
        blank=True  # ← pro admin rozhraní, nepovinné
    )
    nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Přezdívka"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Vytvořeno"
    )

    class Meta:
        verbose_name = "Profil uživatele"
        verbose_name_plural = "Profily uživatelů"

    def __str__(self):
        return self.nickname if self.nickname else self.user.username