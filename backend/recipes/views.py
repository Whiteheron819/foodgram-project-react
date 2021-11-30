from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import MySearchFilter, RecipeFilter
from .models import Ingredient, Recipe, AppUser, Tag, ShoppingList, Favorite, \
    Subscription
from .permissions import IsAuthorOrReadOnly
from .serializers import IngredientSerializer, FavoriteSerializer, \
    GetRecipeSerializer, \
    PostRecipeSerializer, TagsSerializer, ShoppingListSerializer, \
    RecipeToRepresentFavoriteSerializer, SubscribeSerializer, \
    CustomUserSerializer, GetSubscribeSerializer


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
    filter_backends = [MySearchFilter]
    search_fields = ['name', ]
    pagination_class = None


@api_view(['GET', 'DELETE'])
def add_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    favorited = Favorite.objects.filter(recipe=recipe,
                                        user=request.user).exists()
    data = {"user": request.user.id,
            "recipe": id,
            }
    if request.method == 'GET':
        serializer = FavoriteSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            recipe_serializer = (
                RecipeToRepresentFavoriteSerializer(recipe)
            )
            return Response(
                recipe_serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if request.method == 'DELETE':
            if not favorited:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            obj = Favorite.objects.filter(recipe=recipe, user=request.user)
            obj.delete()
            return Response('Рецепт удален из избранного',
                            status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if not subscribed:
            return Response("Нет такой подписки",
                            status=status.HTTP_400_BAD_REQUEST)
        obj = (Subscription.objects.filter(user=request.user,
                                           author=subscription_user))
        obj.delete()
        return Response('Автор удален из подписок', status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def subscriptions_list(request):
    subscription_list = AppUser.objects.filter(subscriptors__user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 6
    result_page = paginator.paginate_queryset(subscription_list, request)
    serializer = GetSubscribeSerializer(result_page,
                                        many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'DELETE'])
def shopping_list(request, id):
    data = {"user": request.user.id,
            "recipe": id,
            }
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'GET':
        serializer = ShoppingListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if request.method == 'DELETE':
            obj = ShoppingList.objects.filter(recipe=recipe, user=request.user)
            obj.delete()
            return Response('Рецепт удален из списка покупок',
                            status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_list(request):
    content = request.user.current_user.all()
    shop_list = {}
    text = 'Ваш список покупок: \n'
    for item in content:
        ingredients = item.recipe.ingredients_in.all()
        for recipe_ingredient in ingredients:
            name = recipe_ingredient.ingredient.name
            amount = recipe_ingredient.amount
            measure_unit = recipe_ingredient.ingredient.measurement_unit
            shop_list[name] = {}
            shop_list[name]['amount'] = amount
            shop_list[name]['measure_unit'] = measure_unit
    for name in shop_list:
        text += f'{name}'
        text += f' {shop_list[name]["amount"]}'
        text += f'{shop_list[name]["measure_unit"]}'
        text += f' \n'
    response = HttpResponse(text, 'Content-Type: application/txt')
    response['Content-Disposition'] = 'attachment; filename="wishlist"'
    return response
