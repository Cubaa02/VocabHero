from django.contrib import admin
from .models import Word, Category, UserProfile, Mistake 

admin.site.register(Word)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Mistake)