from django import forms
from django.forms import inlineformset_factory
from .models import Race, RaceAttribute, Track

class RaceForm(forms.ModelForm):
    track = forms.ModelChoiceField(
        queryset=Track.objects.all(),
        required=True,
        empty_label="Select Track",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Race
        fields = [
            "race_type",
            "event",
            "location",
            "track",
            "club",
            "team",
        ]
        widgets = {
            field: forms.Select(attrs={"class": "form-control"})
            for field in fields
        }

RaceAttributeFormSet = inlineformset_factory(
    Race,
    RaceAttribute,
    fields=("attribute", "value"),
    extra=1,
    can_delete=True,
)
