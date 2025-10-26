from django.contrib import admin
from .models import Team, TeamMember

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    autocomplete_fields = ('human',)
    fields = ('human', 'role')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'website')
    search_fields = ('name', 'profile__user__username')
    inlines = [TeamMemberInline]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('human', 'Team', 'role')
    search_fields = ('human__name', 'Team__name', 'role')
    list_filter = ('Team', 'role')
