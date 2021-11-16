import csv

from django.core.management.base import BaseCommand

from ...models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv', encoding='UTF-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit
                )
