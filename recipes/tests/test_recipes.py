from unittest import TestCase

from rest_framework.test import APIClient

from ingredients.models import Ingredient
from recipes.models import Recipe


class RecipeTestCreateCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def tearDown(self) -> None:
        Ingredient.objects.filter().delete()
        Recipe.objects.filter().delete()
        super().tearDown()

    def test_recipe_create_api(self):
        data = {
            "name": "Pizza",
            "description": "Put it in the oven, or not",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }
        self.create_recipe = self.client.post('/recipes/', data, format='json')
        self.assertEquals(self.create_recipe.status_code, 201)
        self.assertEquals(data['name'], self.create_recipe.json()['name'])
        self.assertEquals(data['description'], self.create_recipe.json()['description'])
        self.assertEquals(data['ingredients'],
                          self.create_recipe.json()['ingredients'])

    def test_recipe_get_api(self):
        data = {
            "name": "Pizza",
            "description": "Put it in the oven, or not",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }
        self.create_recipe = self.client.post('/recipes/', data, format='json')
        recipe_id = self.create_recipe.json()['id']
        self.get_recipe = self.client.get(f'/recipes/{recipe_id}', format='json')
        self.assertEquals(self.get_recipe.status_code, 200)
        self.assertEquals(data['name'], self.get_recipe.json()['name'])
        self.assertEquals(data['description'], self.get_recipe.json()['description'])
        self.assertEquals(data['ingredients'],
                          self.get_recipe.json()['ingredients'])

    def test_recipe_get_by_name_api(self):
        data = {
            "name": "Pizza",
            "description": "Put it in the oven, or not",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }
        self.create_recipe = self.client.post('/recipes/', data, format='json')
        self.get_recipe = self.client.get(f"/recipes/?name={data['name'][:2]}", format='json')
        self.assertEquals(self.get_recipe.status_code, 200)
        self.assertEquals(len(self.get_recipe.json()), 1)
        self.assertEquals(data['name'], self.get_recipe.json()[0]['name'])
        self.assertEquals(data['description'], self.get_recipe.json()[0]['description'])
        self.assertEquals(data['ingredients'],
                          self.get_recipe.json()[0]['ingredients'])

    def test_recipe_get_by_non_existing_name_api(self):
        data = {
            "name": "Pizza",
            "description": "Put it in the oven, or not",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }
        self.create_recipe = self.client.post('/recipes/', data, format='json')
        self.get_recipe = self.client.get(f"/recipes/?name=test", format='json')
        self.assertEquals(self.get_recipe.status_code, 200)
        self.assertEquals(len(self.get_recipe.json()), 0)

    def test_recipe_patch_api(self):
        data = {
            "name": "Pizza",
            "description": "Put it in the oven, or not",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }
        data_updated = {
            "name": "Pizza1",
            "description": "Put it in the oven",
            "ingredients": [{"name": "casa-tarradellas"}]
        }
        self.create_recipe = self.client.post('/recipes/', data, format='json')
        recipe_id = self.create_recipe.json()['id']
        self.patch_recipe = self.client.patch(f'/recipes/{recipe_id}', data_updated, format='json')
        self.assertEquals(self.patch_recipe.status_code, 200)
        self.assertEquals(data_updated['name'], self.patch_recipe.json()['name'])
        self.assertEquals(data_updated['description'], self.patch_recipe.json()['description'])
        self.assertEquals(data_updated['ingredients'],
                          self.patch_recipe.json()['ingredients'])

    def test_recipe_delete_api(self):
        data = {
            "name": "Pizza",
            "description": "Put it in the oven, or not",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }
        self.create_recipe = self.client.post('/recipes/', data, format='json')
        recipe_id = self.create_recipe.json()['id']
        self.delete_recipe = self.client.delete(f'/recipes/{recipe_id}', format='json')
        self.assertEquals(self.delete_recipe.status_code, 204)
        self.assertEquals(0, len(Ingredient.objects.all()))
