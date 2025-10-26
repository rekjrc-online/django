from django.contrib import admin
from .models import Event, EventInterest

class EventInterestInline(admin.TabularInline):
    model = EventInterest
    extra = 1
    autocomplete_fields = ('human',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'eventdate', 'multiday')
    list_filter = ('multiday', 'location')
    search_fields = ('name', 'location__name')
    ordering = ('-eventdate',)
    inlines = [EventInterestInline]

@admin.register(EventInterest)
class EventInterestAdmin(admin.ModelAdmin):
    list_display = ('event', 'human', 'note', 'created_at')
    list_filter = ('event',)
    search_fields = ('event__name', 'human__first_name', 'human__last_name', 'note')
    ordering = ('-created_at',)
    autocomplete_fields = ('human', 'event')
