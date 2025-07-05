from django.urls import path
from .import views


app_name = 'shelter'

urlpatterns = [
    path('',views.home, name = 'home'),
    path('animals/',views.animal_list,name = 'animals_list',)
]