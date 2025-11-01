from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team_list'),
    path('<int:profile_id>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('<int:profile_id>/build/', views.TeamBuildView.as_view(), name='team_build'),
    path('<int:profile_id>/update/', views.TeamUpdateView.as_view(), name='team_update'),
    path('<int:profile_id>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),
]
