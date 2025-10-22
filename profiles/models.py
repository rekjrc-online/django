from django.db import models
from django.conf import settings
from rekjrc.base_models import BaseModel
from PIL import Image

class Profile(BaseModel):
	PROFILE_TYPE_CHOICES = [
        ('DRIVER', 'Driver'),
        ('MODEL', 'Model'),
        ('STORE', 'Store'),
    ]
	human = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	profiletype = models.CharField(max_length=30, choices=PROFILE_TYPE_CHOICES)
	displayname = models.CharField(max_length=50, default='')
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	location = models.CharField(max_length=100, blank=True)
	website = models.URLField(blank=True)
	followers_count = models.PositiveIntegerField(default=0)
	following_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.displayname
	
	def save(self, *args, **kwargs):
		print('SAAAAAAVE')
		super().save(*args, **kwargs)  # Save first to ensure the image file exists

		if self.avatar:
			img_path = self.avatar.path
			img = Image.open(img_path)

			# Resize if larger than 1024x1024 (you can pick your own size)
			max_size = (1024, 1024)
			img.thumbnail(max_size)

			# Save it back with optimization
			img.save(img_path, optimize=True, quality=85)