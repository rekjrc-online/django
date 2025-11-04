from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Profile
from .forms import ProfileEditForm, ProfileCreateForm

import logging
logger = logging.getLogger(__name__)

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
        form.instance.human = self.request.user
        self.object = form.save()
        return redirect(self.get_success_url())
    def get_success_url(self):
        match self.object.profiletype:
            case 'BUILD':
                return reverse('builds:build_build', kwargs={'profile_id': self.object.pk})
            case 'CLUB':
                return reverse('clubs:club_build', kwargs={'profile_id': self.object.pk})
            case 'EVENT':
                return reverse('events:event_build', kwargs={'profile_id': self.object.pk})
            case 'LOCATION':
                return reverse('locations:location_build', kwargs={'profile_id': self.object.pk})
            case 'RACE':
                return reverse('races:race_build', kwargs={'profile_id': self.object.pk})
            case 'STORES':
                return reverse('stores:store_build', kwargs={'profile_id': self.object.pk})
            case 'TEAM':
                return reverse('teams:team_build', kwargs={'profile_id': self.object.pk})
            case 'TRACK':
                return reverse('tracks:track_build', kwargs={'profile_id': self.object.pk})
            case _:
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
