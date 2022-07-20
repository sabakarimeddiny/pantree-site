from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_ingredients, name='get_ingredients'),
    path('results/', views.result, name='result_page'),
]