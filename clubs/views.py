from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import Profile
from .models import Club
from .forms import ClubForm

class ClubListView(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'
    login_url = '/humans/login/'

    def get_queryset(self):
        # ✅ Show only clubs owned by this human
        return Club.objects.filter(profile__human=self.request.user).select_related('profile').order_by('id')

class ClubBuildView(LoginRequiredMixin, View):
    template_name = 'clubs/club_build.html'
    login_url = '/humans/login/'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        # ✅ Ownership check
        if profile.human != request.user:
            return redirect('profiles:detail-profile', profile.id)

        existing_club = Club.objects.filter(profile=profile).first()
        if existing_club:
            return redirect('profiles:update-profile', profile.id)

        form = ClubForm()
        return render(request, self.template_name, {
            'profile': profile,
            'form': form,
        })

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        # ✅ Ownership check
        if profile.human != request.user:
            return redirect('profiles:detail-profile', profile.id)

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

class ClubDeleteView(LoginRequiredMixin, DeleteView):
    model = Club
    template_name = 'clubs/club_confirm_delete.html'
    login_url = '/humans/login/'

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        club = get_object_or_404(Club, profile__id=profile_id)

        # ✅ Ownership check
        if club.profile.human != self.request.user:
            # Redirect immediately if ownership fails
            self.permission_denied_redirect = redirect('profiles:detail-profile', profile_id)
            return None

        return club

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return self.permission_denied_redirect
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return self.permission_denied_redirect
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('clubs:club_list')
