from django.db import models
from humans.models import Human
from profiles.models import Profile
from rekjrc.base_models import BaseModel

# Create your models here.
class Team(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='teams')
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    def __str__(self):
        return f"{self.name}"

class TeamMember(BaseModel):
    Team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='members')
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='Team_memberships')
    role = models.CharField(max_length=100, blank=True)
    class Meta:
        unique_together = ('Team', 'human')
    def __str__(self):
        role_display = f" ({self.role})" if self.role else ""
        return f"{self.human} @ {self.Team}{role_display}"