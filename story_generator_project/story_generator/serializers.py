from rest_framework import serializers
from .models import StoryGeneration

class StoryGenerationSerializer(serializers.ModelSerializer):
    character_image_url = serializers.SerializerMethodField()
    background_image_url = serializers.SerializerMethodField()
    combined_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StoryGeneration
        fields = [
            'id', 'user_prompt', 'short_story', 'character_description',
            'background_description', 'character_image_url', 
            'background_image_url', 'combined_image_url', 'created_at'
        ]
    
    def get_character_image_url(self, obj):
        if obj.character_image:
            return obj.character_image.url
        return None
    
    def get_background_image_url(self, obj):
        if obj.background_image:
            return obj.background_image.url
        return None
    
    def get_combined_image_url(self, obj):
        if obj.combined_image:
            return obj.combined_image.url
        return None
