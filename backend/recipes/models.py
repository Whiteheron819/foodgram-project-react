from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    email = models.EmailField(unique=True)


class MeasureUnit(models.TextChoices):
    GRAM = 'г.'

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=25
    )
    color = models.CharField(max_length=15)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


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
    measure_unit = models.CharField(
        verbose_name='Единицы измерения',
        choices=MeasureUnit.choices,
        max_length=256,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
