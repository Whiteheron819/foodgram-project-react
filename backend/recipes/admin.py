from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient

admin.site.register(RecipeIngredient)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
