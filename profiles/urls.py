from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_list_create, name='profiles-list-create'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('<int:pk>/view/', views.view_profile, name='view-profile'),
    path('<int:pk>/edit/', views.edit_profile, name='edit-profile'),
    path('<int:pk>/delete/', views.delete_profile, name='delete-profile'),
]
