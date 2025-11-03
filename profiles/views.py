from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Profile
from .forms import ProfileEditForm, ProfileCreateForm

class ProfilesListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profiles.html'
    context_object_name = 'profiles'
    login_url = '/humans/login/'
    def get_queryset(self):
        return Profile.objects.filter(human=self.request.user).order_by('profiletype', 'displayname')

class ProfileBuildView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profiles/profile_build.html'
    login_url = '/humans/login/'
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            return redirect('profiles:detail-profile', profile_id=request.user.profile.id)
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        messages.success(self.request, "Profile created successfully!")
        return redirect(self.get_success_url())
    def get_success_url(self):
        return reverse('profiles:detail-profile', kwargs={'profile_id': self.object.pk})

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'profile_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_with_images'] = self.object.posts.filter(image__isnull=False).exclude(image='')
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'profiles/profile_edit.html'
    pk_url_kwarg = 'profile_id'
    login_url = '/humans/login/'
    def get_queryset(self):
        return Profile.objects.filter(human=self.request.user)
    def form_valid(self, form):
        form.save()
        return redirect('profiles:profiles-list')

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profiles/confirm_delete.html'
    pk_url_kwarg = 'profile_id'
    login_url = '/humans/login/'
    def get_queryset(self):
        return Profile.objects.filter(human=self.request.user)
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.deleted = True
        profile.save()
        return redirect('/profiles/')
