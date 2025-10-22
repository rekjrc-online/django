from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profiletype', 'displayname', 'bio', 'avatar', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'full-width'}),
            'displayname': forms.TextInput(attrs={'class': 'full-width'}),
            'location': forms.TextInput(attrs={'class': 'full-width'}),
            'website': forms.URLInput(attrs={'class': 'full-width'}),
        }
