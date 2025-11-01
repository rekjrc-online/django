from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Post, PostLike
from .forms import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = '/'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['human'] = self.request.user
        return kwargs
    def form_valid(self, form):
        form.instance.human_id = self.request.user
        return super().form_valid(form)

class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.select_related('human_id', 'profile_id'),
            pk=self.kwargs['post_id']
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        # Determine if the main post is liked by the user
        post.liked_by_user = (
            self.request.user.is_authenticated
            and post.likes.filter(human=self.request.user).exists()
        )
        context['likes'] = post.likes.select_related('human').all()
        # Paginate replies
        replies_qs = post.replies.select_related('human_id', 'profile_id').order_by('-insertdate')
        paginator = Paginator(replies_qs, 5)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        # Add like state and counts to replies
        if self.request.user.is_authenticated:
            for reply in page_obj:
                reply.liked_by_user = reply.likes.filter(human=self.request.user).exists()
                reply.LikeCount = reply.likes.count()
                reply.CommentCount = reply.replies.count()
        # AJAX support
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            replies_html = render(
                self.request,
                'posts/post_replies.html',
                {'replies': page_obj}
            ).content.decode('utf-8')
            return JsonResponse({
                'html': replies_html,
                'has_next': page_obj.has_next()
            })
        context['replies'] = page_obj
        context['post'] = post
        return context

class PostRepliesAjax(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        replies_qs = post.replies.select_related('profile_id', 'human_id').order_by('-insertdate')
        paginator = Paginator(replies_qs, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        if request.user.is_authenticated:
            for reply in page_obj:
                reply.liked_by_user = reply.likes.filter(human=request.user).exists()
                reply.LikeCount = reply.likes.count()
                reply.CommentCount = reply.replies.count()
        html = render(
            request,
            'posts/_reply_item.html',
            {'posts': page_obj}
        ).content.decode('utf-8')
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next()
        })

class PostReplyView(LoginRequiredMixin, CreateView):
    login_url = '/humans/login/'
    model = Post
    form_class = PostForm
    template_name = 'posts/post_reply.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['human'] = self.request.user
        return kwargs
    def form_valid(self, form):
        human = self.request.user
        parent_post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.human_id = human     # <-- must match your model field exactly
        form.instance.parent = parent_post
        return super().form_valid(form)
    def get_success_url(self):
        return ('/')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        return context

class HomepageView(ListView):
    model = Post
    template_name = 'homepage.html'
    context_object_name = 'posts'
    ordering = ['-insertdate']
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            for post in context['posts']:
                post.liked_by_user = post.likes.filter(human=self.request.user).exists()
        return context
    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
            object_list = page_obj.object_list
        except (EmptyPage, PageNotAnInteger):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                page_obj = None
                object_list = []
                is_paginated = False
                return paginator, page_obj, object_list, is_paginated
            else:
                raise
        is_paginated = page_obj.has_other_pages()
        return paginator, page_obj, object_list, is_paginated
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'posts/post_list.html', {'posts': context['posts']})
        return super().render_to_response(context, **response_kwargs)

@login_required
def toggle_like(request, post_id):
    human = request.user.human
    post = get_object_or_404(Post, id=post_id)
    like, created = PostLike.objects.get_or_create(human=human, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def toggle_like_ajax(request, post_id):
    try:
        human = request.user
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(human=human, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count(),
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)