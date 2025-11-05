from django.contrib import admin
from .models import Race, RaceAttributeEnum, RaceAttribute, LapMonitorResult, RaceDriver

# Inline for RaceAttribute to edit directly within Race
class RaceAttributeInline(admin.TabularInline):
    model = RaceAttribute
    extra = 1  # number of empty rows to show
    autocomplete_fields = ['attribute']
    fields = ['attribute', 'value']

@admin.register(LapMonitorResult)
class LapMonitorResultAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'driver_name', 'lap_index', 'lap_duration', 'lap_kind')
    search_fields = ('session_name', 'driver_name', 'session_id', 'driver_id')
    list_filter = ('session_kind', 'lap_kind')
    ordering = ('session_date', 'driver_name', 'lap_index')

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'human', 'event', 'race_type',
                    'location', 'track', 'club', 'team', 'transponder']
    list_filter = ['event', 'race_type', 'location', 'track', 'club', 'team']
    search_fields = ['profile__user__username', 'human__username', 'event__name']
    autocomplete_fields = ['profile', 'human', 'event', 'location', 'track', 'club', 'team']
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

@admin.register(RaceDriver)
class RaceDriverAdmin(admin.ModelAdmin):
    list_display = ('race', 'human_name', 'driver_name', 'model_name')
    list_filter = ('race',)
    search_fields = (
        'human__first_name',
        'human__last_name',
        'driver__displayname',
        'model__displayname',
        'race__profile__displayname',)
    @admin.display(description='Human')
    def human_name(self, obj):
        if obj.human:
            return f"{obj.human.first_name} {obj.human.last_name}"
        return "-human-"
    @admin.display(description='Driver')
    def driver_name(self, obj):
        return obj.driver.displayname if obj.driver else "-driver-"
    @admin.display(description='Model')
    def model_name(self, obj):
        return obj.model.displayname if obj.model else "-model-"
