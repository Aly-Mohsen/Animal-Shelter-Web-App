from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to="users/", blank=True, null=True)

    def __str__(self):
        return self.username


class AnimalType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.animal_type})"


class Animal(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available for Adoption'),
        ('pending', 'Pending Adoption'),
        ('adopted', 'Adopted'),
        ('medical', 'Medical Hold'),
    ]

    name = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    age = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    arrival_date = models.DateField(default=timezone.now)
    adoption_date = models.DateField(null=True, blank=True)
    special_needs = models.TextField(blank=True)
    is_vaccinated = models.BooleanField(default=False)
    is_spayed_neutered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    class Meta:
        ordering = ['-arrival_date']


class AnimalPhoto(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='animals/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.animal.name}"

    class Meta:
        ordering = ['-uploaded_at']


class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ use CustomUser
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    living_situation = models.TextField(help_text="Describe your living situation (house, apartment, etc.)")
    has_other_pets = models.BooleanField(default=False)
    other_pets_description = models.TextField(blank=True)
    has_children = models.BooleanField(default=False)
    children_ages = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Application for {self.animal.name} by {self.applicant.username}"

    class Meta:
        ordering = ['-application_date']
