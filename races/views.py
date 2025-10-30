from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, DeleteView
from django.views.generic.edit import FormView
from profiles.models import Profile
from .models import Race
from .forms import RaceForm, RaceAttributeFormSet

# /races/
class RaceListView(LoginRequiredMixin, ListView):
    model = Race
    template_name = "races/race_list.html"
    context_object_name = "races"
    def get_queryset(self):
        return Race.objects.select_related("profile", "event", "location").all()

# /races/<profile_id>/
class RaceDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "races/race_detail.html"
    context_object_name = "profile"
    pk_url_kwarg = "profile_id"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context["race"] = getattr(profile, "race", None)
        return context

# /races/<profile_id>/build/
class RaceBuildView(LoginRequiredMixin, FormView):
    template_name = "races/race_build.html"
    form_class = RaceForm
    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, id=kwargs["profile_id"])
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class=None):
        race, _ = Race.objects.get_or_create(profile=self.profile, human=self.request.user)
        return self.form_class(instance=race, **self.get_form_kwargs())
    def form_valid(self, form):
        race = form.save(commit=False)
        race.profile = self.profile
        race.human = self.request.user
        race.save()
        messages.success(self.request, "Race saved successfully.")
        return redirect("races:race_detail", profile_id=self.profile.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context

# /races/<profile_id>/update/
class RaceUpdateView(LoginRequiredMixin, FormView):
    template_name = "races/race_update.html"
    form_class = RaceForm
    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, id=kwargs["profile_id"])
        self.race = get_object_or_404(Race, profile=self.profile)
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class=None):
        return self.form_class(instance=self.race, **self.get_form_kwargs())
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        attribute_formset = RaceAttributeFormSet(instance=self.race)
        return self.render_to_response(
            self.get_context_data(form=form, attribute_formset=attribute_formset, profile=self.profile)
        )
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        attribute_formset = RaceAttributeFormSet(request.POST, instance=self.race)
        if form.is_valid() and attribute_formset.is_valid():
            race = form.save(commit=False)
            race.save()
            attribute_formset.save()
            messages.success(request, "Race and attributes updated successfully.")
            return redirect("races:race_detail", profile_id=self.profile.id)
        return self.render_to_response(
            self.get_context_data(form=form, attribute_formset=attribute_formset, profile=self.profile)
        )

# /races/<profile_id>/delete/
class RaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Race
    template_name = "races/race_confirm_delete.html"
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs["profile_id"])
        return getattr(profile, "race", None)
    def get_success_url(self):
        messages.success(self.request, "Race deleted successfully.")
        return reverse_lazy("races:race_list")
