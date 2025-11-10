from django import forms
from profiles.models import Profile
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['profile', 'content', 'image', 'video_url']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': "What's happening?",
                'class': 'full-width'
            }),
            'profile': forms.Select(attrs={'class': 'full-width'}),
            'image': forms.ClearableFileInput(attrs={'class': 'full-width'}),
            'video_url': forms.URLInput(attrs={'class': 'full-width'}),
        }

    def __init__(self, *args, **kwargs):
        human = kwargs.pop('human', None)  # pass the logged-in user
        super().__init__(*args, **kwargs)

        if human:
            # Limit dropdown to this user's profiles
            self.fields['profile'].queryset = Profile.objects.filter(human=human).order_by('profiletype', 'displayname')

        # Label format: "TYPE - Name"
        self.fields['profile'].label_from_instance = lambda obj: f"{obj.get_profiletype_display()} - {obj.displayname}"
