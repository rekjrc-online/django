from django.urls import path
from locations.views import LocationListView, LocationBuildView, LocationDetailView, LocationUpdateView, LocationDeleteView

app_name = 'locations'

urlpatterns = [
    path('', LocationListView.as_view(), name='location_list'),
    path('<int:profile_id>/', LocationDetailView.as_view(), name='location_detail'),
    path('<int:profile_id>/build/', LocationBuildView.as_view(), name='location_build'),
    path('<int:profile_id>/update/', LocationUpdateView.as_view(), name='location_update'),
    path('<int:profile_id>/delete/', LocationDeleteView.as_view(), name='location_delete'),
]
