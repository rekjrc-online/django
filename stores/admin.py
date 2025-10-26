from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'human')
    search_fields = ('name', 'profile__user__username', 'human__name')
    list_filter = ('profile', 'human')
