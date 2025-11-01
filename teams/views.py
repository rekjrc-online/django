from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from profiles.models import Profile
from .models import Team
from .forms import TeamForm, TeamMemberFormSet

class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'
    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)
        return get_object_or_404(Team, profile=profile)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all()
        return context

class TeamBuildView(View):
    template_name = 'teams/team_build.html'
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        try:
            team = Team.objects.get(profile=profile)
            return redirect('teams:team_update', profile_id=profile.id)
        except Team.DoesNotExist:
            team = Team(profile=profile)
        form = TeamForm(instance=team)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
        })
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        try:
            team = Team.objects.get(profile=profile)
        except Team.DoesNotExist:
            team = Team(profile=profile)
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.profile = profile
            team.save()
            return redirect('teams:team_update', profile_id=profile.id)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
        })

class TeamUpdateView(View):
    template_name = 'teams/team_update.html'
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        team = get_object_or_404(Team, profile=profile)
        form = TeamForm(instance=team)
        member_formset = TeamMemberFormSet(instance=team)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'member_formset': member_formset,
        })
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        team = get_object_or_404(Team, profile=profile)
        form = TeamForm(request.POST, instance=team)
        member_formset = TeamMemberFormSet(request.POST, instance=team)
        if form.is_valid() and member_formset.is_valid():
            form.save()
            member_formset.save()
            return redirect('teams:team_detail', profile_id=profile.id)
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
            'member_formset': member_formset,
        })

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('teams:team_list')
    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)
        return get_object_or_404(Team, profile=profile)
