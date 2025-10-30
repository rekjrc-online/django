from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView
from django.db import transaction
from profiles.models import Profile
from .models import Club
from .forms import ClubForm, ClubLocationFormSet

# List all clubs
class ClubListView(ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'

# Detail view for a single club
class ClubDetailView(View):
    template_name = 'clubs/club_detail.html'
    def get(self, request, profile_id):
        club = get_object_or_404(Club, profile__id=profile_id)
        locations = club.clubs.all()  # ClubLocation
        members = club.members.all()  # ClubMember
        return render(request, self.template_name, {
            'club': club,
            'locations': locations,
            'members': members,
        })

class ClubBuildView(View):
    template_name = 'clubs/club_build.html'
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        club = Club.objects.filter(profile=profile).first()
        if club:
            return redirect('clubs:club_update', profile_id=profile_id)
        form = ClubForm()
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
        })
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.profile = profile
            club.save()
            return redirect('clubs:club_detail', profile_id=profile_id)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
        })

class ClubUpdateView(View):
    template_name = 'clubs/club_update.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        club = get_object_or_404(Club, profile=profile)
        form = ClubForm(instance=club)
        location_formset = ClubLocationFormSet(instance=club)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'location_formset': location_formset,
        })

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        club = get_object_or_404(Club, profile=profile)
        form = ClubForm(request.POST, instance=club)
        location_formset = ClubLocationFormSet(request.POST, instance=club)

        if form.is_valid() and location_formset.is_valid():
            with transaction.atomic():
                club = form.save()
                location_formset.instance = club
                location_formset.save()
            return redirect('clubs:club_detail', profile_id=profile_id)

        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'location_formset': location_formset,
        })
# Delete a club
class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'clubs/club_confirm_delete.html'

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        return get_object_or_404(Club, profile__id=profile_id)

    def get_success_url(self):
        return reverse('clubs:club_list')
