from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Ingredient, RecipeIngredient, Recipe, Tag, AppUser


class UserAdmin(BaseUserAdmin):
    list_display = ('email', )
    search_fields = ('email', 'first_name')
    ordering = ('email',)


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine, TagRecipeInline)


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(AppUser, UserAdmin)
