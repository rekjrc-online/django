from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from .models import Build, BuildAttributeEnum
from .forms import BuildForm, BuildAttributeFormSet

class BuildBuildView(LoginRequiredMixin, CreateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_form.html'
    def dispatch(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        build = Build.objects.filter(profile_id=profile_id).first()
        if build:
            return redirect('builds:build_detail', profile_id=profile_id)
        return super().dispatch(request, *args, **kwargs)
    def get_initial(self):
        profile_id = self.kwargs.get('profile_id')
        from profiles.models import Profile
        profile = Profile.objects.get(id=profile_id)
        return {
            'profile': profile.id,
            'name': f"{profile.displayname} Build" }
    def form_valid(self, form):
        form.instance.human = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs.get('profile_id')
        from profiles.models import Profile
        context['profile'] = Profile.objects.get(id=profile_id)
        return context
    def get_success_url(self):
        return redirect('builds:build_detail', profile_id=self.profile_id)

class BuildDetailView(LoginRequiredMixin, DetailView):
    model = Build
    template_name = 'builds/build_detail.html'
    context_object_name = 'build'
    def get_object(self):
        profile_id = self.kwargs['profile_id']
        try: return Build.objects.get(profile_id=profile_id)
        except Build.DoesNotExist: return None
    def get(self, request, *args, **kwargs):
        build = self.get_object()
        if build is None:
            profile_id = self.kwargs['profile_id']
            return redirect(reverse('build_build', args=[profile_id]))
        self.object = build
        context = self.get_context_data(object=build)
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

class BuildUpdateView(UpdateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_form.html'
    def dispatch(self, request, *args, **kwargs):
        """Redirect to update page if Build already exists."""
        profile_id = self.kwargs['profile_id']
        build = Build.objects.filter(profile_id=profile_id).first()
        if not build:
            # If no build exists, forward to the build creation page
            return redirect('builds:build_build', profile_id=profile_id)
        self.object = build
        return super().dispatch(request, *args, **kwargs)
    def get_object(self):
        # self.object is already set in dispatch
        return self.object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        # Attribute formset
        if self.request.method == "POST":
            formset = BuildAttributeFormSet(
                self.request.POST,
                instance=self.object,
                prefix='attributes'
            )
        else:
            formset = BuildAttributeFormSet(
                instance=self.object,
                prefix='attributes'
            )

        # Sort existing attributes
        formset.queryset = formset.queryset.order_by('attribute_type__name')

        # Sort attribute_type dropdown
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
            return self.form_valid(form)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form):
        # Save form and formset
        form.save()
        self.get_context_data()['attribute_formset'].save()
        return redirect('builds:build_detail', profile_id=self.object.profile.id)

    def form_invalid(self, form, formset):
        # Re-render the page with errors
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        print("BuildUpdateView.form_valid")
        context = self.get_context_data()
        attribute_formset = context["attribute_formset"]

        if attribute_formset.is_valid():
            self.object = form.save()
            attribute_formset.instance = self.object
            attribute_formset.save()

            # Manual redirect fixes both submission and POST refresh issue
            return redirect(reverse("build_detail", kwargs={"profile_id": self.object.profile.id}))

        return self.form_invalid(form)

class BuildDeleteView(LoginRequiredMixin, DeleteView):
    #Allows deleting your own build.
    model = Build
    template_name = 'builds/build_confirm_delete.html'
    success_url = reverse_lazy('build_list')
    def get_queryset(self):
        return Build.objects.filter(human=self.request.user)
