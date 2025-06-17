from django import forms
from .models import Word

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['english', 'czech', 'difficulty', 'example_sentence', 'category']
        widgets = {
            'english': forms.TextInput(attrs={'class': 'form-control'}),
            'czech': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'example_sentence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
