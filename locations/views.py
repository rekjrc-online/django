from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from profiles.models import Profile
from .models import Location
from .forms import LocationForm

class LocationDetailView(DetailView):
    model = Location
    template_name = 'locations/location_detail.html'
    context_object_name = 'location'
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return Location.objects.filter(profile=profile).first()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        context['profile'] = profile
        return context

class LocationBuildView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    def dispatch(self, request, *args, **kwargs):
        # If a location already exists for this profile, redirect to update
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        existing_location = Location.objects.filter(profile=profile).first()
        if existing_location:
            return redirect('locations:location-update', profile_id=profile.id)
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return context
    def form_valid(self, form):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        form.instance.profile = profile
        if hasattr(self.request.user, 'human'):
            form.instance.human = self.request.user.human
        messages.success(self.request, "Location created successfully.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('locations:location-detail', kwargs={'profile_id': self.kwargs['profile_id']})

class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return get_object_or_404(Location, profile=profile)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        context['is_update'] = True
        return context
    def form_valid(self, form):
        messages.success(self.request, "Location updated successfully.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('locations:location-detail', kwargs={'profile_id': self.kwargs['profile_id']})

class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'locations/location_confirm_delete.html'
    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return get_object_or_404(Location, profile=profile)
    def get_success_url(self):
        messages.success(self.request, "Location deleted successfully.")
        return reverse_lazy('profiles:profile-detail', kwargs={'pk': self.kwargs['profile_id']})
