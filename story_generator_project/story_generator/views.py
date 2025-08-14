# # import logging
# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.core.files.base import ContentFile
# # from .models import StoryGeneration
# # from .langchain_service import StoryGenerationService
# # from .image_service import ImageGenerationService
# # from .serializers import StoryGenerationSerializer
# # import gc

# # logger = logging.getLogger(__name__)

# # @api_view(['POST'])
# # def generate_story(request):
# #     """Main endpoint to generate complete story with images"""
# #     try:
# #         user_prompt = request.data.get('prompt', '').strip()
        
# #         if not user_prompt:
# #             return Response(
# #                 {'error': 'Prompt is required'}, 
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )
        
# #         logger.info(f"Processing request for prompt: {user_prompt[:50]}...")
        
# #         # Create database record
# #         story_obj = StoryGeneration.objects.create(user_prompt=user_prompt)
        
# #         # Initialize services
# #         story_service = StoryGenerationService()
# #         image_service = ImageGenerationService()
        
# #         # Step 1: Generate text content
# #         logger.info("Step 1: Generating story content...")
# #         content = story_service.generate_story_content(user_prompt)
        
# #         # Update database
# #         story_obj.short_story = content['story']
# #         story_obj.character_description = content['character_description']
# #         story_obj.background_description = content['background_description']
# #         story_obj.save()
        
# #         # Step 2: Create image prompts
# #         logger.info("Step 2: Creating image prompts...")
# #         image_prompts = story_service.create_image_prompts(
# #             content['character_description'],
# #             content['background_description']
# #         )
        
# #         # Step 3: Generate images
# #         logger.info("Step 3: Generating character image...")
# #         char_img_bytes = image_service.generate_image(image_prompts['character_prompt'])
        
# #         logger.info("Step 4: Generating background image...")
# #         bg_img_bytes = image_service.generate_image(image_prompts['background_prompt'])
        
# #         # Step 5: Combine images
# #         logger.info("Step 5: Combining images...")
# #         combined_img_bytes = image_service.combine_images(char_img_bytes, bg_img_bytes)
        
# #         # Save images to database
# #         story_obj.character_image.save(
# #             f'char_{story_obj.id}.png',
# #             ContentFile(char_img_bytes.getvalue()),
# #             save=False
# #         )
        
# #         story_obj.background_image.save(
# #             f'bg_{story_obj.id}.png',
# #             ContentFile(bg_img_bytes.getvalue()),
# #             save=False
# #         )
        
# #         story_obj.combined_image.save(
# #             f'combined_{story_obj.id}.jpg',
# #             ContentFile(combined_img_bytes.getvalue()),
# #             save=False
# #         )
        
# #         story_obj.save()
        
# #         # Clean up memory
# #         del story_service, image_service
# #         gc.collect()
        
# #         logger.info("Story generation completed successfully")
        
# #         # Return response
# #         serializer = StoryGenerationSerializer(story_obj)
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# #     except Exception as e:
# #         logger.error(f"Error in generate_story: {str(e)}")
# #         return Response(
# #             {'error': f'Internal server error: {str(e)}'}, 
# #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
# #         )

# # @api_view(['GET'])
# # def get_story(request, story_id):
# #     """Get a specific story by ID"""
# #     try:
# #         story = StoryGeneration.objects.get(id=story_id)
# #         serializer = StoryGenerationSerializer(story)
# #         return Response(serializer.data)
# #     except StoryGeneration.DoesNotExist:
# #         return Response(
# #             {'error': 'Story not found'}, 
# #             status=status.HTTP_404_NOT_FOUND
# #         )

# # @api_view(['GET'])
# # def list_stories(request):
# #     """List all generated stories"""
# #     stories = StoryGeneration.objects.all()[:20]  # Limit to 20 recent stories
# #     serializer = StoryGenerationSerializer(stories, many=True)
# #     return Response(serializer.data)

# import logging
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.files.base import ContentFile
# from .models import StoryGeneration
# from .langchain_service import StoryGenerationService
# from .image_service import ImageGenerationService
# from .serializers import StoryGenerationSerializer
# import gc

# logger = logging.getLogger(__name__)

# @api_view(['POST'])
# def generate_story(request):
#     """Main endpoint to generate complete story with images"""
#     image_service = None  # Initialize outside try block
    
#     try:
#         user_prompt = request.data.get('prompt', '').strip()
        
