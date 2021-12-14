from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (AppUser, Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Subscription, Tag)
from .utils import get_existence, update_or_create_ingredients


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = AppUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return (
            Subscription.objects.filter(user=request.user, author=obj).exists()
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class GetRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = (
        serializers.CharField(read_only=True,
                              source='ingredient.measurement_unit')
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class PostRecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = (
        serializers.CharField(read_only=True,
                              source='ingredient.measurement_unit')
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class GetRecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True,
                                             read_only=True,
                                             source='ingredients_in')
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return get_existence(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return get_existence(self, obj, ShoppingList)


class PostRecipeSerializer(serializers.ModelSerializer):
    ingredients = PostRecipeIngredientSerializer(
        many=True,
        source='ingredients_in'
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_in')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        update_or_create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients_in')
            instance.ingredients.clear()
            update_or_create_ingredients(instance, ingredients)
        if 'tags' in self.initial_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        super().update(instance, validated_data)
        return instance

    def validate(self, data):
        ingredients = data['ingredients_in']
        existing_ingredients = {}
        for ingredient in ingredients:
            if (
                    ingredient['ingredient']['id']
            ) not in existing_ingredients:
                instance = ingredient['ingredient']['id']
                existing_ingredients[instance] = True
            else:
                raise serializers.ValidationError(
                    'Повторяющиеся ингредиенты в списке'
                )
        return data


class ShoppingListSerializer(serializers.ModelSerializer):

    def validate(self, data):
        id = data['recipe'].id
        user = data['user']
        if ShoppingList.objects.filter(recipe=id, user=user).exists():
            raise serializers.ValidationError(
                'Рецепт уже в вашем списке покупок!'
            )
        return data

    class Meta:
        model = ShoppingList
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):

    def validate(self, data):
        recipe_id = data['recipe'].id
        user = data['user']
        if Favorite.objects.filter(recipe=recipe_id, user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
                )
        return data

    class Meta:
        model = Favorite
        fields = '__all__'


class RecipeToRepresentFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSubscribe(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):

    def validate(self, data):
        author = data['author']
        user = data['user']
        if Subscription.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError('You are subscribed already!')
        return data

    class Meta:
        model = Subscription
        fields = '__all__'


class GetSubscribeSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscribe(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = AppUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed', 'recipes',
                  'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return (
            Subscription.objects.filter(user=request.user, author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()
