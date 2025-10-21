from django.urls import path
from .views import HumanRegisterView, HumanLoginView, HumanLogoutView, HumanUpdateView

urlpatterns = [
    path('register/', HumanRegisterView.as_view(), name='register'),
    path('login/', HumanLoginView.as_view(), name='login'),
    path('logout/', HumanLogoutView.as_view(), name='logout'),
    path('update/', HumanUpdateView.as_view(), name='update'),
]
