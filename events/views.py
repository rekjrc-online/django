from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from profiles.models import Profile
from .models import Event, EventInterest
from .forms import EventForm

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    login_url = '/humans/login/'
    def get_queryset(self):
        return Event.objects.select_related('profile', 'location').order_by('-eventdate')

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    login_url = '/humans/login/'
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        event = Event.objects.filter(profile=profile).first()
        return event
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        event = self.get_object()
        if not event:
            messages.info(request, 'No event found for this profile. Create one first.')
            return redirect('events:event_build', profile_id=profile.id)
        self.object = event
        context = self.get_context_data(event=event, profile=profile)
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return context

class EventBuildView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_build.html'
    login_url = '/humans/login/'
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        if Event.objects.filter(profile=profile).exists():
            return redirect('events:event_update', profile_id=profile.id)
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        form.instance.profile = profile
        form.save()
        return redirect('events:event_detail', profile_id=profile.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return context

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_update.html'
    login_url = '/humans/login/'
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return get_object_or_404(Event, profile=profile)
    def form_valid(self, form):
        event = form.save()
        return redirect('events:event_detail', profile_id=event.profile.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    login_url = '/humans/login/'
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return get_object_or_404(Event, profile=profile)
    def get_success_url(self):
        return reverse_lazy('events:event_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        return context

class AddInterestView(LoginRequiredMixin, View):
    login_url = '/humans/login/'
    def post(self, request, profile_id, event_id):
        event = get_object_or_404(Event, id=event_id)
        EventInterest.objects.get_or_create(event=event, human=request.user)
        return redirect('events:event_detail', profile_id=profile_id)

class RemoveInterestView(LoginRequiredMixin, View):
    login_url = '/humans/login/'
    def post(self, request, profile_id, event_id):
        event = get_object_or_404(Event, id=event_id)
        EventInterest.objects.filter(event=event, human=request.user).delete()
        return redirect('events:event_detail', profile_id=profile_id)
