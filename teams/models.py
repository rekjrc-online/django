from django.db import models
from profiles.models import Profile

# Create your models here.
class Team(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='teams')
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    def __str__(self):
        return f"{self.name}"
