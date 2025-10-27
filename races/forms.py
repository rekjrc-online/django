from django import forms
from .models import Race, RaceAttribute
from django.forms.models import inlineformset_factory

class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = [
            'profile',
            'human',
            'event',
            'location',
            'club',
            'team',
            'race_type'
        ]
        widgets = {
            'race_type': forms.Select(),
        }

# Inline formset for RaceAttribute
RaceAttributeFormSet = inlineformset_factory(
    Race,
    RaceAttribute,
    fields=('attribute', 'value'),
    extra=1,
    can_delete=True
)
