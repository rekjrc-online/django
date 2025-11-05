from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View, DeleteView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count
from django.db import IntegrityError
from profiles.models import Profile
from .models import Race, RaceDriver, LapMonitorResult
from .forms import RaceForm, RaceAttributeFormSet
from io import TextIOWrapper
import csv

class LapMonitorUploadView(View):
    template_name = "races/lapmonitor_upload.html"

    def get(self, request, race_id):
        race = get_object_or_404(Race, pk=race_id)
        return render(request, self.template_name, {"race": race})

    def post(self, request, race_id):
        race = get_object_or_404(Race, pk=race_id)
        file = request.FILES.get("file")

        if not file:
            messages.error(request, "❌ No file selected.")
            return redirect("races:upload_lapmonitor", race_id=race.id)

        try:
            # Decode file
            data = TextIOWrapper(file.file, encoding="utf-8")
            reader = csv.DictReader(data)

            # ✅ Normalize headers (handle "Session Id" → "session_id")
            reader.fieldnames = [
                name.strip().lower().replace(" ", "_") for name in reader.fieldnames
            ]

            created_count = 0
            skipped_count = 0

            for row in reader:
                try:
                    # Skip empty rows
                    if not row.get("driver_id") or not row.get("lap_index"):
                        skipped_count += 1
                        continue

                    # Avoid duplicates (same race + driver_id + lap_index)
                    if LapMonitorResult.objects.filter(
                        race=race,
                        driver_id=row.get("driver_id"),
                        lap_index=row.get("lap_index")
                    ).exists():
                        skipped_count += 1
                        continue

                    LapMonitorResult.objects.create(
                        race=race,
                        session_id=row.get("session_id"),
                        session_name=row.get("session_name"),
                        session_date=row.get("session_date"),
                        session_kind=row.get("session_kind"),
                        session_duration=float(row.get("session_duration") or 0),
                        driver_id=row.get("driver_id"),
                        driver_name=row.get("driver_name"),
                        driver_transponder_id=row.get("driver_transponder_id"),
                        driver_rank=int(row.get("driver_rank") or 0),
                        lap_index=int(row.get("lap_index") or 0),
                        lap_end_time=float(row.get("lap_end_time") or 0),
                        lap_duration=float(row.get("lap_duration") or 0),
                        lap_kind=row.get("lap_kind"),
                    )
                    created_count += 1

                except IntegrityError:
                    skipped_count += 1
                except Exception as e:
                    print(f"Error processing row: {e}")
                    skipped_count += 1

            messages.success(
                request,
                f"✅ Imported {created_count} new results, skipped {skipped_count} duplicates or invalid rows."
            )

        except Exception as e:
            messages.error(request, f"❌ Error processing CSV: {e}")

        # ✅ Correct redirect (URL expects profile_id)
        return redirect("races:race_detail", profile_id=race.profile.id)

class RaceListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "races/race_list.html"
    context_object_name = "profiles"
    def get_queryset(self):
        return (
            Profile.objects
            .filter(profiletype='RACE')
            .select_related('human')
            .annotate(driver_count=Count('race__race_drivers'))
            .order_by('displayname')
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
        transponder = request.POST.get("transponder")
        driver_profile = Profile.objects.filter(id=driver_id, human=request.user, profiletype="DRIVER").first() if driver_id else None
        model_profile = Profile.objects.filter(id=model_id, human=request.user, profiletype="MODEL").first() if model_id else None
        existing = RaceDriver.objects.filter(
            race=race,
            human=request.user,
            driver=driver_profile,
            model=model_profile
        ).exists()
        if not existing:
            RaceDriver.objects.create(
                race=race,
                human=request.user,
                driver=driver_profile,
                model=model_profile,
                transponder=transponder,
            )
        return redirect("races:race_detail", profile_id=race.profile.id)
