from django.shortcuts import get_object_or_404, render, redirect
from shelter.models import Animal, AnimalType, ShelterProfile
from django.contrib.auth import login
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserCreationForm,
    CustomLoginForm,
    AnimalListingForm,
    )



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

    animals = Animal.objects.filter(
        status='available'
        ).order_by('-arrival_date')

    # Fetch all animal types for filtering
    animal_types = AnimalType.objects.all()
    # Animal Type Filtering
    animal_type_id = request.GET.get('animal_type')
    selected_animal_type = None

    if animal_type_id:
        try:
            selected_animal_type = int(animal_type_id)
        except(TypeError, ValueError):
            # Ignore malformed filter values.
            selected_animal_type = None

    if selected_animal_type is not None:
        animals = animals.filter(animal_type_id = selected_animal_type)

    context={
        'animals': animals,
        'animal_types': animal_types,
        'selected_animal_type':selected_animal_type,
    }

    return render(request,'shelter/animal_list.html',context)

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, "shelter/animal_detail.html", {"animal": animal})

@login_required
def animal_create(request):
    #TODO: check if we need to assign status from submitted data or need another approach
    if request.method == "POST":
        form = AnimalListingForm(request.POST)
    
        if form.is_valid():
            animal = form.save(commit=False)
            
            #Server Controled Values
            animal.posted_by = request.user
            
            animal.save()
            
            messages.success(
                request,
                "your animal listing has been created successfully"
            )
            
            return redirect(
                "shelter:animal_detail",
                pk=animal.pk,
            )
    else:
        form = AnimalListingForm()
        
    return render(
        request,
        "shelter/animal_create.html",
        {"form":form}
    )
    

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                if user.account_type == 'shelter':
                    ShelterProfile.objects.create(
                        user=user,
                        name = user.full_name,
                        contact_email = user.email,
                    )
            login(request, user)  # log in immediately

            # Redirect to ?next= if provided, otherwise to LOGIN_REDIRECT_URL
            redirect_to = request.GET.get("next")
            if not redirect_to or not url_has_allowed_host_and_scheme(
                url = redirect_to,
                allowed_hosts = {request.get_host()},
                require_https = request.is_secure(),
            ):
                redirect_to = reverse(settings.LOGIN_REDIRECT_URL)

            return redirect(redirect_to)

    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
            
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "registration/login.html"