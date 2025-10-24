from django.views.generic import ListView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

class PostReplyView(LoginRequiredMixin, CreateView):
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
    template_name = 'posts/homepage.html'
    context_object_name = 'posts'
    ordering = ['-insertdate']
    paginate_by = 5
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
