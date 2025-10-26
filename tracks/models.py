from django.db import models
from locations.models import Location

class TrackType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=100, unique=True)
    track_type = models.ForeignKey(
        TrackType,
        on_delete=models.PROTECT,
        related_name='tracks')
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='tracks')
    def __str__(self):
        return self.name

class TrackAttributeEnum(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class TrackAttribute(models.Model):
    track = models.ForeignKey(
        Track,
        on_delete=models.PROTECT,
        related_name='attributes')
    attribute_type = models.ForeignKey(
        TrackAttributeEnum,
        on_delete=models.PROTECT)
    value = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.attribute_type.name}: {self.value}"
