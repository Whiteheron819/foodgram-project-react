from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


def get_existence(self, obj, model):
    request = self.context.get('request')
    if request is None or request.user.is_anonymous:
        return False
    return model.objects.filter(user=request.user, recipe=obj).exists()


def update_or_create_ingredients(instance, ingredients):
    for ingredient in ingredients:
        current_ingredient = (
            get_object_or_404(Ingredient, pk=ingredient['ingredient']['id'].id)
            )
        if (RecipeIngredient.objects.filter(
                recipe=instance,
                ingredient=current_ingredient).exists()):
            instance.ingredients.amount = (
                    ingredient['amount']
            )
        else:
            RecipeIngredient.objects.update_or_create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )
