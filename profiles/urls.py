from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_list_create, name='profiles-list-create'),
    path('<int:profile_id>/', views.detail_profile, name='detail-profile'),
    path('<int:profile_id>/update/', views.update_profile, name='update-profile'),
    path('<int:profile_id>/delete/', views.delete_profile, name='delete-profile'),
]
