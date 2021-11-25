from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Ingredient, RecipeIngredient, Recipe, Tag, AppUser, Favorite


class UserAdmin(BaseUserAdmin):
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


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
admin.site.register(Favorite)
