from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .models import Event, EventInterest
from .forms import EventForm, EventInterestForm

def event_list(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    events = Event.objects.filter(location__profile=profile).select_related('location').order_by('-eventdate')
    return render(request, 'events/event_list.html', {
        'profile': profile,
        'events': events,
    })

def event_detail(request, profile_id):
    """Show the details of the single event for this profile."""
    profile = get_object_or_404(Profile, id=profile_id)
    event = Event.objects.filter(profile=profile).first()
    if not event:
        messages.info(request, 'No event found for this profile. Create one first.')
        return redirect('events:event_build', profile_id=profile.id)
    return render(request, 'events/event_detail.html', {
        'profile': profile,
        'event': event,
    })

@login_required
def event_build(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    existing_event = Event.objects.filter(profile=profile).first()
    if existing_event:
        return redirect('events:event_update', profile_id=profile.id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.profile = profile
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', profile_id=profile.id)
    else:
        form = EventForm()
    return render(request, 'events/event_build.html', {
        'form': form,
        'profile': profile,
    })

@login_required
def event_update(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    event = get_object_or_404(Event, profile=profile)
    if not event:
        return redirect('events:event_build', profile_id=profile.id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail', profile_id=profile.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_update.html', {
        'form': form,
        'profile': profile,
        'event': event,
    })

@login_required
def event_delete(request, profile_id, event_id):
    profile = get_object_or_404(Profile, id=profile_id)
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events:event_list', profile_id=profile.id)
    return render(request, 'events/event_confirm_delete.html', {
        'event': event,
        'profile': profile,
    })

@login_required
def add_interest(request, profile_id, event_id):
    event = get_object_or_404(Event, id=event_id)
    EventInterest.objects.get_or_create(event=event, human=request.user)
    messages.success(request, f"You've shown interest in {event.profile.displayname}.")
    return redirect('events:event_list', profile_id=profile_id)

@login_required
def remove_interest(request, profile_id, event_id):
    event = get_object_or_404(Event, id=event_id)
    EventInterest.objects.filter(event=event, human=request.user).delete()
    messages.info(request, f"You are no longer marked as interested in {event.profile.displayname}.")
    return redirect('events:event_list', profile_id=profile_id)
