from django.db import models
from clubs.models import Club
from teams.models import Team
from events.models import Event
from humans.models import Human
from profiles.models import Profile
from locations.models import Location
from tracks.models import Track

class Race(models.Model):
    RACE_TYPE_CHOICES = [
        ('Lap Race', 'Lap Race'),
        ('Drag Race', 'Drag Race'),
		('Out and Back', 'Out and Back'),
        ('Long Jump', 'Long Jump'),
    ]
    race_type = models.CharField(max_length=30, choices=RACE_TYPE_CHOICES, default='')
    profile = models.OneToOneField(
        Profile,
        on_delete=models.PROTECT,
        related_name='race',
        default=1
    )
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='races',
        default=1
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='races',
        db_index=True,
        null=True,
        blank=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='races',
        null=True,
        blank=True
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.PROTECT,
        related_name='races',
        null=True,
        blank=True)
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='races',
        null=True,
        blank=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='races',
        null=True,
        blank=True
    )
    def __str__(self):
        return f"Race for {self.event or 'No Event'}"

class RaceAttributeEnum(models.Model):
    """
    Lookup table for race attributes.  
    This model defines the possible attribute types that a race can have, like 'Track Surface' or 'Lap Count'.

    Fields:
        name (CharField): The name of the attribute. Must be unique.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RaceAttribute(models.Model):
    """
    Stores specific attribute values for a race.  
    Each entry links a race to an attribute type (from RaceAttributeEnum) and a value.

    Fields:
        race (ForeignKey): The race this attribute belongs to.
        attribute (ForeignKey): The attribute type (from RaceAttributeEnum).
        value (CharField): The value of the attribute for this race.

    Constraints:
        unique_together (race, attribute): Ensures that each race can only have one entry per attribute type.
    """
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='attributes',
        db_index=True
    )
    attribute = models.ForeignKey(
        RaceAttributeEnum,
        on_delete=models.PROTECT,
        related_name='race_attributes'
    )
    value = models.CharField(max_length=255)
    class Meta:
        unique_together = ('race', 'attribute')
    def __str__(self):
        return f"{self.race}: {self.attribute.name} = {self.value}"

class LapMonitorResult(models.Model):
    session_id = models.UUIDField()
    session_name = models.CharField(max_length=100)
    session_date = models.DateTimeField()
    session_kind = models.CharField(max_length=50)
    session_duration = models.FloatField()
    driver_id = models.UUIDField()
    driver_name = models.CharField(max_length=100)
    driver_transponder_id = models.CharField(max_length=50)
    driver_rank = models.IntegerField()
    lap_index = models.IntegerField()
    lap_end_time = models.FloatField()
    lap_duration = models.FloatField()
    lap_kind = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Lap Monitor Result"
        verbose_name_plural = "Lap Monitor Results"
        indexes = [
            models.Index(fields=["session_id"]),
            models.Index(fields=["driver_id"]),
        ]
    def __str__(self):
        return f"{self.session_name} - {self.driver_name} (Lap {self.lap_index})"
