from rest_framework import routers
from .api import RecipeViewSet, UserViewSet, TagViewSet, IngredientViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, 'recipes')
router.register('users', UserViewSet, 'users')
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
