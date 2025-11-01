from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('human', 'displayname', 'profiletype', 'city', 'state', 'followers_count', 'following_count')
    search_fields = ('human__username', 'profiletype', 'displayname')
    list_filter = ('human', 'profiletype', 'state', 'displayname')

admin.site.register(Profile, ProfileAdmin)
