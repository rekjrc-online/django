from django.urls import path
from . import views

app_name = 'builds'

urlpatterns = [
    path("", views.BuildListView.as_view(), name="build_list"),
    path('<int:profile_id>/build/', views.BuildBuildView.as_view(), name='build_build'),
    path('<int:profile_id>/delete/', views.BuildDeleteView.as_view(), name='build_delete'),
]
