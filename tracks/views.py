from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from profiles.models import Profile
from .models import Track
from .forms import TrackForm, TrackAttributeFormSet

class TrackListView(ListView):
    model = Track
    template_name = 'tracks/track_list.html'
    context_object_name = 'tracks'

class TrackBuildView(View):
    template_name = 'tracks/track_build.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        track = Track()
        form = TrackForm(instance=track)
        attribute_formset = TrackAttributeFormSet(instance=track)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'attribute_formset': attribute_formset,
        })

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        track = Track()
        form = TrackForm(request.POST, instance=track)
        attribute_formset = TrackAttributeFormSet(request.POST, instance=track)

        if form.is_valid() and attribute_formset.is_valid():
            track = form.save()
            attribute_formset.instance = track
            attribute_formset.save()
            return redirect('tracks:track_list')

        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'attribute_formset': attribute_formset,
        })
