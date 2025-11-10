from django.urls import path
from . import views

app_name = 'races'

urlpatterns = [
    path("", views.RaceListView.as_view(), name="race_list"),
    path("<int:profile_id>/build/", views.RaceBuildView.as_view(), name="race_build"),
    path("<int:profile_id>/delete/", views.RaceDeleteView.as_view(), name="race_delete"),
    path("<int:profile_id>/join/", views.RaceJoinView.as_view(), name="race_join"),
    path("<int:race_id>/upload-lapmonitor/", views.LapMonitorUploadView.as_view(), name="lapmonitor_upload"),
    path("<int:profile_id>/drag-race/<int:race_id>/", views.RaceDragRaceView.as_view(), name="race_drag_race"),
    path("<int:profile_id>/crawler-comp/<int:race_id>/", views.RaceCrawlerCompView.as_view(), name="race_crawler_comp"),
    path("<int:profile_id>/crawler-comp/<int:race_id>/racedriver/<int:racedriver_id>/run/", views.RaceCrawlerRunView.as_view(), name="race_crawler_run"),
]