#         if not user_prompt:
#             return Response(
#                 {'error': 'Prompt is required'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         logger.info(f"Processing request for prompt: {user_prompt[:50]}...")
        
#         # Create database record
#         story_obj = StoryGeneration.objects.create(user_prompt=user_prompt)
        
#         # Initialize services
#         story_service = StoryGenerationService()
#         image_service = ImageGenerationService()
        
#         # Step 1: Generate text content
#         logger.info("Step 1: Generating story content...")
#         content = story_service.generate_story_content(user_prompt)
        
#         # Update database
#         story_obj.short_story = content['story']
#         story_obj.character_description = content['character_description']
#         story_obj.background_description = content['background_description']
#         story_obj.save()
        
#         # Step 2: Create image prompts
#         logger.info("Step 2: Creating image prompts...")
#         image_prompts = story_service.create_image_prompts(
#             content['character_description'],
#             content['background_description']
#         )
        
#         # Step 3: Generate images
#         print(image_prompts['character_prompt'])
#         logger.info("Step 3: Generating character image...")
#         char_img_bytes = image_service.generate_image(image_prompts['character_prompt'])
        
#         print(image_prompts['background_prompt'])
#         logger.info("Step 4: Generating background image...")
#         bg_img_bytes = image_service.generate_image(image_prompts['background_prompt'])
        
#         # Step 5: Combine images
#         logger.info("Step 5: Combining images...")
#         combined_img_bytes = image_service.combine_images(char_img_bytes, bg_img_bytes)
        
#         # Save images to database
#         story_obj.character_image.save(
#             f'char_{story_obj.id}.png',
#             ContentFile(char_img_bytes.getvalue()),
#             save=False
#         )
        
#         story_obj.background_image.save(
#             f'bg_{story_obj.id}.png',
#             ContentFile(bg_img_bytes.getvalue()),
#             save=False
#         )
        
#         story_obj.combined_image.save(
#             f'combined_{story_obj.id}.jpg',
#             ContentFile(combined_img_bytes.getvalue()),
#             save=False
#         )
        
#         story_obj.save()
        
#         logger.info("Story generation completed successfully")
        
#         # Return response
#         serializer = StoryGenerationSerializer(story_obj)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#     except Exception as e:
#         logger.error(f"Error in generate_story: {str(e)}")
#         return Response(
#             {'error': f'Internal server error: {str(e)}'}, 
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
    
#     finally:
#         # CRITICAL: Clean up memory after each request
#         try:
#             if image_service is not None:
#                 image_service.cleanup()
#                 logger.info("Image service cleaned up successfully")
            
#             # Clean up other services
#             if 'story_service' in locals():
#                 del story_service
            
#             # Force garbage collection
#             gc.collect()
            
#         except Exception as cleanup_error:
#             logger.error(f"Error during cleanup: {str(cleanup_error)}")
#             # Don't fail the request due to cleanup errors

# @api_view(['GET'])
# def get_story(request, story_id):
#     """Get a specific story by ID"""
#     try:
#         story = StoryGeneration.objects.get(id=story_id)
#         serializer = StoryGenerationSerializer(story)
#         return Response(serializer.data)
#     except StoryGeneration.DoesNotExist:
#         return Response(
#             {'error': 'Story not found'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )

# @api_view(['GET'])
# def list_stories(request):
#     """List all generated stories"""
#     stories = StoryGeneration.objects.all()[:20]  # Limit to 20 recent stories
#     serializer = StoryGenerationSerializer(stories, many=True)
#     return Response(serializer.data)


import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from io import BytesIO
from .models import StoryGeneration
from .langchain_service import StoryGenerationService
from .image_service import ImageGenerationService
from .serializers import StoryGenerationSerializer
import gc

logger = logging.getLogger(__name__)

