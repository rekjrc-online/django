from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views as post_views

urlpatterns = [
    path('', post_views.HomepageView.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
	path('humans/', include('humans.urls')),
    path('profiles/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
    path('builds/', include('builds.urls')),
    path('stores/', include('stores.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
