from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views as post_views

urlpatterns = [
    path('', post_views.HomepageView.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('builds/', include('builds.urls')),
    path('clubs/', include('clubs.urls')),
    path('events/', include('events.urls')),
	path('humans/', include('humans.urls')),
    path('locations/', include('locations.urls')),
    path('posts/', include('posts.urls')),
    path('profiles/', include('profiles.urls')),
    path('races/', include('races.urls')),
    path('sponsors/', include('sponsors.urls')),
    path('stores/', include('stores.urls')),
    path('support/', include('support.urls')),
    path('teams/', include('teams.urls')),
    path('tracks/', include('tracks.urls')),
]

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
