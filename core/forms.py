from django import forms
from .models import Word, AcceptedTranslation

class WordForm(forms.ModelForm):
    alt_translations = forms.CharField(
        required=False,
        label="Alternativní překlady",
        widget=forms.TextInput(attrs={'placeholder': ' ...'})
    )

    class Meta:
        model = Word
        fields = ['english', 'czech', 'difficulty', 'example_sentence', 'category', 'alt_translations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            existing = [t.text for t in self.instance.accepted_translations.all()]
            self.fields['alt_translations'].initial = ", ".join(existing)

    def save(self, commit=True):
        instance = super().save(commit)

        alts_raw = self.cleaned_data.get("alt_translations", "")
        alts = [a.strip() for a in alts_raw.split(",") if a.strip()]

        instance.accepted_translations.all().delete()

        for a in alts:
            AcceptedTranslation.objects.create(word=instance, text=a)

        return instance
