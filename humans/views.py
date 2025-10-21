from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .models import Human
from .forms import HumanRegistrationForm

# ------------------------------
# Registration
# ------------------------------
class HumanRegisterView(CreateView):
    model = Human
    form_class = HumanRegistrationForm
    template_name = 'humans/register.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Automatically log in the new user after registration
        login(self.request, self.object)
        return response

# ------------------------------
# Login
# ------------------------------
class HumanLoginView(LoginView):
    template_name = 'humans/login.html'

    def get_success_url(self):
        # Always redirect to homepage after login
        return '/'

# ------------------------------
# Logout
# ------------------------------
class HumanLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        print("=== HUMAN LOGOUT VIEW CALLED ===")
        print("Before logout: user is_authenticated =", request.user.is_authenticated)
        response = super().dispatch(request, *args, **kwargs)
        print("After logout: user is_authenticated =", request.user.is_authenticated)
        print("Redirecting to /")
        return redirect('/')
    
    def get_next_page(self):
        print(">>> get_next_page() called. Returning '/' explicitly.")
        return '/'

class HumanUpdateView(UpdateView):
    model = Human
    fields = ['username', 'email', 'is_verified']  # extend as needed
    template_name = 'humans/update.html'
    success_url = '/'

    def get_object(self, queryset=None):
        # Only allow users to update their own account
        return self.request.user
