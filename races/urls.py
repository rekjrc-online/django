from django.urls import path
from . import views

app_name = 'races'

urlpatterns = [
    path("", views.RaceListView.as_view(), name="race_list"),
    path("<int:profile_id>/", views.RaceDetailView.as_view(), name="race_detail"),
    path("<int:profile_id>/build/", views.RaceBuildView.as_view(), name="race_build"),
    path("<int:profile_id>/update/", views.RaceUpdateView.as_view(), name="race_update"),
    path("<int:profile_id>/delete/", views.RaceDeleteView.as_view(), name="race_delete"),
    path("<int:profile_id>/join/", views.RaceJoinView.as_view(), name="race_join"),
]