from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse, get_object_or_404, render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from .forms import ProfileEditForm, ProfileCreateForm
from .models import Profile

from builds.models import Build
from clubs.models import Club
from events.models import Event
from locations.models import Location
from races.models import Race
from stores.models import Store
from teams.models import Team
from tracks.models import Track

from builds.forms import BuildForm, BuildAttributeFormSet
from clubs.forms import ClubForm, ClubLocationFormSet
from events.forms import EventForm
from locations.forms import LocationForm
from races.forms import RaceForm, RaceAttributeFormSet
from stores.forms import StoreForm
from teams.forms import TeamForm
from tracks.forms import TrackForm, TrackAttributeFormSet

import logging
logger = logging.getLogger(__name__)

class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profiles/profile_update.html'
    related_models = {
        'model': {
            'model': Build,
            'form': BuildForm,
            'subforms': {
                'attributes': {
                    'fk': 'build',
                    'formset': BuildAttributeFormSet}}},
        'club': {
            'model': Club,
            'form': ClubForm,
            'subforms': {
                'locations': {
                    'fk': 'club',
                    'formset': ClubLocationFormSet}}},
        'race': {
            'model': Race,
            'form': RaceForm,
            'subforms': {
                'attributes': {
                    'fk': 'race',
                    'formset': RaceAttributeFormSet}}},
        'track': {
            'model': Track,
            'form': TrackForm,
            'subforms': {
                'attributes': {
                    'fk': 'track',
                    'formset': TrackAttributeFormSet}}},
        'event': {'model': Event, 'form': EventForm},
        'location': {'model': Location, 'form': LocationForm},
        'store': {'model': Store, 'form': StoreForm},
        'team': {'model': Team, 'form': TeamForm},
    }

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        profile_form = ProfileEditForm(instance=profile)
        context = {'profile': profile, 'profile_form': profile_form}
        profiletype_info = self.related_models.get(profile.profiletype.lower())
        if not profiletype_info:
            return render(request, self.template_name, context)
        model_class = profiletype_info['model']
        form_class = profiletype_info['form']
        subforms = profiletype_info.get('subforms', {})
        obj = model_class.objects.filter(profile=profile).first()
        related_form = form_class(instance=obj)
        context['related_form'] = related_form
        context['related_obj'] = obj
        context['related_type'] = profile.profiletype
        subformsets = {}
        for key, sub in subforms.items():
            formset_class = sub.get('formset')
            if formset_class:
                subformsets[key] = formset_class(
                    instance=obj,
                    queryset=getattr(obj, key).all() if obj else formset_class.model.objects.none(),
                    prefix=key
                )
        context.update({
            'related_form': related_form,
            'related_obj': obj,
            'related_type': profile.profiletype,
            'subformsets': subformsets,
        })
        return render(request, self.template_name, context)

    def post(self, request, profile_id):
        print()
        print()
        print("=================================")
        print("Submitted POST data:", request.POST)
        print("=================================")
        print()
        print()
        print(f"\n--- ProfileUpdateView POST called for profile_id={profile_id} ---")
        
        profile = get_object_or_404(Profile, pk=profile_id)
        print(f"Loaded Profile: {profile}")

        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        print(f"Profile form initialized. POST keys: {list(request.POST.keys())}, FILES keys: {list(request.FILES.keys())}")

        profiletype_info = self.related_models.get(profile.profiletype.lower())
        if not profiletype_info:
            print("No related model for this profile type.")
            if profile_form.is_valid():
                print("Profile form valid. Saving...")
                profile_form.save()
                return redirect('profiles:detail-profile', profile_id=profile.id)
            else:
                print("Profile form invalid:", profile_form.errors)
                return render(self.request, self.template_name, {'profile': profile, 'profile_form': profile_form})

        model_class = profiletype_info['model']
        form_class = profiletype_info['form']
        subforms = profiletype_info.get('subforms', {})
        print(f"Related model: {model_class}, Form: {form_class}, Subforms: {list(subforms.keys())}")

        # Ensure related object exists
        related_obj, created = model_class.objects.get_or_create(profile=profile)
        print(f"Related object: {related_obj} (created={created})")

        related_form = form_class(request.POST, request.FILES, instance=related_obj)
        print(f"Related form initialized. Valid? {related_form.is_valid()}")

        # Build inline formsets
        subformsets = {}
        for key, sub in subforms.items():
            if 'formset' in sub:
                formset_class = sub['formset']
                subformsets[key] = formset_class(
                    request.POST, 
                    request.FILES, 
                    instance=related_obj, 
                    queryset=getattr(related_obj, key).all() if related_obj else formset_class.model.objects.none(),
                    prefix=key
                )
                print(f"Initialized subformset '{key}' with {len(subformsets[key].forms)} forms.")

        # Validate all forms
        all_valid = profile_form.is_valid() and related_form.is_valid() and all(fs.is_valid() for fs in subformsets.values())
        print(f"Validation: profile_form={profile_form.is_valid()}, related_form={related_form.is_valid()}, all subforms valid={all(fs.is_valid() for fs in subformsets.values())}")

        if not all_valid:
            print("Form validation failed.")
            print("Profile form errors:", profile_form.errors)
            print("Related form errors:", related_form.errors)
            for key, fs in subformsets.items():
                print(f"Subformset '{key}' errors: {fs.errors}")
            context = {
                'profile': profile,
                'profile_form': profile_form,
                'related_form': related_form,
                'related_type': profile.profiletype,
                'subformsets': subformsets,
            }
            return render(request, self.template_name, context)

        # Save all forms
        print("All forms valid. Saving...")
        profile_form.save()
        related_obj = related_form.save(commit=False)
        related_obj.profile = profile
        related_obj.save()
        print(f"Saved related object: {related_obj}")

        for key, fs in subformsets.items():
            fs.instance = related_obj  # ensure FK is set
            saved_instances = fs.save()
            print(f"Saved subformset '{key}' with {len(saved_instances)} instances.")

        print("Redirecting to profile detail page.")
        return redirect('profiles:detail-profile', profile_id=profile.id)


class ProfilesListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profiles.html'
    context_object_name = 'profiles'
    login_url = '/humans/login/'
    def get_queryset(self):
        return Profile.objects.filter(human=self.request.user).order_by('profiletype', 'displayname')


class ProfileBuildView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profiles/profile_build.html'
    login_url = '/humans/login/'
    def form_valid(self, form):
        form.instance.human = self.request.user
        self.object = form.save()
        return redirect('profiles:detail-profile', profile_id=self.object.pk)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'profile_id'

    related_models = {
        'model': Build,
        'club': Club,
        'race': Race,
        'track': Track,
        'event': Event,
        'location': Location,
        'store': Store,
        'team': Team,
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs['profile_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        # Posts with images (existing)
        context['posts_with_images'] = profile.posts.filter(image__isnull=False).exclude(image='')

        # Dynamically gather related objects
        related_objs = {}
        profile_type_lower = profile.profiletype.lower()
        for key, model_class in self.related_models.items():
            if key == profile_type_lower:
                # fetch the related object(s)
                try:
                    if model_class._meta.model_name == 'club':
                        # clubs may have multiple locations / members
                        obj = model_class.objects.get(profile=profile)
                        locations = obj.locations.all()
                        members = obj.members.all()
                        related_objs[key] = {
                            'object': obj,
                            'locations': locations,
                        }
                    else:
                        obj = model_class.objects.filter(profile=profile).first()
                        related_objs[key] = {'object': obj} if obj else None
                except model_class.DoesNotExist:
                    related_objs[key] = None

        context['related_objs'] = related_objs
        return context


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profiles/confirm_delete.html'
    pk_url_kwarg = 'profile_id'
    login_url = '/humans/login/'
    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        if profile.human != self.request.user:
            return redirect('profiles:detail-profile', profile_id=profile.id)
        return profile
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.human != request.user:
            return redirect('profiles:detail-profile', profile_id=profile.id)
        # Soft-delete
        profile.deleted = True
        profile.save()
        return redirect('/profiles/')
