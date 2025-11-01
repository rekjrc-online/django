from django.urls import path
from locations.views import LocationBuildView, LocationDetailView, LocationUpdateView, LocationDeleteView

app_name = 'locations'

urlpatterns = [
    path('<int:profile_id>', LocationDetailView.as_view(), name='location-detail'),
    path('<int:profile_id>/build', LocationBuildView.as_view(), name='location-build'),
    path('<int:profile_id>/update', LocationUpdateView.as_view(), name='location-update'),
    path('<int:profile_id>/delete', LocationDeleteView.as_view(), name='location-delete'),
]
