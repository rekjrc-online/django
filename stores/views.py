from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Store
from .forms import StoreForm

class StoreListView(LoginRequiredMixin, ListView):
    model = Store
    template_name = 'stores/store_list.html'
    context_object_name = 'stores'
    def get_queryset(self):
        profile = getattr(self.request.user, 'profile', None)
        if profile:
            return Store.objects.filter(profile=profile)
        return Store.objects.none()

class StoreBuildView(LoginRequiredMixin, CreateView):
    model = Store
    form_class = StoreForm
    template_name = 'stores/store_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Redirect to update if a store already exists for this profile."""
        profile = getattr(request.user, 'profile', None)
        if profile:
            existing_store = Store.objects.filter(profile=profile).first()
            if existing_store:
                return redirect('store:update', pk=existing_store.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the store to the logged-in user's profile."""
        profile = getattr(self.request.user, 'profile', None)
        if profile:
            form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('store:detail', kwargs={'pk': self.object.pk})

class StoreDeleteView(LoginRequiredMixin, DeleteView):
    model = Store
    template_name = 'stores/store_confirm_delete.html'
    success_url = reverse_lazy('store:list')

    def get_queryset(self):
        """Only allow deletion of stores belonging to the logged-in user's profile."""
        profile = getattr(self.request.user, 'profile', None)
        if profile:
            return Store.objects.filter(profile=profile)
        return Store.objects.none()
