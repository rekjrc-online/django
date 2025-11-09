from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:profile_id>/build/', views.EventBuildView.as_view(), name='event_build'),
    path('<int:profile_id>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('<int:profile_id>/<int:event_id>/interest/add/', views.AddInterestView.as_view(), name='add_interest'),
    path('<int:profile_id>/<int:event_id>/interest/remove/', views.RemoveInterestView.as_view(), name='remove_interest'),
]
