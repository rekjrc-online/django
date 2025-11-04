from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, DeleteView, TemplateView
from django.views.generic.edit import FormView
from profiles.models import Profile
from .models import Race, RaceDriver
from .forms import RaceForm, RaceAttributeFormSet

class RaceListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "races/race_list.html"
    context_object_name = "profiles"
    def get_queryset(self):
        return (
            Profile.objects
            .filter(profiletype='RACE')
            .select_related('human')
            .prefetch_related('race')
        )

class RaceDetailView(LoginRequiredMixin, DetailView):
    model = Race
    template_name = "races/race_detail.html"
    context_object_name = "race"
    pk_url_kwarg = "profile_id"
    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.kwargs["profile_id"])
        race = getattr(profile, "race", None)
        if not race:
            return redirect("races:race_build", profile_id=self.profile.id)
        return race
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.object
        context["profile"] = race.profile
        context["event"] = getattr(race, "event", None)
        context["location"] = getattr(race, "location", None)
        context["attributes"] = getattr(race, "attributes", None)
        context['race_drivers'] = race.race_drivers.select_related('human', 'driver', 'model')
        context["user_is_in_race"] = race.race_drivers.filter(human=self.request.user).exists()
        return context

class RaceBuildView(View):
    template_name = "races/race_build.html"
    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, id=kwargs["profile_id"])
        existing_race = Race.objects.filter(profile=self.profile).first()
        if existing_race:
            return redirect("races:race_update", profile_id=self.profile.id)
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        form = RaceForm()
        return render(request, self.template_name, {"form": form, "profile": self.profile})
    def post(self, request, *args, **kwargs):
        form = RaceForm(request.POST)
        if form.is_valid():
            race = form.save(commit=False)
            race.profile = self.profile
            race.human = request.user
            race.save()
            return redirect("races:race_detail", profile_id=self.profile.id)
        return render(request, self.template_name, {"form": form, "profile": self.profile})

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
            self.get_context_data(form=form, attribute_formset=attribute_formset, profile=self.profile))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.race)
        attribute_formset = RaceAttributeFormSet(request.POST, instance=self.race)
        if form.is_valid() and attribute_formset.is_valid():
            race = form.save(commit=False)
            race.profile = self.profile
            race.human = request.user
            race.save()
            attribute_formset.save()
            return redirect("races:race_update", profile_id=self.profile.id)
        return self.render_to_response(
            self.get_context_data(form=form, attribute_formset=attribute_formset, profile=self.profile))

class RaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Race
    template_name = "races/race_confirm_delete.html"
    def get_object(self):
        profile = get_object_or_404(Profile, id=self.kwargs["profile_id"])
        return getattr(profile, "race", None)
    def get_success_url(self):
        return reverse_lazy("races:race_list")

class RaceJoinView(LoginRequiredMixin, View):
    template_name = "races/race_join.html"
    def get(self, request, profile_id):
        race = get_object_or_404(Race, profile_id=profile_id)
        driver_profiles = Profile.objects.filter(human=request.user, profiletype="DRIVER")
        model_profiles = Profile.objects.filter(human=request.user, profiletype="MODEL")
        context = {
            "race": race,
            "driver_profiles": driver_profiles,
            "model_profiles": model_profiles,
        }
        return render(request, self.template_name, context)
    def post(self, request, profile_id):
        race = get_object_or_404(Race, profile_id=profile_id)
        driver_id = request.POST.get("driver_id")
        model_id = request.POST.get("model_id")
        driver_profile = Profile.objects.filter(id=driver_id, human=request.user, profiletype="DRIVER").first() if driver_id else None
        model_profile = Profile.objects.filter(id=model_id, human=request.user, profiletype="MODEL").first() if model_id else None
        race_driver, created = RaceDriver.objects.update_or_create(
            race=race,
            human=request.user,
            defaults={
                "driver": driver_profile,
                "model": model_profile,
            }
        )
        return redirect("races:race_detail", profile_id=race.profile.id)
