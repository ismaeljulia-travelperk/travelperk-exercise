from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from ingredients.models import Ingredient
from recipes.models import Recipe
from . import serializer


class ListCreateRecipesAPI(ListCreateAPIView):
    serializers_classes = (serializer.ListRecipeSerializer, serializer.CreateRecipeSerializer)

    def get_queryset(self):
        recipes = Recipe.objects.all()
        recipe_name = self.request.query_params.get('name')
        if recipe_name is not None:
            recipes = recipes.filter(name__startswith=recipe_name)
        return recipes

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.serializers_classes[0]
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = self.serializers_classes[1]
        return super().create(request, *args, **kwargs)


class RetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializers_classes = (
        serializer.ListRecipeSerializer, serializer.DestroyRecipeSerializer, serializer.UpdateRecipeSerializer)

    def get(self, request, *args, **kwargs):
        self.serializer_class = self.serializers_classes[0]
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        Ingredient.objects.filter(recipe_id=self.kwargs[
            'pk']).delete()  # a bit dirty (?) investigating if this can be done in the serializer overriding a method
        self.serializer_class = self.serializers_classes[1]
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = self.serializers_classes[2]
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = self.serializers_classes[2]
        return self.partial_update(request, *args, **kwargs)
