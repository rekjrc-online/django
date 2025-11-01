from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfilesListView.as_view(), name='profiles-list'),
    path('<int:profile_id>/', views.ProfileDetailView.as_view(), name='detail-profile'),
    path('<int:profile_id>/update/', views.ProfileUpdateView.as_view(), name='update-profile'),
    path('<int:profile_id>/delete/', views.ProfileDeleteView.as_view(), name='delete-profile'),
]
