from django.contrib import admin
from .models import TrackType, Track, TrackAttributeEnum, TrackAttribute

@admin.register(TrackType)
class TrackTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'track_type', 'location')
    list_filter = ('track_type', 'location')
    search_fields = ('name', 'track_type__name', 'location__name')
    ordering = ('name',)

@admin.register(TrackAttributeEnum)
class TrackAttributeEnumAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(TrackAttribute)
class TrackAttributeAdmin(admin.ModelAdmin):
    list_display = ('track', 'attribute_type', 'value')
    list_filter = ('attribute_type', 'track')
    search_fields = ('track__name', 'attribute_type__name', 'value')
    ordering = ('track',)
