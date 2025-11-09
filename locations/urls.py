from django.urls import path
from locations.views import LocationListView, LocationBuildView, LocationDeleteView

app_name = 'locations'

urlpatterns = [
    path('', LocationListView.as_view(), name='location_list'),
    path('<int:profile_id>/build/', LocationBuildView.as_view(), name='location_build'),
    path('<int:profile_id>/delete/', LocationDeleteView.as_view(), name='location_delete'),
]
