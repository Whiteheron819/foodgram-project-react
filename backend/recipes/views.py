from djoser.serializers import UserSerializer
from rest_framework import viewsets, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Ingredient, Recipe, AppUser, Tag
from .serializers import IngredientSerializer, GetRecipeSerializer, PostRecipeSerializer, TagsSerializer
from .permissions import IsAuthorOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer = PostRecipeSerializer
    permission_class = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetRecipeSerializer
        return PostRecipeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        elif self.request.method == "POST":
            return [permissions.IsAdminUser()]
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


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = IngredientSerializer
