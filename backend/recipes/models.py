from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


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
        related_name="recipes"
    )
    text = models.TextField(
        verbose_name='Описание',
        null=True
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        null=True
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    ingredients = models.ManyToManyField(
        through='RecipeIngredient',
        to='Ingredient'
    )
    tags = models.ManyToManyField(
        through='RecipeTag',
        to='Tag'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=25,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='ingredients_in')
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE, related_name='ingredients_in')
    amount = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_favorite')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE,
                             related_name='favorite')


class ShoppingList(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipes_in')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE,
                             related_name='current_user')


class Subscription(models.Model):
    user = models.ForeignKey(AppUser,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    author = models.ForeignKey(AppUser,
                               on_delete=models.CASCADE,
                               related_name='subcriptors')