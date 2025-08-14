from django.urls import path
from . import views

urlpatterns = [
    # Core generation
    path('generate/', views.generate_story, name='generate_story'),
    path('story/<uuid:story_id>/', views.get_story, name='get_story'),
    path('stories/', views.list_stories, name='list_stories'),
    
    # Iterative refinement endpoints
    path('refine/character/', views.refine_character_image, name='refine_character'),
    path('refine/background/', views.refine_background_image, name='refine_background'),
    path('refine/smart/', views.smart_scene_refinement, name='smart_refinement'),
]
