from django.db import models
from locations.models import Location
from profiles.models import Profile
from rekjrc.base_models import BaseModel

class TrackType(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Track(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='track', default=1)
    name = models.CharField(max_length=100, unique=True)
    track_type = models.ForeignKey(TrackType, on_delete=models.PROTECT, related_name='tracks')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='tracks')
    def __str__(self):
        return self.name

class TrackAttributeEnum(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class TrackAttribute(BaseModel):
    track = models.ForeignKey(Track, on_delete=models.PROTECT, related_name='attributes')
    attribute_type = models.ForeignKey(TrackAttributeEnum, on_delete=models.PROTECT)
    value = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.attribute_type.name}: {self.value}"
