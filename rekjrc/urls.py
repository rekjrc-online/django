from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views as post_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_views.HomepageView.as_view(), name='homepage'),
    path('builds/', include('builds.urls')),
    path('clubs/', include('clubs.urls')),
    path('events/', include('events.urls')),
	path('humans/', include('humans.urls')),
    path('locations/', include('locations.urls')),
    path('posts/', include('posts.urls')),
    path('profiles/', include('profiles.urls')),
    path('races/', include('races.urls')),
    path('stores/', include('stores.urls')),
    path('teams/', include('teams.urls')),
    path('tracks/', include('tracks.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
