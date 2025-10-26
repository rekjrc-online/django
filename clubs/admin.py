from django.contrib import admin
from .models import Club, ClubLocation, ClubMember

class ClubMemberInline(admin.TabularInline):
    model = ClubMember
    extra = 1
    autocomplete_fields = ('human',)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')
    search_fields = ('name', 'profile__username')
    ordering = ('name',)
    inlines = [ClubMemberInline]

@admin.register(ClubLocation)
class ClubLocationAdmin(admin.ModelAdmin):
    list_display = ('club', 'location')
    search_fields = ('club__name', 'location__name')
    ordering = ('club__name', 'location__name')

@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('club', 'human')
    search_fields = ('club__name', 'role')
    list_filter = ('club', 'role')
    ordering = ('club__name', 'role')
