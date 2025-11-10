from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Case, When, Value, IntegerField, QuerySet
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
import unicodedata


def normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = s.strip().lower()
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s) if unicodedata.category(ch) != "Mn")
    s = " ".join(s.split())
    return s

class Word(models.Model):
    english = models.CharField(
        max_length=100,
        verbose_name="Anglické slovo",
        help_text="Zadej slovo v angličtině (bez speciálních znaků)",
        validators=[RegexValidator(r'^[a-zA-Z\s\-\(\)]+$', 'Pouze písmena, mezery, pomlčky a závorky')]
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
    
    def acceptable_normalized_set(self):
        base = {normalize_text(self.czech)}
        variants = {t.normalized for t in self.accepted_translations.all()}
        return base | variants

    def acceptable_display_list(self):
        return [self.czech] + [t.text for t in self.accepted_translations.all()]

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
    
    
class AcceptedTranslation(models.Model):
    word = models.ForeignKey(
        Word,
        related_name="accepted_translations",
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=100,
        verbose_name="Alternativní překlad"
    )
    normalized = models.CharField(
        max_length=120,
        editable=False,
        db_index=True
    )

    class Meta:
        verbose_name = "Akceptovaná varianta"
        verbose_name_plural = "Akceptované varianty"
        unique_together = (("word", "normalized"),)

    def save(self, *args, **kwargs):
        self.normalized = normalize_text(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorie"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    
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
    

class Mistake(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='mistakes',
        verbose_name="Uživatel"
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='mistakes',
        verbose_name="Slovo"
    )
    incorrect_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Počet chyb"
    )
    first_incorrect = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="První chyba"
    )
    last_incorrect = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Poslední chyba"
    )

    class Meta:
        verbose_name = "Chyba"
        verbose_name_plural = "Chyby"
        unique_together = ('user', 'word')
        ordering = ['-incorrect_count', '-last_incorrect']

    def __str__(self):
        return f"{self.user} – {self.word} ({self.incorrect_count})"

    def bump(self):
        now = timezone.now()
        if not self.first_incorrect:
            self.first_incorrect = now
        self.last_incorrect = now
        self.incorrect_count += 1
        self.save(update_fields=['incorrect_count', 'last_incorrect', 'first_incorrect'])
