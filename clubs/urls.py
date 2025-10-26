from django.urls import path
from .views import (
    ClubRegisterView,
    ClubLoginView,
    ClubLogoutView,
    ClubUpdateView,
    GenerateInvitationView,
    VerifyInvitationView,
)
urlpatterns = [
    path('register/', ClubRegisterView.as_view(), name='register'),
    path('login/', ClubLoginView.as_view(), name='login'),
    path('logout/', ClubLogoutView.as_view(), name='logout'),
    path('update/', ClubUpdateView.as_view(), name='update'),
    path('generate-invitation/', GenerateInvitationView.as_view(), name='generate-invitation'),
    path('verify-invitation/', VerifyInvitationView.as_view(), name='verify-invitation'),
]
