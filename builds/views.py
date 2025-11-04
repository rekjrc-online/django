from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from profiles.models import Profile
from .models import Build, BuildAttributeEnum
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

class BuildBuildView(LoginRequiredMixin, CreateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_build.html'

    def dispatch(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        build = Build.objects.filter(profile_id=profile_id).first()
        if build:
            return redirect('builds:build_update', profile_id=profile_id)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(id=profile_id)
        return {
            'profile': profile.id,
        }

    def form_valid(self, form):
        form.instance.human = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs.get('profile_id')
        context['profile'] = Profile.objects.get(id=profile_id)
        return context

    def get_success_url(self):
        return reverse('builds:build_detail', kwargs={'profile_id': self.object.profile.id})

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

class BuildUpdateView(LoginRequiredMixin, UpdateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_update.html'

    def dispatch(self, request, *args, **kwargs):
        profile_id = self.kwargs['profile_id']
        build = Build.objects.filter(profile_id=profile_id).first()
        if not build:
            return redirect('builds:build_build', profile_id=profile_id)
        self.object = build
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile

        if self.request.method == "POST":
            formset = BuildAttributeFormSet(self.request.POST, instance=self.object, prefix='attributes')
        else:
            formset = BuildAttributeFormSet(instance=self.object, prefix='attributes')

        formset.queryset = formset.queryset.order_by('attribute_type__name')
        for form in formset.forms:
            form.fields['attribute_type'].queryset = BuildAttributeEnum.objects.order_by('name')

        context['attribute_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data()
        formset = context['attribute_formset']

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(reverse('builds:build_detail', kwargs={'profile_id': self.object.profile.id}))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data())

class BuildDeleteView(LoginRequiredMixin, DeleteView):
    model = Build
    template_name = 'builds/build_confirm_delete.html'
    success_url = reverse_lazy('builds:build_list')

    def get_queryset(self):
        return Build.objects.filter(human=self.request.user)
