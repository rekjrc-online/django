from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('<int:profile_id>/build', views.build_location, name='build'),
]
