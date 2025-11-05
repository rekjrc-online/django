from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Build
from profiles.models import Profile
from .forms import BuildForm


# ========================================
# 1️⃣ List all builds belonging to the user
# ========================================
class BuildListView(LoginRequiredMixin, ListView):
    model = Build
    template_name = 'builds/build_list.html'
    context_object_name = 'builds'

    def get_queryset(self):
        return Build.objects.filter(human=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.filter(human=self.request.user, profiletype='MODEL')
        context['unbuilt_models'] = Profile.objects.filter(human=self.request.user, profiletype='MODEL').exclude(id__in=Build.objects.values_list('profile_id', flat=True))
        return context


# ========================================
# 2️⃣ Create a new build for a profile
# ========================================
class BuildBuildView(LoginRequiredMixin, View):
    template_name = 'builds/build_build.html'

    def get_profile(self, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.human != self.request.user:
            return None
        return profile

    def get(self, request, profile_id):
        profile = self.get_profile(profile_id)
        if not profile:
            return redirect('profiles:detail-profile', profile_id)

        existing_build = Build.objects.filter(profile=profile).first()
        if existing_build:
            return redirect('builds:build_update', profile_id=profile.id)

        form = BuildForm()
        return render(request, self.template_name, {'form': form, 'profile': profile})

    def post(self, request, profile_id):
        profile = self.get_profile(profile_id)
        if not profile:
            return redirect('profiles:detail-profile', profile_id)

        existing_build = Build.objects.filter(profile=profile).first()
        if existing_build:
            return redirect('builds:build_update', profile_id=profile.id)

        form = BuildForm(request.POST)
        if form.is_valid():
            build = form.save(commit=False)
            build.profile = profile
            build.human = request.user
            build.save()
            return redirect('profiles:detail-profile', profile.id)
        return render(request, self.template_name, {'form': form, 'profile': profile})


# ========================================
# 3️⃣ Update an existing build
# ========================================
class BuildUpdateView(LoginRequiredMixin, View):
    template_name = 'builds/build_update.html'

    def get_build(self, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.human != self.request.user:
            return None, None
        build = get_object_or_404(Build, profile=profile)
        if build.human != self.request.user:
            return profile, None
        return profile, build

    def get(self, request, profile_id):
        profile, build = self.get_build(profile_id)
        if not profile or not build:
            return redirect('profiles:detail-profile', profile_id)

        form = BuildForm(instance=build)
        return render(request, self.template_name, {'form': form, 'profile': profile, 'build': build})

    def post(self, request, profile_id):
        profile, build = self.get_build(profile_id)
        if not profile or not build:
            return redirect('profiles:detail-profile', profile_id)

        form = BuildForm(request.POST, instance=build)
        if form.is_valid():
            form.save()
            return redirect('profiles:detail-profile', profile.id)
        return render(request, self.template_name, {'form': form, 'profile': profile, 'build': build})


# ========================================
# 4️⃣ Build details (view only)
# ========================================
class BuildDetailView(LoginRequiredMixin, DetailView):
    model = Build
    template_name = 'builds/build_detail.html'
    context_object_name = 'build'

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        build = get_object_or_404(Build, profile_id=profile_id)
        if build.human != self.request.user:
            # Redirect instead of raising 404
            return redirect('profiles:detail-profile', profile_id)
        return build

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        # if redirect returned above
        if isinstance(obj, redirect):
            return obj
        return super().get(request, *args, **kwargs)


# ========================================
# 5️⃣ Delete build (safe via queryset)
# ========================================
class BuildDeleteView(LoginRequiredMixin, DeleteView):
    model = Build
    template_name = 'builds/build_confirm_delete.html'
    success_url = reverse_lazy('builds:build_list')

    def get_queryset(self):
        return Build.objects.filter(human=self.request.user)

    def get_success_url(self):
        # after delete, redirect to the related profile
        profile_id = self.object.profile.id
        return reverse_lazy('profiles:detail-profile', kwargs={'profile_id': profile_id})
