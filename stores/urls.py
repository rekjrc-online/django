from django.urls import path
from .views import *

urlpatterns = [
    path('build/', StoreBuildView.as_view(), name='register'),
    path('build/update/', StoreUpdateView.as_view(), name='update'),
]
