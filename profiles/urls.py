from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_list_create, name='profiles-list-create'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('<int:pk>/edit/', views.edit_profile, name='edit-profile'),
]
