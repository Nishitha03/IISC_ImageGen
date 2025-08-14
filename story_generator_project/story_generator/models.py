from django.db import models
import uuid

class StoryGeneration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_prompt = models.TextField()
    short_story = models.TextField(blank=True)
    character_description = models.TextField(blank=True)
    background_description = models.TextField(blank=True)
    character_image = models.ImageField(upload_to='characters/', blank=True, null=True)
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    combined_image = models.ImageField(upload_to='combined/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']