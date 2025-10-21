from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
	list_display = ('human', 'profile', 'short_content', 'insertdate', 'deleted')
	search_fields = ('human__username', 'profile__displayname', 'content')
	list_filter = (
		('human_id', RelatedOnlyFieldListFilter),
		('profile_id', RelatedOnlyFieldListFilter),
		'deleted',
		'insertdate' )
	autocomplete_fields = ('profile_id', 'human_id')

	def human(self, obj):
		return obj.human_id.username
	human.short_description = 'Human'

	def profile(self, obj):
		return obj.profile_id.displayname
	profile.short_description = 'Profile'

	def short_content(self, obj):
		return obj.content[:50]
	short_content.short_description = 'Content'


admin.site.register(Post, PostAdmin)
