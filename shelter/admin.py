from django.contrib import admin
from .models import AnimalType, Breed, Animal, AdoptionApplication, AnimalPhoto

# Register your models here.


class AnimalPhotoInline(admin.TabularInline):
    model = AnimalPhoto
    extra = 5  # Number of empty photo upload slots shown
    fields = ('photo', 'uploaded_at')
    readonly_fields = ('uploaded_at',)  

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name','animal_type','breed','age','gender','weight','status','arrival_date') 
    list_filter = ('animal_type', 'status', 'gender', 'is_vaccinated','is_spayed_neutered') 
    search_fields = ('name', 'description')
    readonly_fields = ('arrival_date', 'adoption_date')
    inlines = [AnimalPhotoInline]  
    fieldsets = (
        (None, {
            'fields': ('name', 'animal_type', 'breed', 'gender', 'age', 'weight', 'description')
        }),
        ('Status', {
            'fields': ('status', 'arrival_date', 'adoption_date')
        }),
        ('Medical Information', {
            'fields': ('is_vaccinated', 'is_spayed_neutered', 'special_needs')
        }),
    )



class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('animal','applicant','status','application_date')
    list_filter= ('status','application_date')
    search_fields = ('animal__name','applicant__username','living_situation')
    raw_id_fields = ('animal', 'applicant')


admin.site.register(AnimalType)
admin.site.register(Breed)
admin.site.register(AnimalPhoto)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(AdoptionApplication, AdoptionApplicationAdmin)