from django.db import models
from humans.models import Human
from profiles.models import Profile

class Build(models.Model):
    human = models.ForeignKey(Human, on_delete=models.PROTECT, related_name='builds')
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='builds')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.name} ({self.profile.displayname})"

class BuildAttributeEnum(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class BuildAttribute(models.Model):
    build = models.ForeignKey(Build, on_delete=models.PROTECT, related_name='attributes')
    attribute_type = models.ForeignKey(BuildAttributeEnum, on_delete=models.PROTECT)
    value = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.attribute_type.name}: {self.value}"
