from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('<int:profile_id>/build/', views.TeamBuildView.as_view(), name='team_build'),
    path('', views.TeamListView.as_view(), name='team_list'),
]
