from rest_framework import serializers

from ingredients.models import Ingredient
from .models import Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class ListRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']

    @staticmethod
    def get_ingredients(obj):
        ingredients = Ingredient.objects.filter(recipe=obj.id)
        return IngredientSerializer(ingredients, many=True).data


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, write_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']

    def create(self, validated_data):
        recipe_instance = Recipe.objects.create(name=validated_data.pop('name'),
                                                description=validated_data.pop('description'))
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            ingredient_name = ingredient.get('name')
            if not ingredient_name:
                continue
            Ingredient.objects.create(name=ingredient_name, recipe=recipe_instance)
        return recipe_instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["ingredients"] = Ingredient.objects.filter(recipe_id=instance.id).values('name')
        return data


class UpdateRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, write_only=True,
                                       required=False)  # write_only because ingredients field is not part of the model

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']
        extra_kwargs = {"name": {"required": False}, "description": {"required": False}}

    def update(self, instance, validated_data):
        recipe_instance = Recipe.objects.get(id=instance.id)
        recipe_instance.name = validated_data.get('name', recipe_instance.name)
        recipe_instance.description = validated_data.get('description', recipe_instance.description)
        recipe_instance.save()
        ingredients = validated_data.get('ingredients')
        if ingredients is None:
            return recipe_instance
        ingredients_created = []
        for ingredient in ingredients:
            ingredient_name = ingredient.get('name')
            if not ingredient_name:
                continue
            ingredients_created.append(Ingredient.objects.create(name=ingredient_name, recipe=recipe_instance).id)
        Ingredient.objects.filter(recipe_id=instance.id).exclude(id__in=ingredients_created).delete()
        return recipe_instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["ingredients"] = Ingredient.objects.filter(recipe_id=instance.id).values('name')
        return data


class DestroyRecipeSerializer(serializers.ModelSerializer):
    pass
