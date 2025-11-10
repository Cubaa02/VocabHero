from django.contrib import admin
from .models import Word, Category, UserProfile, Mistake, AcceptedTranslation

class AcceptedTranslationInline(admin.TabularInline):
    model = AcceptedTranslation
    extra = 1

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("english", "czech", "difficulty", "category")
    search_fields = ("english", "czech")
    list_filter = ("difficulty", "category")
    inlines = [AcceptedTranslationInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nickname", "created_at")
    search_fields = ("user__username", "nickname")

@admin.register(Mistake)
class MistakeAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "incorrect_count", "last_incorrect")
    search_fields = ("user__user__username", "word__english", "word__czech")
    list_filter = ("incorrect_count",)

@admin.register(AcceptedTranslation)
class AcceptedTranslationAdmin(admin.ModelAdmin):
    list_display = ("word", "text")
    search_fields = ("text", "word__english", "word__czech")
