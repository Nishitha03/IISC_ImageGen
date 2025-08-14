from django.contrib import admin
from .models import StoryGeneration

@admin.register(StoryGeneration)
class StoryGenerationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_prompt', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_prompt', 'short_story')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Input', {
            'fields': ('user_prompt',)
        }),
        ('Generated Content', {
            'fields': ('short_story', 'character_description', 'background_description')
        }),
        ('Images', {
            'fields': ('character_image', 'background_image', 'combined_image')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at')
        }),
    )