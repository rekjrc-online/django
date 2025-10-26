from django.db import models
from django.utils import timezone
from locations.models import Location
from humans.models import Human

class Event(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='events')
    name = models.CharField(max_length=100)
    eventdate = models.DateTimeField(default=timezone.now)
    multiday = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"

class EventInterest(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='interests')
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='event_interests')
    note = models.CharField(max_length=255, blank=True)  # optional note
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'human')

    def __str__(self):
        return f"{self.human} interested in {self.event}"