from django.contrib.auth.models import AbstractUser
from django.db import models
from rekjrc.base_models import BaseModel

class Human(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # For verified accounts
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    # AbstractUser already has username, password, first_name, last_name

    def __str__(self):
        return self.username
