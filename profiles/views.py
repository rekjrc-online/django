from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import get_object_or_404

@login_required
def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk, human=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles-list-create')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form, 'profile': profile})

@login_required(login_url='/')
def profiles_list_create(request):
    user_profiles = Profile.objects.filter(human=request.user).order_by('profiletype', 'displayname')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.human = request.user
            profile.save()
            return redirect('profiles-list-create')
    else:
        form = ProfileForm()
    context = {
        'profiles': user_profiles,
        'form': form,
    }
    return render(request, 'profiles/profiles.html', context)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'