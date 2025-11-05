from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse, get_object_or_404
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
        # Only show profiles owned by current user
        return Profile.objects.filter(human=self.request.user).order_by('profiletype', 'displayname')


class ProfileBuildView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profiles/profile_build.html'
    login_url = '/humans/login/'

    def form_valid(self, form):
        # Assign current human as owner
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


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'profile_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs['profile_id'])

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

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        if profile.human != self.request.user:
            return redirect('profiles:detail-profile', profile_id=profile.id)
        return profile

    def form_valid(self, form):
        profile = form.save()
        return redirect('profiles:profiles-list')


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profiles/confirm_delete.html'
    pk_url_kwarg = 'profile_id'
    login_url = '/humans/login/'

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        if profile.human != self.request.user:
            return redirect('profiles:detail-profile', profile_id=profile.id)
        return profile

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.human != request.user:
            return redirect('profiles:detail-profile', profile_id=profile.id)

        # Soft-delete
        profile.deleted = True
        profile.save()
        return redirect('/profiles/')
