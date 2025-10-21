from django.urls import path
from . import views

urlpatterns = [
    # Example placeholder view
	path('create/', views.PostCreateView.as_view(), name='post-create'),
]
