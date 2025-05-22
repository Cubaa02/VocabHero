from django.db import models

class Word(models.Model):
    english = models.CharField(max_length=100)
    czech = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ])
    
    def __str__(self):
        return self.english