@api_view(['POST'])
def generate_story(request):
    """Main endpoint to generate complete story with images"""
    image_service = None
    
    try:
        user_prompt = request.data.get('prompt', '').strip()
        
        if not user_prompt:
            return Response(
                {'error': 'Prompt is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Processing request for prompt: {user_prompt[:50]}...")
        
        # Create database record
        story_obj = StoryGeneration.objects.create(user_prompt=user_prompt)
        
        # Initialize services
        story_service = StoryGenerationService()
        image_service = ImageGenerationService()
        
        # Step 1: Generate text content
        logger.info("Step 1: Generating story content...")
        content = story_service.generate_story_content(user_prompt)
        
        # Update database
        story_obj.short_story = content['story']
        story_obj.character_description = content['character_description']
        story_obj.background_description = content['background_description']
        story_obj.save()
        
        # Step 2: Create image prompts
        logger.info("Step 2: Creating image prompts...")
        image_prompts = story_service.create_image_prompts(
            content['character_description'],
            content['background_description']
        )
        
        # Step 3: Generate images
        logger.info("Step 3: Generating character image...")
        char_img_bytes = image_service.generate_image(image_prompts['character_prompt'])
        
        logger.info("Step 4: Generating background image...")
        bg_img_bytes = image_service.generate_image(image_prompts['background_prompt'])
        
        # Step 5: Combine images
        logger.info("Step 5: Combining images...")
        combined_img_bytes = image_service.combine_images(char_img_bytes, bg_img_bytes)
        
        # Save images to database
        story_obj.character_image.save(
            f'char_{story_obj.id}.png',
            ContentFile(char_img_bytes.getvalue()),
            save=False
        )
        
        story_obj.background_image.save(
            f'bg_{story_obj.id}.png',
            ContentFile(bg_img_bytes.getvalue()),
            save=False
        )
        
        story_obj.combined_image.save(
            f'combined_{story_obj.id}.jpg',
            ContentFile(combined_img_bytes.getvalue()),
            save=False
        )
        
        story_obj.save()
        
        logger.info("Story generation completed successfully")
        
        # Return response
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error in generate_story: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        # CRITICAL: Clean up memory after each request
        try:
            if image_service is not None:
                image_service.cleanup()
                logger.info("Image service cleaned up successfully")
            
            # Clean up other services
            if 'story_service' in locals():
                del story_service
            
            # Force garbage collection
            gc.collect()
            
        except Exception as cleanup_error:
            logger.error(f"Error during cleanup: {str(cleanup_error)}")
            # Don't fail the request due to cleanup errors

@api_view(['GET'])
def get_story(request, story_id):
    """Get a specific story by ID"""
    try:
        story = StoryGeneration.objects.get(id=story_id)
        serializer = StoryGenerationSerializer(story)
        return Response(serializer.data)
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def list_stories(request):
    """List all generated stories"""
    stories = StoryGeneration.objects.all()[:20]  # Limit to 20 recent stories
    serializer = StoryGenerationSerializer(stories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def refine_character_image(request):
    """Refine character image based on feedback"""
    image_service = None
    
    try:
        story_id = request.data.get('story_id')
        refinement_prompt = request.data.get('refinement_prompt', '').strip()
        strength = float(request.data.get('strength', 0.4))
        
        if not story_id or not refinement_prompt:
            return Response(
                {'error': 'story_id and refinement_prompt are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate strength parameter
        if not 0.1 <= strength <= 0.9:
            return Response(
                {'error': 'strength must be between 0.1 and 0.9'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Refining character for story {story_id} with strength {strength}")
        
        # Get existing story
        story_obj = StoryGeneration.objects.get(id=story_id)
        
        if not story_obj.character_image:
            return Response(
                {'error': 'No character image found to refine'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize image service
        image_service = ImageGenerationService()
        
        # Read existing character image
        story_obj.character_image.seek(0)
        char_img_bytes = BytesIO(story_obj.character_image.read())
        
        # Refine the image
        refined_img_bytes = image_service.refine_image(
            char_img_bytes, 
            refinement_prompt, 
            strength
        )
        
        # Save refined image (keep original with version number)
        story_obj.character_image.save(
            f'char_refined_{story_obj.id}.png',
            ContentFile(refined_img_bytes.getvalue()),
            save=False
        )
        
        # Re-generate combined image with refined character
        if story_obj.background_image:
            story_obj.background_image.seek(0)
            bg_img_bytes = BytesIO(story_obj.background_image.read())
            
            combined_img_bytes = image_service.combine_images(refined_img_bytes, bg_img_bytes)
            
            story_obj.combined_image.save(
                f'combined_refined_{story_obj.id}.jpg',
                ContentFile(combined_img_bytes.getvalue()),
                save=False
            )
        
        story_obj.save()
        
        logger.info("Character image refined successfully")
        
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as e:
        return Response(
            {'error': f'Invalid parameter: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error refining character image: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        if image_service is not None:
            image_service.cleanup()
        gc.collect()

@api_view(['POST'])
def refine_background_image(request):
    """Refine background image based on feedback"""
    image_service = None
    
    try:
        story_id = request.data.get('story_id')
        refinement_prompt = request.data.get('refinement_prompt', '').strip()
        strength = float(request.data.get('strength', 0.4))
        
        if not story_id or not refinement_prompt:
            return Response(
                {'error': 'story_id and refinement_prompt are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate strength parameter
        if not 0.1 <= strength <= 0.9:
            return Response(
                {'error': 'strength must be between 0.1 and 0.9'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Refining background for story {story_id} with strength {strength}")
        
        # Get existing story
        story_obj = StoryGeneration.objects.get(id=story_id)
        
        if not story_obj.background_image:
            return Response(
                {'error': 'No background image found to refine'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize image service
        image_service = ImageGenerationService()
        
        # Read existing background image
        story_obj.background_image.seek(0)
        bg_img_bytes = BytesIO(story_obj.background_image.read())
        
        # Refine the image
        refined_img_bytes = image_service.refine_image(
            bg_img_bytes, 
            refinement_prompt, 
            strength
        )
        
        # Save refined image
        story_obj.background_image.save(
            f'bg_refined_{story_obj.id}.png',
            ContentFile(refined_img_bytes.getvalue()),
            save=False
        )
        
        # Re-generate combined image with refined background
        if story_obj.character_image:
            story_obj.character_image.seek(0)
            char_img_bytes = BytesIO(story_obj.character_image.read())
            
            combined_img_bytes = image_service.combine_images(char_img_bytes, refined_img_bytes)
            
            story_obj.combined_image.save(
                f'combined_refined_{story_obj.id}.jpg',
                ContentFile(combined_img_bytes.getvalue()),
                save=False
            )
        
        story_obj.save()
        
        logger.info("Background image refined successfully")
        
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as e:
        return Response(
            {'error': f'Invalid parameter: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error refining background image: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        if image_service is not None:
            image_service.cleanup()
        gc.collect()

@api_view(['POST'])
def smart_scene_refinement(request):
    """Smart refinement - character and background learn from each other"""
    image_service = None
    
    try:
        story_id = request.data.get('story_id')
        character_adjustments = request.data.get('character_adjustments', '').strip()
        background_adjustments = request.data.get('background_adjustments', '').strip()
        
        if not story_id:
            return Response(
                {'error': 'story_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not character_adjustments and not background_adjustments:
            return Response(
                {'error': 'At least one adjustment (character_adjustments or background_adjustments) is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Smart scene refinement for story {story_id}")
        
        # Get existing story
        story_obj = StoryGeneration.objects.get(id=story_id)
        
        if not story_obj.character_image or not story_obj.background_image:
            return Response(
                {'error': 'Both character and background images required for smart refinement'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize image service
        image_service = ImageGenerationService()
        
        # Read existing images
        story_obj.character_image.seek(0)
        char_img_bytes = BytesIO(story_obj.character_image.read())
        
        story_obj.background_image.seek(0)
        bg_img_bytes = BytesIO(story_obj.background_image.read())
        
        # Smart refinements
        if character_adjustments:
            logger.info("Applying smart character refinement...")
            char_img_bytes = image_service.refine_character_for_scene(
                char_img_bytes, bg_img_bytes, character_adjustments
            )
            
            # Save refined character
            story_obj.character_image.save(
                f'char_smart_{story_obj.id}.png',
                ContentFile(char_img_bytes.getvalue()),
                save=False
            )
        
        if background_adjustments:
            logger.info("Applying smart background refinement...")
            bg_img_bytes = image_service.refine_background_for_character(
                bg_img_bytes, char_img_bytes, background_adjustments
            )
            
            # Save refined background
            story_obj.background_image.save(
                f'bg_smart_{story_obj.id}.png',
                ContentFile(bg_img_bytes.getvalue()),
                save=False
            )
        
        # Generate new combined image
        logger.info("Generating new combined image...")
        combined_img_bytes = image_service.combine_images(char_img_bytes, bg_img_bytes)
        
        story_obj.combined_image.save(
            f'combined_smart_{story_obj.id}.jpg',
            ContentFile(combined_img_bytes.getvalue()),
            save=False
        )
        
        story_obj.save()
        
        logger.info("Smart scene refinement completed successfully")
        
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error in smart scene refinement: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        if image_service is not None:
            image_service.cleanup()
        gc.collect()

@api_view(['POST'])
def regenerate_character(request):
    """Completely regenerate character image with new prompt"""
    image_service = None
    
    try:
        story_id = request.data.get('story_id')
        new_character_prompt = request.data.get('character_prompt', '').strip()
        
        if not story_id or not new_character_prompt:
            return Response(
                {'error': 'story_id and character_prompt are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Regenerating character for story {story_id}")
        
        # Get existing story
        story_obj = StoryGeneration.objects.get(id=story_id)
        
        # Initialize image service
        image_service = ImageGenerationService()
        
        # Generate new character image
        new_char_img_bytes = image_service.generate_image(new_character_prompt)
        
        # Save new character image
        story_obj.character_image.save(
            f'char_regen_{story_obj.id}.png',
            ContentFile(new_char_img_bytes.getvalue()),
            save=False
        )
        
        # Re-generate combined image if background exists
        if story_obj.background_image:
            story_obj.background_image.seek(0)
            bg_img_bytes = BytesIO(story_obj.background_image.read())
            
            combined_img_bytes = image_service.combine_images(new_char_img_bytes, bg_img_bytes)
            
            story_obj.combined_image.save(
                f'combined_regen_{story_obj.id}.jpg',
                ContentFile(combined_img_bytes.getvalue()),
                save=False
            )
        
        story_obj.save()
        
        logger.info("Character regenerated successfully")
        
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error regenerating character: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        if image_service is not None:
            image_service.cleanup()
        gc.collect()

@api_view(['POST'])
def regenerate_background(request):
    """Completely regenerate background image with new prompt"""
    image_service = None
    
    try:
        story_id = request.data.get('story_id')
        new_background_prompt = request.data.get('background_prompt', '').strip()
        
        if not story_id or not new_background_prompt:
            return Response(
                {'error': 'story_id and background_prompt are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Regenerating background for story {story_id}")
        
        # Get existing story
        story_obj = StoryGeneration.objects.get(id=story_id)
        
        # Initialize image service
        image_service = ImageGenerationService()
        
        # Generate new background image
        new_bg_img_bytes = image_service.generate_image(new_background_prompt)
        
        # Save new background image
        story_obj.background_image.save(
            f'bg_regen_{story_obj.id}.png',
            ContentFile(new_bg_img_bytes.getvalue()),
            save=False
        )
        
        # Re-generate combined image if character exists
        if story_obj.character_image:
            story_obj.character_image.seek(0)
            char_img_bytes = BytesIO(story_obj.character_image.read())
            
            combined_img_bytes = image_service.combine_images(char_img_bytes, new_bg_img_bytes)
            
            story_obj.combined_image.save(
                f'combined_regen_{story_obj.id}.jpg',
                ContentFile(combined_img_bytes.getvalue()),
                save=False
            )
        
        story_obj.save()
        
        logger.info("Background regenerated successfully")
        
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error regenerating background: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        if image_service is not None:
            image_service.cleanup()
        gc.collect()

@api_view(['POST'])
def regenerate_combined_image(request):
    """Regenerate combined image from existing character and background"""
    image_service = None
    
    try:
        story_id = request.data.get('story_id')
        
        if not story_id:
            return Response(
                {'error': 'story_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Regenerating combined image for story {story_id}")
        
        # Get existing story
        story_obj = StoryGeneration.objects.get(id=story_id)
        
        if not story_obj.character_image or not story_obj.background_image:
            return Response(
                {'error': 'Both character and background images are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize image service
        image_service = ImageGenerationService()
        
        # Read existing images
        story_obj.character_image.seek(0)
        char_img_bytes = BytesIO(story_obj.character_image.read())
        
        story_obj.background_image.seek(0)
        bg_img_bytes = BytesIO(story_obj.background_image.read())
        
        # Regenerate combined image
        combined_img_bytes = image_service.combine_images(char_img_bytes, bg_img_bytes)
        
        # Save new combined image
        story_obj.combined_image.save(
            f'combined_new_{story_obj.id}.jpg',
            ContentFile(combined_img_bytes.getvalue()),
            save=False
        )
        
        story_obj.save()
        
        logger.info("Combined image regenerated successfully")
        
        serializer = StoryGenerationSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except StoryGeneration.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error regenerating combined image: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    finally:
        if image_service is not None:
            image_service.cleanup()
        gc.collect()