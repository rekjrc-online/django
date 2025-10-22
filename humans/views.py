from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from .forms import HumanRegistrationForm
from .forms import HumanForm
from .models import Human

class HumanRegisterView(CreateView):
    model = Human
    form_class = HumanRegistrationForm
    template_name = 'humans/register.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class HumanLoginView(LoginView):
    template_name = 'humans/login.html'
    def get_success_url(self):
        return '/'

class HumanLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect('/')
    def get_next_page(self):
        return '/'

class HumanUpdateView(UpdateView):
    model = Human
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'humans/update.html'
    success_url = '/humans/update'
    def get_object(self, queryset=None):
        return self.request.user