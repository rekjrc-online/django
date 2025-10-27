from django import forms
from django.forms import inlineformset_factory
from .models import Club, ClubMember, ClubLocation

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name']

class ClubMemberForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        fields = ['human', 'role']

class ClubLocationForm(forms.ModelForm):
    class Meta:
        model = ClubLocation
        fields = ['location']

# Formsets
ClubMemberFormSet = inlineformset_factory(
    Club, ClubMember, form=ClubMemberForm, extra=1, can_delete=True
)
ClubLocationFormSet = inlineformset_factory(
    Club, ClubLocation, form=ClubLocationForm, extra=1, can_delete=True
)
