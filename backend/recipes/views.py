from djoser.serializers import UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Ingredient, Recipe, AppUser, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import IngredientSerializer, GetRecipeSerializer, \
    PostRecipeSerializer, TagsSerializer, ShoppingListSerializer
from .filters import MySearchFilter, RecipeFilter


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


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
def shopping_list(request, id):
    data = {"user": request.user.id,
            "recipe": id,
            }
    if request.method == 'GET':
        serializer = ShoppingListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        pass
