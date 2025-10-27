from django.urls import path
from . import views

app_name = 'tracks'

urlpatterns = [
    path('<int:profile_id>/build/', views.TrackBuildView.as_view(), name='track_build'),
    path('', views.TrackListView.as_view(), name='track_list'),
]
