from django import forms
from django.forms import inlineformset_factory
from .models import Build, BuildAttribute, BuildAttributeEnum

class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ['profile', 'name', 'description']
        widgets = {
            'profile': forms.HiddenInput(),  # auto-set from view
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter build name',
                'style': 'width: 100%;'
            }),
            'description': forms.Textarea(attrs={
                'id': 'id_description',  # fixed ID for JS counter
                'rows': 5,
                'style': 'width: 100%;',
                'placeholder': 'Optional',
            }),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['attribute_type'].queryset = BuildAttributeEnum.objects.order_by('name')

BuildAttributeFormSet = inlineformset_factory(
    Build,
    BuildAttribute,
    fields=('attribute_type', 'value'),
    extra=1,
    can_delete=True
)