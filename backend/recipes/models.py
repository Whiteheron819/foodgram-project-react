from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MeasureUnit(models.TextChoices):
    GRAM = 'GRAM', 'г.'

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Tags(models.TextChoices):
    BREAKFAST = 'BREAKFAST', 'завтрак'
    DINNER = 'DINNER', 'обед'
    SUPPER = 'SUPPER', 'ужин'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        null=True,
        related_name="recipes"
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True
    )
    time = models.PositiveIntegerField(
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
    slug = models.SlugField(
        null=False,
        unique=True,
        max_length=80
    )
    tags = models.CharField(
        verbose_name='Теги',
        max_length=256,
        choices=Tags.choices
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


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
