from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class AppUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    email = models.EmailField(verbose_name='Почта', unique=True)
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        unique=True,
        null=True
    )
    first_name = models.CharField(verbose_name='Имя', max_length=30, null=True)
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=25
    )
    color = models.CharField(max_length=15, verbose_name='Цвет')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        null=True,
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(0, message='Ошибка ввода - меньше ноля')]
    )
    image = models.ImageField(
        verbose_name='Изображение',
        null=True
    )
    ingredients = models.ManyToManyField(
        through='RecipeIngredient',
        to='Ingredient'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    text = models.TextField(
        verbose_name='Описание',
        null=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=25,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe, on_delete=models.CASCADE, related_name='ingredients_in'
    )
    ingredient = models.ForeignKey(
        to=Ingredient, on_delete=models.CASCADE, related_name='ingredients_in'
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0, message='Ошибка ввода - меньше ноля')]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_favorite')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE,
                             related_name='favorite')

    class Meta:
        constraints = (models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='following_unique'),)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipes_in')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE,
                             related_name='current_user')

    class Meta:
        constraints = (models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='shopping_unique'),)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Subscription(models.Model):
    user = models.ForeignKey(AppUser,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    author = models.ForeignKey(AppUser,
                               on_delete=models.CASCADE,
                               related_name='subscriptors')

    class Meta:
        constraints = (models.UniqueConstraint(fields=['user', 'author'],
                                               name='subscription_unique'),)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
