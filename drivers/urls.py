# drivers/urls.py
from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('', views.DriverListView.as_view(), name='driver_list'),
    path('<int:profile_id>/update/', views.DriverUpdateView.as_view(), name='driver_update'),
]
