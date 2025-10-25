from django.urls import path
from . import views

urlpatterns = [
    # Example placeholder view
	path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/reply/', views.PostReplyView.as_view(), name='post_reply'),
    path('<int:post_id>/like-ajax/', views.toggle_like_ajax, name='post_like_ajax'),
]
