from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Race
from .forms import RaceForm, RaceAttributeFormSet

# List all races
class RaceListView(ListView):
    model = Race
    template_name = 'races/race_list.html'
    context_object_name = 'races'


# View race details
class RaceDetailView(DetailView):
    model = Race
    template_name = 'races/race_detail.html'
    context_object_name = 'race'


# Create a new race with attributes
class RaceCreateView(CreateView):
    model = Race
    form_class = RaceForm
    template_name = 'races/race_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attributes'] = RaceAttributeFormSet(self.request.POST)
        else:
            context['attributes'] = RaceAttributeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attributes = context['attributes']
        self.object = form.save()
        if attributes.is_valid():
            attributes.instance = self.object
            attributes.save()
        return redirect(self.object.get_absolute_url() if hasattr(self.object, 'get_absolute_url') else 'races:race_list')


# Update an existing race with attributes
class RaceUpdateView(UpdateView):
    model = Race
    form_class = RaceForm
    template_name = 'races/race_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attributes'] = RaceAttributeFormSet(self.request.POST, instance=self.object)
        else:
            context['attributes'] = RaceAttributeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attributes = context['attributes']
        self.object = form.save()
        if attributes.is_valid():
            attributes.instance = self.object
            attributes.save()
        return redirect(self.object.get_absolute_url() if hasattr(self.object, 'get_absolute_url') else 'races:race_list')


# Delete a race
class RaceDeleteView(DeleteView):
    model = Race
    template_name = 'races/race_confirm_delete.html'
    success_url = reverse_lazy('races:race_list')
