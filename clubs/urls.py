from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path('', views.ClubListView.as_view(), name='club_list'),
    path('<int:profile_id>/build/', views.ClubBuildView.as_view(), name='club_build'),
]
