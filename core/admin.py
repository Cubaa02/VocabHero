from django.contrib import admin
from .models import Word, Category, GameResult, UserProfile

admin.site.register(Word)
admin.site.register(Category)
admin.site.register(GameResult)
admin.site.register(UserProfile)