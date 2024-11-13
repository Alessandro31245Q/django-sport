from django.contrib import admin
from django import forms
from .models import Category, Court, SportRating
import json

with open('Barrios_de_Cartagena.geojson', 'r') as f:
    data = json.load(f)

barrios = [feature['properties']['NOMBRE'] for feature in data['features']]

class CourtAdminForm(forms.ModelForm):
    barrio = forms.ChoiceField(choices=[(barrio, barrio) for barrio in barrios], label="Barrio")

    class Meta:
        model = Court
        fields = '__all__'

class CourtAdmin(admin.ModelAdmin):
    form = CourtAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'status', 'barrio', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status', 'barrio', 'is_featured')
    list_editable = ('status', 'is_featured')

class SportRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'court', 'score', 'created_at')  # Mostrar usuario, cancha, calificación y fecha
    search_fields = ('user__username', 'court__title')  # Puedes buscar por usuario o cancha
    list_filter = ('score',)  # Filtro para las calificaciones
    list_editable = ('score',)  # Permite editar la calificación desde el admin

admin.site.register(Category)
admin.site.register(Court, CourtAdmin)
admin.site.register(SportRating, SportRatingAdmin)
