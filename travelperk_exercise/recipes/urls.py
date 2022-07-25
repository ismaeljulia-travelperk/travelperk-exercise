from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCreateRecipesAPI.as_view()),
    path('<int:pk>', views.RetrieveUpdateDestroyAPI.as_view())
]
