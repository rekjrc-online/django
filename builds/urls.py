from django.urls import path
from .views import (
    BuildDetailView,
    BuildCreateView,
    BuildUpdateView,
    BuildDeleteView,
)

urlpatterns = [
    path('<int:profile_id>/', BuildDetailView.as_view(), name='build_detail'),
    path('<int:profile_id>/create/', BuildCreateView.as_view(), name='build_create'),
    path('<int:profile_id>/edit/', BuildUpdateView.as_view(), name='build_update'),
    path('<int:profile_id>/delete/', BuildDeleteView.as_view(), name='build_delete'),
]
