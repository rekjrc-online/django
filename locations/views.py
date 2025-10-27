from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from profiles.models import Profile
from .models import Location
from .forms import LocationForm

def build_location(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    existing_location = Location.objects.filter(profile=profile).first()
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=existing_location)
        if form.is_valid():
            location = form.save(commit=False)
            location.profile = profile
            location.save()
            messages.success(request, 'Location saved successfully.')
            return redirect('locations:build', profile_id=profile.id)
    else:
        form = LocationForm(instance=existing_location)
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'locations/location_build.html', context)