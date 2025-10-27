from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('<int:profile_id>/', views.event_list, name='event_list'),
    path('<int:profile_id>/build/', views.event_build, name='event_build'),
    path('<int:profile_id>/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('<int:profile_id>/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('<int:profile_id>/<int:event_id>/interest/add/', views.add_interest, name='add_interest'),
    path('<int:profile_id>/<int:event_id>/interest/remove/', views.remove_interest, name='remove_interest'),
]
