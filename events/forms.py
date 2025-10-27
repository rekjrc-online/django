from django import forms
from .models import Event, EventInterest

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['location', 'eventdate', 'multiday']
        widgets = {
            'eventdate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EventInterestForm(forms.ModelForm):
    class Meta:
        model = EventInterest
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional note...'}),
        }
