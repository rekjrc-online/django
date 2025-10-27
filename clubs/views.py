from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from profiles.models import Profile
from .models import Club
from .forms import ClubForm, ClubMemberFormSet, ClubLocationFormSet

class ClubListView(ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'

class ClubBuildView(View):
    template_name = 'clubs/club_build.html'
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        club, created = Club.objects.get_or_create(profile=profile)
        form = ClubForm(instance=club)
        member_formset = ClubMemberFormSet(instance=club)
        location_formset = ClubLocationFormSet(instance=club)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'member_formset': member_formset,
            'location_formset': location_formset
        })

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        club, created = Club.objects.get_or_create(profile=profile)
        form = ClubForm(request.POST, instance=club)
        member_formset = ClubMemberFormSet(request.POST, instance=club)
        location_formset = ClubLocationFormSet(request.POST, instance=club)
        if form.is_valid() and member_formset.is_valid() and location_formset.is_valid():
            form.save()
            member_formset.save()
            location_formset.save()
            return redirect('clubs:club_list')
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'member_formset': member_formset,
            'location_formset': location_formset
        })
