from django import forms
from django.forms import inlineformset_factory
from .models import Race, RaceAttribute

class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = [
            "race_type",
            "event",
            "location",
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
