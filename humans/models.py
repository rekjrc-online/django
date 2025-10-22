from django.contrib.auth.models import AbstractUser
from django.db import models
from rekjrc.base_models import BaseModel

class Human(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    def __str__(self):
        return self.username
