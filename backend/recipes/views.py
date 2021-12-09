from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (AppUser, Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Subscription, Tag)
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          GetRecipeSerializer, GetSubscribeSerializer,
                          IngredientSerializer, PostRecipeSerializer,
                          RecipeToRepresentFavoriteSerializer,
                          ShoppingListSerializer, SubscribeSerializer,
                          TagsSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer = PostRecipeSerializer
    permission_class = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetRecipeSerializer
        return PostRecipeSerializer


class CustomUserViewSet(UserViewSet):
    queryset = AppUser.objects.all()
    serializer_class = CustomUserSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter]
    search_fields = ['name', ]
    pagination_class = None


@api_view(['GET', 'DELETE'])
@login_required()
def add_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    favorited = Favorite.objects.filter(recipe=recipe,
                                        user=request.user).exists()
    data = {'user': request.user.id,
            'recipe': id,
            }
    if request.method == 'GET':
        serializer = FavoriteSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe_serializer = (
            RecipeToRepresentFavoriteSerializer(recipe)
        )
        return Response(
            recipe_serializer.data, status=status.HTTP_201_CREATED
        )

    if request.method == 'DELETE':
        if not favorited:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = Favorite.objects.filter(recipe=recipe, user=request.user)
        obj.delete()
        return Response('Рецепт удален из избранного',
                            status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@login_required()
def subscription(request, id):
    subscription_user = get_object_or_404(AppUser, id=id)
    user = request.user
    subscribed = (
        Subscription.objects.filter(user=user,
                                    author=subscription_user).exists()
    )
    data = {'user': request.user.id,
            'author': id}
    if request.method == 'GET':
        serializer = SubscribeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        if not subscribed:
            return Response("Нет такой подписки",
                            status=status.HTTP_400_BAD_REQUEST)
        obj = (Subscription.objects.filter(user=request.user,
                                           author=subscription_user))
        obj.delete()
        return Response('Автор удален из подписок', status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@login_required()
def subscriptions_list(request):
    subscription_list = AppUser.objects.filter(subscriptors__user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 6
    result_page = paginator.paginate_queryset(subscription_list, request)
    serializer = GetSubscribeSerializer(result_page,
                                        many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'DELETE'])
@login_required()
def shopping_list(request, id):
    data = {'user': request.user.id,
            'recipe': id,
            }
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'GET':
        serializer = ShoppingListSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        if request.method == 'DELETE':
            obj = ShoppingList.objects.filter(recipe=recipe, user=request.user)
            obj.delete()
            return Response('Рецепт удален из списка покупок',
                            status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_list(request):
    text = 'Ваш список покупок: \n'
    shop_list = {}
    items = RecipeIngredient.objects.filter(
        recipe__recipes_in__user=request.user
    )
    for item in items:
        ingredients = item.ingredient.ingredients_in.values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )[0]
        name, unit, amount = ingredients[0], ingredients[1], ingredients[2]
        shop_list[name] = {}
        shop_list[name]['amount'] = amount
        shop_list[name]['measure_unit'] = unit
    for name in shop_list:
        text += f'{name}'
        text += f' {shop_list[name]["amount"]}'
        text += f'{shop_list[name]["measure_unit"]}'
        text += f' \n'
    response = HttpResponse(text, 'Content-Type: application/txt')
    response['Content-Disposition'] = 'attachment; filename="wishlist"'
    return response
