from django.views.generic import TemplateView
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
	path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:post_id>/reply/', views.PostReplyView.as_view(), name='post_reply'),
    path('<int:post_id>/like-ajax/', views.toggle_like_ajax, name='post_like_ajax'),
    path('<int:post_id>/replies/ajax/', views.PostRepliesAjax.as_view(), name='PostRepliesAjax'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]