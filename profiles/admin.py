from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('human', 'displayname', 'profiletype', 'followers_count', 'following_count')
    search_fields = ('human__username', 'profiletype', 'displayname', 'location')
    list_filter = ('human', 'profiletype', 'location', 'displayname')

admin.site.register(Profile, ProfileAdmin)
