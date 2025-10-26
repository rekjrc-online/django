from django.db import models
from humans.models import Human
from profiles.models import Profile
from locations.models import Location

class Club(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='clubs')
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class ClubLocation(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='clubs')
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='clubs')
    def __str__(self):
        return f"{self.club.name}"

class ClubMember(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='members')
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='club_memberships')
    role = models.CharField(max_length=100, blank=True)
    class Meta:
        unique_together = ('club', 'human')
    def __str__(self):
        role_display = f" ({self.role})" if self.role else ""
        return f"{self.human} @ {self.club}{role_display}"