from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'website')
    search_fields = ('name', 'profile__name')
    list_filter = ('profile',)
    ordering = ('name',)
