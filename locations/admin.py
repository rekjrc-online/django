from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'profile', 'website')
    search_fields = ('name', 'city', 'state', 'profile__name')
    list_filter = ('profile', 'city', 'state',)
    ordering = ('name',)
