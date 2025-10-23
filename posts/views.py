from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
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
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None

        # Calculate hours_remaining
        recent_invite = Invitation.objects.filter(
            Q(from_human=user) | Q(to_human=user),
            insertdate__gte=timezone.now() - timedelta(hours=72)
        ).order_by('-insertdate').first()

        hours_remaining = 0
        if recent_invite:
            elapsed = timezone.now() - recent_invite.insertdate
            hours_remaining = max(0, 72 - elapsed.total_seconds() / 3600)

        context['hours_remaining'] = hours_remaining
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST, request.FILES, human=request.user)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.human_id = request.user
            new_post.save()
        return redirect('/')