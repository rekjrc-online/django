from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from .models import Post
from .forms import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm        # <-- use the custom form
    template_name = 'posts/post_form.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['human'] = self.request.user  # pass logged-in user to form
        return kwargs

    def form_valid(self, form):
        form.instance.human_id = self.request.user  # automatically set author
        return super().form_valid(form)

class HomepageView(ListView):
    model = Post
    template_name = 'posts/homepage.html'
    context_object_name = 'posts'
    ordering = ['-insertdate']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['post_form'] = PostForm(human=self.request.user)
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