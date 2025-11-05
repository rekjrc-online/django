from django.db import models
from rekjrc.base_models import BaseModel
from clubs.models import Club
from events.models import Event
from humans.models import Human
from locations.models import Location
from profiles.models import Profile
from teams.models import Team
from tracks.models import Track

class Race(BaseModel):
    RACE_TYPE_CHOICES = [
        ('Lap Race', 'Lap Race'),
        ('Drag Race', 'Drag Race'),
		('Out and Back', 'Out and Back'),
        ('Long Jump', 'Long Jump')]
    race_type = models.CharField(max_length=30, choices=RACE_TYPE_CHOICES, default='')
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='races',
        null=True,
        blank=True)
    profile = models.OneToOneField(
        Profile,
        on_delete=models.PROTECT,
        related_name='race',
        default=1)
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        related_name='races',
        db_index=True,
        null=True,
        blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='races',
        null=True,
        blank=True)
    track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        related_name='races',
        null=True,
        blank=True)
    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        related_name='races',
        null=True,
        blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name='races',
        null=True,
        blank=True)
    TRANSPONDER_CHOICES = [
        ('LapMonitor','LapMonitor'),
        ('MyLaps','MyLaps')]
    transponder = models.CharField(max_length=10, choices=TRANSPONDER_CHOICES, blank=True)
    def __str__(self):
        return self.profile.displayname

class RaceAttributeEnum(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class RaceAttribute(BaseModel):
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='attributes',
        db_index=True,
        null=True,
        blank=True)
    attribute = models.ForeignKey(
        RaceAttributeEnum,
        on_delete=models.CASCADE,
        related_name='race_attributes')
    value = models.CharField(max_length=255)
    class Meta:
        unique_together = ('race', 'attribute')
    def __str__(self):
        return f"{self.race}: {self.attribute.name} = {self.value}"

class LapMonitorResult(BaseModel):
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='lapmonitor_results',
        db_index=True)
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
        verbose_name = "LapMonitor Result"
        verbose_name_plural = "LapMonitor Results"
        indexes = [
            models.Index(fields=["session_id"]),
            models.Index(fields=["driver_id"]),
            models.Index(fields=["race", "session_id", "driver_id", "lap_index"]),
        ]
    def __str__(self):
        return f"{self.session_name} - {self.driver_name} (Lap {self.lap_index})"

class RaceDriver(BaseModel):
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='race_drivers')
    human = models.ForeignKey(
        Human,
        on_delete=models.CASCADE,
        related_name='race_humans')
    driver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='driver_races',
        null=True,
        blank=True,
        limit_choices_to={'profiletype':'DRIVER'})
    model = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='model_races',
        null=True,
        blank=True,
        limit_choices_to={'profiletype':'MODEL'})
    transponder = models.CharField(max_length=10, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['race', 'model'], name='unique_race_model')]
    def __str__(self):
        human_name = f"{self.human.first_name} {self.human.last_name}" if self.human else '-human-'
        driver_name = self.driver.displayname if self.driver else '-driver-'
        model_name = self.model.displayname if self.model else '-model-'
        return f"Human: {human_name} | Driver: {driver_name} | Model: {model_name}"
