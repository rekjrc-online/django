from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView
from profiles.models import Profile
from .models import Track
from .forms import TrackForm, TrackAttributeFormSet

# List all tracks
class TrackListView(ListView):
    model = Track
    template_name = 'tracks/track_list.html'
    context_object_name = 'tracks'


# Show details for a track
class TrackDetailView(View):
    template_name = 'tracks/track_detail.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        track = get_object_or_404(Track, profile=profile)

        # Ownership check
        if profile.human != request.user:
            return redirect('tracks:track_list')

        return render(request, self.template_name, {
            'profile': profile,
            'track': track,
        })


# Build (create) a new track
class TrackBuildView(View):
    template_name = 'tracks/track_build.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        # Ownership check
        if profile.human != request.user:
            return redirect('tracks:track_list')

        # Redirect if this profile already has a track
        if Track.objects.filter(profile=profile).exists():
            return redirect('tracks:track_update', profile_id=profile_id)

        form = TrackForm(initial={'human': profile.human, 'profile': profile})
        return render(request, self.template_name, {'profile': profile, 'form': form})

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        # Ownership check
        if profile.human != request.user:
            return redirect('tracks:track_list')

        form = TrackForm(request.POST, initial={'human': profile.human, 'profile': profile})
        if form.is_valid():
            track = form.save(commit=False)
            track.human = profile.human
            track.profile = profile
            track.save()
            return redirect('tracks:track_update', profile_id=profile_id)

        return render(request, self.template_name, {'profile': profile, 'form': form})


# Update an existing track (with attributes)
class TrackUpdateView(View):
    template_name = 'tracks/track_update.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        # Ownership check
        if profile.human != request.user:
            return redirect('tracks:track_list')

        track = get_object_or_404(Track, profile=profile)
        form = TrackForm(instance=track)
        attribute_formset = TrackAttributeFormSet(instance=track)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'attribute_formset': attribute_formset,
        })

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        # Ownership check
        if profile.human != request.user:
            return redirect('tracks:track_list')

        track = get_object_or_404(Track, profile=profile)
        form = TrackForm(request.POST, request.FILES, instance=track)
        attribute_formset = TrackAttributeFormSet(request.POST, request.FILES, instance=track)

        if form.is_valid() and attribute_formset.is_valid():
            # Save Track
            track = form.save(commit=False)
            track.human = profile.human
            track.profile = profile
            track.save()

            # Save attributes (existing + new)
            attribute_formset.save()

            return redirect('tracks:track_list')

        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'attribute_formset': attribute_formset,
        })


# Delete a track
class TrackDeleteView(DeleteView):
    model = Track
    template_name = 'tracks/track_confirm_delete.html'

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        profile = get_object_or_404(Profile, id=profile_id)

        # Ownership check
        if profile.human != self.request.user:
            return redirect('tracks:track_list')

        return get_object_or_404(Track, profile=profile)

    def get_success_url(self):
        return reverse('tracks:track_list')
