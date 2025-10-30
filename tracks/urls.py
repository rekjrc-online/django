from django.urls import path
from . import views

app_name = 'tracks'

urlpatterns = [
    path("", views.TrackListView.as_view(), name="track_list"),
    path("<int:profile_id>/", views.TrackDetailView.as_view(), name="track_detail"),
    path("<int:profile_id>/build/", views.TrackBuildView.as_view(), name="track_build"),
    path("<int:profile_id>/update/", views.TrackUpdateView.as_view(), name="track_update"),
    path("<int:profile_id>/delete/", views.TrackDeleteView.as_view(), name="track_delete"),
]