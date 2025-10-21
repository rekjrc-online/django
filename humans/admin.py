from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Human

class HumanAdmin(UserAdmin):
    model = Human
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_verified', 'last_login_ip')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'is_active')

    # This controls the “Add Human” page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('first_name', 'last_name', 'email', 'is_verified', 'last_login_ip')}),
    )

admin.site.register(Human, HumanAdmin)
