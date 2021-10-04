from rest_framework import routers
from .api import RecipeViewSet, UserViewSet, TagViewSet, IngredientViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register('api/recipes', RecipeViewSet, 'recipes')
router.register('api/users', UserViewSet, 'users')
router.register('api/tags', TagViewSet, 'tags')
router.register('api/ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
