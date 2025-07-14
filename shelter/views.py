from django.shortcuts import get_object_or_404, render

from shelter.models import *


# Create your views here.
def home(request):
    featured_animals = []  # Placeholder for featured animals logic
    animal_types = AnimalType.objects.all()
    featured_dogs = Animal.objects.filter(animal_type__name='Dog', status='available').order_by('-arrival_date')[:5]
    context = {
        'featured_animals':featured_animals,
        'featured_dogs':featured_dogs,
        'animal_types':animal_types,
    }
    return render(request,'shelter/home.html',context)

def animal_list(request):
    animals = Animal.objects.filter(status='available').order_by('-arrival_date')

    # Fetch all animal types for filtering
    animal_types = AnimalType.objects.all()

    # Animal Type Filtering
    animal_type_id = request.GET.get('animal_type')
    if animal_type_id:
        animals = animals.filter(animal_type_id = animal_type_id)


    context={
        'animals': animals,
        'animal_types': animal_types,
        'selected_animal_type':int(animal_type_id)if animal_type_id else None,
    }

    return render(request,'shelter/animal_list.html',context)


def animal_detail(request,animal_id):
    animal = get_object_or_404(Animal,id = animal_id)
    context ={
        'animal':animal,
    }
    return render(request,'shelter/animal_detail.html',context)
