from django.db import models
from humans.models import Human
from profiles.models import Profile
from rekjrc.base_models import BaseModel

class Store(BaseModel):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.PROTECT,
        related_name='store')
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='stores')
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"
