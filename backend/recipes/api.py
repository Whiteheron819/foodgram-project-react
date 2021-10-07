from .models import Ingredient, Recipe, AppUser, Tag
from rest_framework import mixins, viewsets, permissions
from .serializers import IngredientSerializer, RecipeSerializer, UserSerializer, TagsSerializer
from rest_framework.request import Request
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RecipeSerializer


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
