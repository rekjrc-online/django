from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from profiles.models import Profile
from .models import Team
from .forms import TeamForm, TeamMemberFormSet


class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'


class TeamBuildView(View):
    template_name = 'teams/team_build.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        team, created = Team.objects.get_or_create(profile=profile)
        form = TeamForm(instance=team)
        member_formset = TeamMemberFormSet(instance=team)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'member_formset': member_formset,
        })

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        team, created = Team.objects.get_or_create(profile=profile)
        form = TeamForm(request.POST, instance=team)
        member_formset = TeamMemberFormSet(request.POST, instance=team)

        if form.is_valid() and member_formset.is_valid():
            form.save()
            member_formset.save()
            return redirect('teams:team_list')

        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'member_formset': member_formset,
        })
