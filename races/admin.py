from django.contrib import admin
from .models import Race, RaceAttributeEnum, RaceAttribute

# Inline for RaceAttribute to edit directly within Race
class RaceAttributeInline(admin.TabularInline):
    model = RaceAttribute
    extra = 1  # number of empty rows to show
    autocomplete_fields = ['attribute']
    fields = ['attribute', 'value']

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'human', 'event', 'race_type', 'location', 'club', 'team']
    list_filter = ['event', 'race_type', 'location', 'club', 'team']
    search_fields = ['profile__user__username', 'human__username', 'event__name']
    autocomplete_fields = ['profile', 'human', 'event', 'location', 'club', 'team']
    inlines = [RaceAttributeInline]

@admin.register(RaceAttributeEnum)
class RaceAttributeEnumAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(RaceAttribute)
class RaceAttributeAdmin(admin.ModelAdmin):
    list_display = ['race', 'attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['value', 'race__profile__user__username', 'race__event__name']
    autocomplete_fields = ['race', 'attribute']
