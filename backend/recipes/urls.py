from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet,
                    TagViewSet, add_favorite, download_shopping_list,
                    shopping_list, subscription, subscriptions_list)

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, 'recipes')
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('api/users/subscriptions/',
         subscriptions_list,
         name='user_subscription'),
    path('api/users/<int:id>/subscribe/',
         subscription,
         name='user_subscription'),
    path('api/recipes/<int:id>/shopping_cart/',
         shopping_list,
         name='making_the_cart'),
    path('api/recipes/<int:id>/favorite/',
         add_favorite,
         name='add_to_favorite'),
    path('api/recipes/download_shopping_cart/',
         download_shopping_list,
         name='dsc'),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
