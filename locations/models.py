from django.db import models
from profiles.models import Profile
from rekjrc.base_models import BaseModel
from humans.models import Human

# Create your models here.
class Location(BaseModel):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='locations',
        null=True,
        blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='locations')
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"
