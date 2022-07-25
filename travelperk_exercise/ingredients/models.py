from django.db import models

from recipes.models import Recipe


# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  # assume a given ingredient belongs only to one recipe

    def __str__(self):
        return self.name
