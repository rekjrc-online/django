from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, DeleteView, ListView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from profiles.models import Profile
from .models import Build
from .forms import BuildForm, BuildAttributeFormSet

class BuildListView(LoginRequiredMixin, ListView):
    model = Build
    template_name = 'builds/build_list.html'
    context_object_name = 'builds'
    login_url = '/humans/login/'

    def get_queryset(self):
        return (
            Build.objects.filter(human=self.request.user)
            .select_related('profile')
            .order_by('profile__displayname')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.filter(human=self.request.user).order_by('profiletype', 'displayname')

        context['unbuilt_models'] = Profile.objects.filter(
            human=self.request.user,
            profiletype='MODEL'
        ).filter(builds__isnull=True).order_by('displayname')

        return context

class BuildBuildView(LoginRequiredMixin, View):
    template_name = 'builds/build_build.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        existing_build = Build.objects.filter(profile=profile).first()
        if existing_build:
            return redirect('builds:build_update', profile_id=profile_id)

        form = BuildForm(initial={'human': request.user.id, 'profile': profile.id})
        formset = BuildAttributeFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset, 'profile': profile})

    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        form = BuildForm(request.POST)
        formset = BuildAttributeFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            build = form.save(commit=False)
            build.human = request.user
            build.profile = profile
            build.save()
            formset.instance = build
            formset.save()
            return redirect('builds:build_detail', profile_id=profile_id)

        return render(request, self.template_name, {'form': form, 'formset': formset, 'profile': profile})

class BuildUpdateView(LoginRequiredMixin, View):
    template_name = 'builds/build_update.html'

    def get_build(self, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        return get_object_or_404(Build, profile=profile)

    def get(self, request, profile_id):
        build = self.get_build(profile_id)
        form = BuildForm(instance=build)
        formset = BuildAttributeFormSet(instance=build)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'profile': build.profile
        })

    def post(self, request, profile_id):
        build = self.get_build(profile_id)
        form = BuildForm(request.POST, instance=build)
        formset = BuildAttributeFormSet(request.POST, instance=build)

        # Update Profile fields from the POST data
        profile = build.profile
        profile.displayname = request.POST.get('displayname', profile.displayname)
        profile.bio = request.POST.get('bio', profile.bio)

        if form.is_valid() and formset.is_valid():
            build = form.save()
            formset.save()
            profile.save()  # save changes to Profile
            return redirect('builds:build_detail', profile_id=profile_id)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'profile': profile
        })

class BuildDetailView(LoginRequiredMixin, DetailView):
    model = Build
    template_name = 'builds/build_detail.html'
    context_object_name = 'build'

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        try:
            return Build.objects.get(profile_id=profile_id)
        except Build.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        build = self.get_object()
        if build is None:
            return redirect('builds:build_build', profile_id=self.kwargs['profile_id'])
        self.object = build
        return self.render_to_response(self.get_context_data(object=build))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

class BuildDeleteView(LoginRequiredMixin, DeleteView):
    model = Build
    template_name = 'builds/build_confirm_delete.html'
    success_url = reverse_lazy('builds:build_list')

    def get_queryset(self):
        return Build.objects.filter(human=self.request.user)
