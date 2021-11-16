from rest_framework import routers
from .views import RecipeViewSet, UserViewSet, TagViewSet, IngredientViewSet, shopping_list
from django.urls import include, path

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, 'recipes')
router.register('users', UserViewSet, 'users')
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('api/recipes/<int:id>/shopping_cart/',
         shopping_list,
         name='making_the_cart'),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
