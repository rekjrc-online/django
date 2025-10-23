from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from humans.models import Invitation
from .models import Post
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

class HomepageView(ListView):
    model = Post
    template_name = 'posts/homepage.html'
    context_object_name = 'posts'
    ordering = ['-insertdate']
    paginate_by = 5

    # ... keep get_context_data and post methods ...

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset. For AJAX requests, return empty list if page invalid.
        Must return exactly 4 values: paginator, page_obj, object_list, is_paginated
        """
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get('page', 1)

        try:
            page_obj = paginator.page(page_number)
            object_list = page_obj.object_list
        except (EmptyPage, PageNotAnInteger):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # AJAX: return empty list instead of 404
                page_obj = None
                object_list = []
                is_paginated = False
                return paginator, page_obj, object_list, is_paginated
            else:
                raise  # normal request still raises 404

        is_paginated = page_obj.has_other_pages()
        return paginator, page_obj, object_list, is_paginated

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # AJAX requests render only the posts partial
            return render(self.request, 'posts/post_list.html', {'posts': context['posts']})
        return super().render_to_response(context, **response_kwargs)