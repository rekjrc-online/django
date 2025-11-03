from django.db.models import Q
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import HumanRegistrationForm
from .models import Human, Invitation
from datetime import timedelta
import random

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
    fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
    template_name = 'humans/update.html'
    success_url = '/humans/update'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Calculate hours_remaining for invitation cooldown
        recent_invite = Invitation.objects.filter(
            Q(from_human=user) | Q(to_human=user),
            insertdate__gte=timezone.now() - timedelta(hours=12)
        ).order_by('-insertdate').first()

        hours_remaining = 0
        if recent_invite:
            elapsed = timezone.now() - recent_invite.insertdate
            hours_remaining = max(0, 12 - elapsed.total_seconds() / 3600)
        context['hours_remaining'] = hours_remaining

        return context

class GenerateInvitationView(LoginRequiredMixin, View):
    template_name = 'includes/invitations.html'  # or your template path

    def get(self, request, *args, **kwargs):
        user = request.user

        # Check if user has any invitation in the last 12 hours
        recent_invite = Invitation.objects.filter(
            Q(from_human=user) | Q(to_human=user),
            insertdate__gte=timezone.now() - timedelta(hours=12)
        ).order_by('-insertdate').first()

        hours_remaining = 0
        if recent_invite:
            elapsed = timezone.now() - recent_invite.insertdate
            hours_remaining = max(0, 12 - elapsed.total_seconds() / 3600)

        context = {
            'user': user,
            'hours_remaining': hours_remaining
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user

        # Prevent generation if user is still in 12-hour cooldown
        recent_invite = Invitation.objects.filter(
            Q(from_human=user) | Q(to_human=user),
            insertdate__gte=timezone.now() - timedelta(hours=12)
        ).first()

        if recent_invite:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if not user.invitation_code:
            user.invitation_code = str(random.randint(11111111, 99999999))
            user.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))

class VerifyInvitationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code', '').strip()
        current_user = request.user

        # Validate code
        if not code.isdigit() or len(code) != 8:
            messages.error(request, "Please enter a valid 8-digit code.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Find inviter
        try:
            inviter = Human.objects.get(
                invitation_code=code,
                is_active=True,
                is_verified=True
            )
        except Human.DoesNotExist:
            messages.error(request, "Invalid or inactive invitation code.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if inviter == current_user:
            messages.error(request, "You cannot use your own invitation code.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Step 1: mark current user verified
        current_user.is_verified = True
        current_user.save()

        # Step 2: clear inviter's invitation_code
        inviter.invitation_code = None
        inviter.save()

        # Step 3: create the Invitation record
        try:
            invitation = Invitation.objects.create(
                from_human=inviter,
                to_human=current_user
            )
            print(f"Invitation record created: {invitation.id}")
        except Exception as e:
            print(f"Failed to create invitation record: {e}")
            messages.error(request, "Failed to record invitation in database.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        return redirect(request.META.get('HTTP_REFERER', '/'))