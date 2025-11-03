from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Store
from .forms import StoreForm

class StoreListView(ListView):
    model = Store
    template_name = 'stores/store_list.html'
    context_object_name = 'stores'
    ordering = ['name']
    def get_queryset(self):
        """Return stores for the user's profile if logged in, else all stores."""
        if self.request.user.is_authenticated:
            profile = getattr(self.request.user, 'profile', None)
            if profile:
                return Store.objects.filter(profile=profile).order_by('name')
        return Store.objects.all().order_by('name')

class StoreDetailView(DetailView):
    model = Store
    template_name = 'stores/store_detail.html'
    context_object_name = 'store'
    def get_queryset(self):
        """Return stores for the user's profile if logged in, else all stores."""
        if self.request.user.is_authenticated:
            profile = getattr(self.request.user, 'profile', None)
            if profile:
                return Store.objects.filter(profile=profile)
        return Store.objects.all()

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
        profile = getattr(self.request.user, 'profile', None)
        if profile:
            form.instance.profile = profile
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('store:detail', kwargs={'pk': self.object.pk})

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Store
    form_class = StoreForm
    template_name = 'stores/store_form.html'
    def get_object(self, queryset=None):
        """Return the store associated with the logged-in user."""
        if self.request.user.is_authenticated:
            return Store.objects.get(profile__user=self.request.user)
        return super().get_object(queryset)
    def get_success_url(self):
        return reverse_lazy('store:detail', kwargs={'pk': self.object.pk})

class StoreDeleteView(LoginRequiredMixin, DeleteView):
    model = Store
    template_name = 'stores/store_confirm_delete.html'
    success_url = reverse_lazy('store:list')
    def get_queryset(self):
        """Only allow deletion of stores belonging to the logged-in user's profile."""
        if self.request.user.is_authenticated:
            profile = getattr(self.request.user, 'profile', None)
            if profile:
                return Store.objects.filter(profile=profile)
        return Store.objects.none()
