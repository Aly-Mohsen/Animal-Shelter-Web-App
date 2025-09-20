from django.urls import path
from .import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from shelter import views as shelter_views

app_name = 'shelter'

urlpatterns = [
    path('',views.home, name = 'home'),
    path('animals/',views.animal_list,name = 'animal_list',),
    path("animals/<int:pk>/", views.animal_detail, name="animal_detail"),

    # Auth
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="shelter:home"), name="logout"),
    path("signup/", shelter_views.signup, name="signup"),
    
]