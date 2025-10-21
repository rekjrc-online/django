from django import forms
from .models import Post
from profiles.models import Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['profile_id', 'content', 'image', 'video_url']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': "What's happening?",
                'class': 'full-width'
            }),
            'profile_id': forms.Select(attrs={'class': 'full-width'}),
            'image': forms.ClearableFileInput(attrs={'class': 'full-width'}),
            'video_url': forms.URLInput(attrs={'class': 'full-width'}),
        }

    def __init__(self, *args, **kwargs):
        human = kwargs.pop('human', None)  # pass the logged-in user
        super().__init__(*args, **kwargs)
        if human:
            # Limit profile dropdown to only this human’s profiles
            self.fields['profile_id'].queryset = self.fields['profile_id'].queryset = (
                Profile.objects
                    .filter(human=human)
                    .order_by('profiletype', 'displayname'))
        self.fields['profile_id'].label_from_instance = lambda obj: f"{obj.profiletype} - {obj.displayname}"