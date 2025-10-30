from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path("", views.ClubListView.as_view(), name="club_list"),
    path("<int:profile_id>/", views.ClubDetailView.as_view(), name="club_detail"),
    path("<int:profile_id>/build/", views.ClubBuildView.as_view(), name="club_build"),
    path("<int:profile_id>/update/", views.ClubUpdateView.as_view(), name="club_update"),
    path("<int:profile_id>/delete/", views.ClubDeleteView.as_view(), name="club_delete"),
]