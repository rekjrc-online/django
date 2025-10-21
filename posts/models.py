from django.db import models
from django.conf import settings
from rekjrc.base_models import BaseModel
from profiles.models import Profile

class Post(BaseModel):
    human_id = models.ForeignKey (
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='posts',
        db_index=True )
    profile_id = models.ForeignKey (
        Profile,
        on_delete=models.PROTECT,
        related_name='posts',
        db_index=True )
    content = models.TextField(max_length=200)
    # Optional media attachments
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    # Engagement metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    reposts_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.profile_id.displayname}: {self.content[:50]}"
