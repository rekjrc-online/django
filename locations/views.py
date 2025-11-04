from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from profiles.models import Profile
from .models import Location
from .forms import LocationForm

class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'locations/location_list.html'
    context_object_name = 'locations'
    login_url = '/humans/login/'
    def get_queryset(self):
        return (Location.objects.select_related('profile').order_by('profile__displayname'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    template_name = 'locations/location_detail.html'
    context_object_name = 'location'
    login_url = '/humans/login/'
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        location = Location.objects.filter(profile=profile).first()
        return location
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        location = self.get_object()
        if not location:
            messages.info(request, 'No location found for this profile. Create one first.')
            return redirect('locations:location_build', profile_id=profile.id)
        self.object = location  
        context = self.get_context_data(object=self.object, profile=profile)
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return context

class LocationBuildView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    login_url = '/humans/login/'
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        if Location.objects.filter(profile=profile).exists():
            return redirect('locations:location_update', profile_id=profile.id)
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        context['is_update'] = False
        return context
    def form_valid(self, form):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        form.instance.profile = profile
        if hasattr(self.request.user, 'human'):
            form.instance.human = self.request.user.human
        self.object = form.save()
        return redirect('locations:location_detail', profile_id=profile.id)

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    login_url = '/humans/login/'
    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return get_object_or_404(Location, profile=profile)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        context['profile'] = profile
        context['is_update'] = True
        return context
    def form_valid(self, form):
        self.object = form.save()
        return redirect('locations:location_detail', profile_id=self.kwargs['profile_id'])

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'locations/location_confirm_delete.html'
    login_url = '/humans/login/'
    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return get_object_or_404(Location, profile=profile)
    def get_success_url(self):
        return reverse_lazy('locations:location_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return context
