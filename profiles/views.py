from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileCreateForm, ProfileEditForm
from django.shortcuts import get_object_or_404

def detail_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    posts_with_images = profile.posts.filter(image__isnull=False).exclude(image='')
    return render(request, 'profiles/profile_detail.html', {'profile': profile, 'posts_with_images': posts_with_images})

@login_required(login_url='/')
def profiles_list_create(request):
    user_profiles = Profile.objects.filter(human=request.user).order_by('profiletype', 'displayname')
    if request.method == 'POST':
        form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.human = request.user
            profile.save()
            return redirect('profiles-list-create')
    else:
        form = ProfileCreateForm()
    context = {
        'profiles': user_profiles,
        'form': form,
    }
    return render(request, 'profiles/profiles.html', context)

@login_required
def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, human=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles-list-create')
        else:
            print("FORM NOT VALID")
            print(form.errors)
            print(form.non_field_errors())
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'profiles/profile_edit.html', {'form': form, 'profile': profile})

@login_required
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, human=request.user)
    if request.method == 'POST':
        profile.deleted = True
        profile.save()
        return redirect('/profiles/')
    return render(request, 'profiles/confirm_delete.html', {'profile': profile})
