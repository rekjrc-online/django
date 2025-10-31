from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_list_create, name='profiles-list-create'),
    path('<int:pk>/', views.detail_profile, name='detail-profile'),
    path('<int:pk>/update/', views.update_profile, name='update-profile'),
    path('<int:pk>/delete/', views.delete_profile, name='delete-profile'),
]
