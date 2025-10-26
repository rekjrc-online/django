from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Store
from .forms import StoreForm

class StoreBuildView(CreateView):
    model = Store
    form_class = StoreForm
    template_name = 'stores/store_form.html'
    success_url = reverse_lazy('store:register')
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            profile = getattr(self.request.user, 'profile', None)
            if profile:
                form.instance.profile = profile
        return super().form_valid(form)

class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreForm
    template_name = 'stores/store_form.html'
    success_url = reverse_lazy('store:update')
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return Store.objects.get(profile__user=self.request.user)
        return super().get_object(queryset)
