from django import forms
from django.forms import inlineformset_factory
from .models import Track, TrackAttribute, TrackAttributeEnum, TrackType

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['name', 'track_type', 'location']


class TrackAttributeForm(forms.ModelForm):
    class Meta:
        model = TrackAttribute
        fields = ['attribute_type', 'value']


TrackAttributeFormSet = inlineformset_factory(
    Track,
    TrackAttribute,
    form=TrackAttributeForm,
    extra=1,
    can_delete=True
)
