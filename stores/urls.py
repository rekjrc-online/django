from django.urls import path
from .views import *

urlpatterns = [
    path("", StoreListView.as_view(), name="store_list"),
    path("<int:profile_id>/build/", StoreBuildView.as_view(), name="store_build"),
    path("<int:profile_id>/delete/", StoreDeleteView.as_view(), name="store_delete"),
]