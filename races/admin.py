from django.contrib import admin
from .models import Race

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_id')
    list_filter = ('event_id',)
    search_fields = ('event_id__name',)
    ordering = ('event_id',)
