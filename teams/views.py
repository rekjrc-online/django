from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DeleteView
from profiles.models import Profile
from .models import Team
from .forms import TeamForm

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return Team.objects.filter(profile__human=self.request.user).select_related('profile').order_by('profile__displayname')

class TeamBuildView(View):
    template_name = 'teams/team_build.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.human != request.user:
            return redirect('teams:team_list')

        team, created = Team.objects.get_or_create(profile=profile)
        form = TeamForm(instance=team)
        return render(request, self.template_name, {'profile': profile, 'form': form})

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.human != request.user:
            return redirect('teams:team_list')

        team, created = Team.objects.get_or_create(profile=profile)
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.profile = profile
            team.save()
            return redirect('teams:team_update', profile_id=profile.id)

        return render(request, self.template_name, {'profile': profile, 'form': form})

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('teams:team_list')

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.human != self.request.user:
            return redirect('teams:team_list')
        return get_object_or_404(Team, profile=profile)
