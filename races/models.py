from django.db import models
from events.models import Event

# Create your models here.
class Race(models.Model):
    event_id = models.ForeignKey (
        Event,
        on_delete=models.PROTECT,
        related_name='races',
        db_index=True )
    def __str__(self):
        return f"{self.event_id}"
