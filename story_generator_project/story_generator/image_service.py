
# import logging
# import torch
# import gc
# import numpy as np
# from PIL import Image
# from io import BytesIO
# from django.conf import settings
# from django.core.files.base import ContentFile
# from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
# from rembg import remove, new_session
# import warnings

# # Suppress warnings for cleaner output
# warnings.filterwarnings("ignore")

# logger = logging.getLogger(__name__)

# class ImageGenerationService:
#     def __init__(self):
#         # Initialize diffusers pipeline
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.pipeline = None
#         self.img2img_pipeline = None
#         self.model_id = "runwayml/stable-diffusion-v1-5"

#         # Initialize rembg session for background removal
#         try:
#             self.rembg_session = new_session('u2net')
#             logger.info("✓ rembg session initialized for background removal")
#         except Exception as e:
#             logger.warning(f"rembg initialization failed: {e}")
#             self.rembg_session = None
        
#         logger.info(f"Initializing ImageService on device: {self.device}")
        
#         # Initialize pipelines
#         self._initialize_pipelines()
    
#     def _initialize_pipelines(self):
#         """Initialize both text2img and img2img pipelines"""
#         try:
#             logger.info("Loading Stable Diffusion models...")
            
#             # Text-to-Image Pipeline
#             try:
#                 self.pipeline = StableDiffusionPipeline.from_pretrained(
#                     self.model_id,
#                     torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#                     use_safetensors=True,
#                     variant="fp16" if self.device == "cuda" else None
#                 )
#                 logger.info("✓ Text2Img pipeline loaded")
#             except Exception as e:
#                 logger.warning(f"Optimized loading failed: {e}")
#                 self.pipeline = StableDiffusionPipeline.from_pretrained(
#                     self.model_id,
#                     torch_dtype=torch.float32
#                 )
#                 logger.info("✓ Text2Img pipeline loaded (fallback)")
            
#             # Image-to-Image Pipeline for iterative refinement
#             try:
#                 self.img2img_pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
#                     self.model_id,
#                     torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#                     use_safetensors=True,
#                     variant="fp16" if self.device == "cuda" else None
#                 )
#                 logger.info("✓ Img2Img pipeline loaded")
#             except Exception as e:
#                 logger.warning(f"Img2Img loading failed: {e}")
#                 self.img2img_pipeline = None
            
#             # Use faster scheduler for both
#             for pipeline in [self.pipeline, self.img2img_pipeline]:
#                 if pipeline is not None:
#                     try:
#                         pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
#                             pipeline.scheduler.config
#                         )
#                     except Exception as e:
#                         logger.warning(f"Could not set faster scheduler: {e}")
                    
#                     # Move to device
#                     pipeline = pipeline.to(self.device)
                    
#                     # Memory optimizations
#                     if self.device == "cuda":
#                         try:
#                             if hasattr(pipeline, 'enable_model_cpu_offload'):
#                                 pipeline.enable_model_cpu_offload()
#                             if hasattr(pipeline, 'enable_attention_slicing'):
#                                 pipeline.enable_attention_slicing()
#                             if hasattr(pipeline, 'enable_vae_slicing'):
#                                 pipeline.enable_vae_slicing()
#                         except Exception as opt_error:
#                             logger.warning(f"Memory optimizations failed: {opt_error}")
            
#             logger.info("🎉 All pipelines loaded successfully!")
            
#         except Exception as e:
#             logger.error(f"Failed to initialize pipelines: {str(e)}")
#             logger.info("💡 Will use placeholder images instead")
#             self.pipeline = None
#             self.img2img_pipeline = None
    
#     def generate_image(self, prompt: str) -> BytesIO:
#         """Generate image using Diffusers Stable Diffusion"""
#         try:
#             if self.pipeline is None:
#                 logger.warning("Pipeline not available, using placeholder")
#                 return self._create_placeholder_image(prompt)
            
#             logger.info(f"Generating image for: {prompt[:50]}...")
            
#             # Clean and optimize prompt
#             clean_prompt = self._optimize_prompt(prompt)
            
#             # Generate image
#             with torch.inference_mode():
#                 result = self.pipeline(
#                     prompt=clean_prompt,
#                     negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
#                     num_inference_steps=20,
#                     guidance_scale=7.5,
#                     width=512,
#                     height=512,
#                     generator=torch.Generator(device=self.device).manual_seed(42)
#                 )
            
#             # Convert to BytesIO
#             image = result.images[0]
#             buffer = BytesIO()
#             image.save(buffer, format='PNG', quality=95)
#             buffer.seek(0)
            
#             # Clean up GPU memory
#             if self.device == "cuda":
#                 torch.cuda.empty_cache()
#             gc.collect()
            
#             logger.info("✅ Image generated successfully!")
#             return buffer
            
#         except Exception as e:
#             logger.error(f"Error generating image: {str(e)}")
#             return self._create_placeholder_image(prompt)
    
#     def refine_image(self, image_bytes: BytesIO, refinement_prompt: str, strength: float = 0.4) -> BytesIO:
#         """Refine existing image using img2img - for iterative improvement"""
#         try:
#             if self.img2img_pipeline is None:
#                 logger.warning("Img2Img pipeline not available")
#                 return image_bytes  # Return original if can't refine
            
#             logger.info(f"Refining image with: {refinement_prompt[:50]}... (strength: {strength})")
            
#             # Load existing image
#             image_bytes.seek(0)
#             existing_image = Image.open(image_bytes).convert('RGB')
#             existing_image = existing_image.resize((512, 512), Image.Resampling.LANCZOS)
            
#             # Clean prompt
#             clean_prompt = self._optimize_prompt(refinement_prompt)
            
#             # Refine using img2img
#             with torch.inference_mode():
#                 result = self.img2img_pipeline(
#                     prompt=clean_prompt,
#                     image=existing_image,
#                     strength=strength,  # How much to change (0.1=small, 0.9=big changes)
#                     negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
#                     num_inference_steps=20,
#                     guidance_scale=7.5,
#                     generator=torch.Generator(device=self.device).manual_seed(42)
#                 )
            
#             # Convert to BytesIO
#             refined_image = result.images[0]
#             buffer = BytesIO()
#             refined_image.save(buffer, format='PNG', quality=95)
#             buffer.seek(0)
            
#             # Clean up
#             existing_image.close()
#             refined_image.close()
#             if self.device == "cuda":
#                 torch.cuda.empty_cache()
#             gc.collect()
            
#             logger.info("✅ Image refined successfully!")
#             return buffer
            
#         except Exception as e:
#             logger.error(f"Error refining image: {str(e)}")
#             return image_bytes  # Return original on error
    
#     def refine_character_for_scene(self, character_img_bytes: BytesIO, background_img_bytes: BytesIO, 
#                                  character_adjustments: str) -> BytesIO:
#         """Refine character image to better fit the scene"""
#         try:
#             logger.info("🎨 Refining character to match scene...")
            
#             # Analyze background for context
#             background_img_bytes.seek(0)
#             bg_img = Image.open(background_img_bytes).convert('RGB')
#             scene_context = self._analyze_scene_context(bg_img)
            
#             # Create scene-aware refinement prompt
#             refinement_prompt = f"{character_adjustments}, {scene_context['lighting']}, {scene_context['style']}"
            
#             # Refine character with scene context
#             refined_character = self.refine_image(
#                 character_img_bytes, 
#                 refinement_prompt, 
#                 strength=0.3  # Moderate changes to maintain character
#             )
            
#             logger.info("✅ Character refined for scene compatibility")
#             return refined_character
            
#         except Exception as e:
#             logger.error(f"Error refining character for scene: {str(e)}")
#             return character_img_bytes
    
#     def refine_background_for_character(self, background_img_bytes: BytesIO, character_img_bytes: BytesIO,
#                                       background_adjustments: str) -> BytesIO:
#         """Refine background to better accommodate the character"""
#         try:
#             logger.info("🏞️ Refining background for character placement...")
            
#             # Analyze character for context
#             character_img_bytes.seek(0)
#             char_img = Image.open(character_img_bytes).convert('RGB')
#             char_context = self._analyze_character_context(char_img)
            
#             # Create character-aware refinement prompt
#             refinement_prompt = f"{background_adjustments}, clear center space, {char_context['scale']}, {char_context['perspective']}"
            
#             # Refine background with character context
#             refined_background = self.refine_image(
#                 background_img_bytes,
#                 refinement_prompt,
#                 strength=0.4  # More changes allowed for background
#             )
            
#             logger.info("✅ Background refined for character compatibility")
#             return refined_background
            
#         except Exception as e:
#             logger.error(f"Error refining background for character: {str(e)}")
#             return background_img_bytes
    
#     def _analyze_scene_context(self, bg_img: Image.Image) -> dict:
#         """Analyze background image to determine lighting and style context"""
#         # Convert to numpy for analysis
#         img_array = np.array(bg_img)
        
#         # Calculate average brightness
#         brightness = np.mean(img_array)
        
#         # Determine lighting style
#         if brightness < 100:
#             lighting = "dark moody lighting, shadows"
#         elif brightness > 180:
#             lighting = "bright natural lighting, warm tones"
#         else:
#             lighting = "balanced lighting, natural"
        
#         # Determine general style (simple heuristic)
#         # More sophisticated analysis could be added here
#         style = "realistic digital art style"
        
#         return {
#             'lighting': lighting,
#             'style': style,
#             'brightness': brightness
#         }
    
#     def _analyze_character_context(self, char_img: Image.Image) -> dict:
#         """Analyze character image to determine scale and perspective needs"""
#         # Simple analysis - more sophisticated methods could be added
#         return {
#             'scale': 'human scale proportions',
#             'perspective': 'eye level perspective',
#             'style': 'realistic character art'
#         }
    
#     def _optimize_prompt(self, prompt: str) -> str:
#         """Optimize prompt for better Stable Diffusion results"""
#         clean_prompt = prompt.replace("Portrait of ", "").replace("Scene: ", "")
        
#         if "character" in prompt.lower() or "portrait" in prompt.lower():
#             clean_prompt += ", portrait, detailed, high quality, digital art"
#         elif "background" in prompt.lower() or "scene" in prompt.lower():
#             clean_prompt += ", landscape, detailed environment, high quality, digital art"
#         else:
#             clean_prompt += ", detailed, high quality, digital art"
        
#         return clean_prompt
    
#     def combine_images(self, character_img_bytes: BytesIO, background_img_bytes: BytesIO) -> BytesIO:
#         """Simple combination: rembg + PIL compositing"""
#         try:
#             logger.info("🎨 Simple combination: rembg + PIL...")
            
#             # Step 1: Remove character background with rembg
#             character_img_bytes.seek(0)
            
#             if self.rembg_session is not None:
#                 char_no_bg_bytes = remove(character_img_bytes.read(), session=self.rembg_session)
#                 char_no_bg = Image.open(BytesIO(char_no_bg_bytes)).convert('RGBA')
#                 logger.info("✅ Background removed with rembg")
#             else:
#                 # Simple fallback
#                 char_img = Image.open(character_img_bytes).convert('RGBA')
#                 char_no_bg = self._simple_background_removal(char_img)
#                 logger.info("✅ Background removed with fallback method")
            
#             # Step 2: Load background
#             background_img_bytes.seek(0)
#             bg_img = Image.open(background_img_bytes).convert('RGBA')
            
#             # Step 3: Resize both to 512x512
#             char_no_bg = char_no_bg.resize((512, 512), Image.Resampling.LANCZOS)
#             bg_img = bg_img.resize((512, 512), Image.Resampling.LANCZOS)
            
#             # Step 4: Simple PIL alpha composite - that's it!
#             combined = Image.alpha_composite(bg_img, char_no_bg)
            
#             # Step 5: Convert to RGB and save
#             combined = combined.convert('RGB')
            
#             buffer = BytesIO()
#             combined.save(buffer, format='JPEG', quality=95, optimize=True)
#             buffer.seek(0)
            
#             # Clean up
#             char_no_bg.close()
#             bg_img.close()
#             combined.close()
#             gc.collect()
            
#             logger.info("🎉 Simple combination complete!")
#             return buffer
            
#         except Exception as e:
#             logger.error(f"Error in simple combination: {str(e)}")
#             return self._create_placeholder_image("Combined Scene")
    
#     def _simple_background_removal(self, char_img: Image.Image) -> Image.Image:
#         """Fallback background removal if rembg is not available"""
#         if char_img.mode != 'RGBA':
#             char_img = char_img.convert('RGBA')
        
#         pixels = char_img.load()
#         width, height = char_img.size
        
#         for y in range(height):
#             for x in range(width):
#                 r, g, b, a = pixels[x, y]
#                 brightness = (r + g + b) / 3
                
#                 # Remove light backgrounds
#                 if brightness > 230:
#                     pixels[x, y] = (r, g, b, 0)
#                 elif brightness > 200:
#                     new_alpha = int(a * (230 - brightness) / 30)
#                     pixels[x, y] = (r, g, b, new_alpha)
        
#         return char_img
    
#     def _create_placeholder_image(self, prompt: str) -> BytesIO:
#         """Create a placeholder image when generation fails"""
#         img = Image.new('RGB', (512, 512), color='#2c3e50')
        
#         # Add simple gradient
#         pixels = img.load()
#         for y in range(512):
#             for x in range(512):
#                 factor = y / 512
#                 r = int(44 + factor * 40)
#                 g = int(62 + factor * 50) 
#                 b = int(80 + factor * 60)
#                 pixels[x, y] = (r, g, b)
        
#         # Add text
#         from PIL import ImageDraw
#         draw = ImageDraw.Draw(img)
        
#         draw.rectangle([10, 10, 502, 60], fill='#34495e', outline='#ecf0f1', width=2)
#         draw.text((20, 20), "AI IMAGE GENERATION", fill='#ecf0f1')
#         draw.text((20, 40), "(Placeholder)", fill='#bdc3c7')
        
#         # Add prompt
#         words = prompt.split()[:10]  # First 10 words
#         prompt_text = ' '.join(words)
#         draw.text((20, 100), f"Prompt: {prompt_text}", fill='#ecf0f1')
        
#         # Add center element
#         draw.ellipse([200, 200, 312, 312], fill='#e74c3c', outline='#c0392b', width=3)
#         draw.text((240, 245), "AI", fill='#ffffff')
        
#         buffer = BytesIO()
#         img.save(buffer, format='PNG')
#         buffer.seek(0)
#         return buffer
    
#     def cleanup(self):
#         """Clean up GPU memory and models"""
#         try:
#             if self.pipeline is not None:
#                 del self.pipeline
#                 self.pipeline = None
            
#             if self.img2img_pipeline is not None:
#                 del self.img2img_pipeline
#                 self.img2img_pipeline = None
            
#             if self.rembg_session is not None:
#                 del self.rembg_session
#                 self.rembg_session = None
            
#             if torch.cuda.is_available():
#                 torch.cuda.empty_cache()
            
#             gc.collect()
#             logger.info("✅ ImageService cleaned up successfully")
            
#         except Exception as e:
#             logger.warning(f"Cleanup error: {e}")

# # Usage examples for iterative refinement:
# """
# # Basic usage
# image_service = ImageGenerationService()

# # Generate initial images
# char_img = image_service.generate_image("knight, armor, sword")
# bg_img = image_service.generate_image("castle courtyard")

# # Iterative refinement
# # Fix character pose
# char_img_v2 = image_service.refine_image(char_img, "knight, armor, heroic stance, sword raised", strength=0.4)

# # Fix background composition  
# bg_img_v2 = image_service.refine_image(bg_img, "castle courtyard, empty center, clear space", strength=0.3)

# # Smart scene-aware refinement
# char_img_v3 = image_service.refine_character_for_scene(char_img_v2, bg_img_v2, "knight, armor, castle lighting")

# # Final combination
# final_img = image_service.combine_images(char_img_v3, bg_img_v2)
# """

# image_generation_service.py - Your existing service with vision enhancement under the hood
import logging
import torch
import gc
import numpy as np
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
from rembg import remove, new_session
import warnings

# Import vision positioning (will fail gracefully if not available)
try:
    from .vision_positioning import VisionPositioningService
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    VisionPositioningService = None

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

class ImageGenerationService:
    def __init__(self):
        # Initialize diffusers pipeline
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        self.img2img_pipeline = None
        self.model_id = "runwayml/stable-diffusion-v1-5"

        # Initialize rembg session for background removal
        try:
            self.rembg_session = new_session('u2net')
            logger.info("✓ rembg session initialized for background removal")
        except Exception as e:
            logger.warning(f"rembg initialization failed: {e}")
            self.rembg_session = None
        
        # Initialize vision positioning service (silently, won't affect API if it fails)
        self.vision_service = None
        if VISION_AVAILABLE:
            try:
                self.vision_service = VisionPositioningService()
                logger.info("✓ Vision positioning service initialized")
            except Exception as e:
                logger.warning(f"Vision positioning initialization failed: {e}")
                self.vision_service = None
        
        logger.info(f"Initializing ImageService on device: {self.device}")
        
        # Initialize pipelines
        self._initialize_pipelines()
    
    def _initialize_pipelines(self):
        """Initialize both text2img and img2img pipelines"""
        try:
            logger.info("Loading Stable Diffusion models...")
            
            # Text-to-Image Pipeline
            try:
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    use_safetensors=True,
                    variant="fp16" if self.device == "cuda" else None
                )
                logger.info("✓ Text2Img pipeline loaded")
            except Exception as e:
                logger.warning(f"Optimized loading failed: {e}")
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float32
                )
                logger.info("✓ Text2Img pipeline loaded (fallback)")
            
            # Image-to-Image Pipeline for iterative refinement
            try:
                self.img2img_pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    use_safetensors=True,
                    variant="fp16" if self.device == "cuda" else None
                )
                logger.info("✓ Img2Img pipeline loaded")
            except Exception as e:
                logger.warning(f"Img2Img loading failed: {e}")
                self.img2img_pipeline = None
            
            # Use faster scheduler for both
            for pipeline in [self.pipeline, self.img2img_pipeline]:
                if pipeline is not None:
                    try:
                        pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                            pipeline.scheduler.config
                        )
                    except Exception as e:
                        logger.warning(f"Could not set faster scheduler: {e}")
                    
                    # Move to device
                    pipeline = pipeline.to(self.device)
                    
                    # Memory optimizations
                    if self.device == "cuda":
                        try:
                            if hasattr(pipeline, 'enable_model_cpu_offload'):
                                pipeline.enable_model_cpu_offload()
                            if hasattr(pipeline, 'enable_attention_slicing'):
                                pipeline.enable_attention_slicing()
                            if hasattr(pipeline, 'enable_vae_slicing'):
                                pipeline.enable_vae_slicing()
                        except Exception as opt_error:
                            logger.warning(f"Memory optimizations failed: {opt_error}")
            
            logger.info("🎉 All pipelines loaded successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipelines: {str(e)}")
            logger.info("💡 Will use placeholder images instead")
            self.pipeline = None
            self.img2img_pipeline = None
    
    def generate_image(self, prompt: str) -> BytesIO:
        """Generate image using Diffusers Stable Diffusion"""
        try:
            if self.pipeline is None:
                logger.warning("Pipeline not available, using placeholder")
                return self._create_placeholder_image(prompt)
            
            logger.info(f"Generating image for: {prompt[:50]}...")
            
            # Clean and optimize prompt
            clean_prompt = self._optimize_prompt(prompt)
            
            # Generate image
            with torch.inference_mode():
                result = self.pipeline(
                    prompt=clean_prompt,
                    negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
                    num_inference_steps=20,
                    guidance_scale=7.5,
                    width=512,
                    height=512,
                    generator=torch.Generator(device=self.device).manual_seed(42)
                )
            
            # Convert to BytesIO
            image = result.images[0]
            buffer = BytesIO()
            image.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            # Clean up GPU memory
            if self.device == "cuda":
                torch.cuda.empty_cache()
            gc.collect()
            
            logger.info("✅ Image generated successfully!")
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return self._create_placeholder_image(prompt)
    
    def refine_image(self, image_bytes: BytesIO, refinement_prompt: str, strength: float = 0.4) -> BytesIO:
        """Refine existing image using img2img - for iterative improvement"""
        try:
            if self.img2img_pipeline is None:
                logger.warning("Img2Img pipeline not available")
                return image_bytes  # Return original if can't refine
            
            logger.info(f"Refining image with: {refinement_prompt[:50]}... (strength: {strength})")
            
            # Load existing image
            image_bytes.seek(0)
            existing_image = Image.open(image_bytes).convert('RGB')
            existing_image = existing_image.resize((512, 512), Image.Resampling.LANCZOS)
            
            # Clean prompt
            clean_prompt = self._optimize_prompt(refinement_prompt)
            
            # Refine using img2img
            with torch.inference_mode():
                result = self.img2img_pipeline(
                    prompt=clean_prompt,
                    image=existing_image,
                    strength=strength,  # How much to change (0.1=small, 0.9=big changes)
                    negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
                    num_inference_steps=20,
                    guidance_scale=7.5,
                    generator=torch.Generator(device=self.device).manual_seed(42)
                )
            
            # Convert to BytesIO
            refined_image = result.images[0]
            buffer = BytesIO()
            refined_image.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            # Clean up
            existing_image.close()
            refined_image.close()
            if self.device == "cuda":
                torch.cuda.empty_cache()
            gc.collect()
            
            logger.info("✅ Image refined successfully!")
            return buffer
            
        except Exception as e:
            logger.error(f"Error refining image: {str(e)}")
            return image_bytes  # Return original on error
    
    def refine_character_for_scene(self, character_img_bytes: BytesIO, background_img_bytes: BytesIO, 
                                 character_adjustments: str) -> BytesIO:
        """Refine character image to better fit the scene"""
        try:
            logger.info("🎨 Refining character to match scene...")
            
            # Analyze background for context
            background_img_bytes.seek(0)
            bg_img = Image.open(background_img_bytes).convert('RGB')
            scene_context = self._analyze_scene_context(bg_img)
            
            # Create scene-aware refinement prompt
            refinement_prompt = f"{character_adjustments}, {scene_context['lighting']}, {scene_context['style']}"
            
            # Refine character with scene context
            refined_character = self.refine_image(
                character_img_bytes, 
                refinement_prompt, 
                strength=0.3  # Moderate changes to maintain character
            )
            
            logger.info("✅ Character refined for scene compatibility")
            return refined_character
            
        except Exception as e:
            logger.error(f"Error refining character for scene: {str(e)}")
            return character_img_bytes
    
    def refine_background_for_character(self, background_img_bytes: BytesIO, character_img_bytes: BytesIO,
                                      background_adjustments: str) -> BytesIO:
        """Refine background to better accommodate the character"""
        try:
            logger.info("🏞️ Refining background for character placement...")
            
            # Analyze character for context
            character_img_bytes.seek(0)
            char_img = Image.open(character_img_bytes).convert('RGB')
            char_context = self._analyze_character_context(char_img)
            
            # Create character-aware refinement prompt
            refinement_prompt = f"{background_adjustments}, clear center space, {char_context['scale']}, {char_context['perspective']}"
            
            # Refine background with character context
            refined_background = self.refine_image(
                background_img_bytes,
                refinement_prompt,
                strength=0.4  # More changes allowed for background
            )
            
            logger.info("✅ Background refined for character compatibility")
            return refined_background
            
        except Exception as e:
            logger.error(f"Error refining background for character: {str(e)}")
            return background_img_bytes
    
    def combine_images(self, character_img_bytes: BytesIO, background_img_bytes: BytesIO) -> BytesIO:
        """
        Combine images - automatically uses vision positioning if available, 
        falls back to simple positioning seamlessly. Your API stays the same!
        """
        try:
            logger.info("🎨 Combining images...")
            
            # Step 1: Remove character background with rembg
            character_img_bytes.seek(0)
            
            if self.rembg_session is not None:
                char_no_bg_bytes = remove(character_img_bytes.read(), session=self.rembg_session)
                char_no_bg = BytesIO(char_no_bg_bytes)
                logger.info("✅ Background removed with rembg")
            else:
                char_no_bg = character_img_bytes
                logger.info("⚠️ Using original character image")
            
            # Step 2: Try vision positioning first (silently)
            if self.vision_service is not None:
                try:
                    combined_img_bytes = self.vision_service.smart_position_character(
                        char_no_bg, background_img_bytes
                    )
                    logger.info("✅ Vision-based positioning used")
                    return combined_img_bytes
                except Exception as e:
                    logger.warning(f"Vision positioning failed, using fallback: {e}")
            
            # Step 3: Fallback to simple PIL compositing (your original method)
            return self._simple_combine_images(char_no_bg, background_img_bytes)
            
        except Exception as e:
            logger.error(f"Error in image combination: {str(e)}")
            return self._create_placeholder_image("Combined Scene")
    
    def _simple_combine_images(self, character_img_bytes: BytesIO, background_img_bytes: BytesIO) -> BytesIO:
        """Simple combination: PIL compositing (your original method)"""
        try:
            logger.info("🎨 Simple combination: PIL...")
            
            # Load character (should already have background removed)
            character_img_bytes.seek(0)
            if self.rembg_session is None:
                # Apply simple background removal if rembg wasn't used
                char_img = Image.open(character_img_bytes).convert('RGBA')
                char_no_bg = self._simple_background_removal(char_img)
            else:
                char_no_bg = Image.open(character_img_bytes).convert('RGBA')
            
            # Load background
            background_img_bytes.seek(0)
            bg_img = Image.open(background_img_bytes).convert('RGBA')
            
            # Resize both to 512x512
            char_no_bg = char_no_bg.resize((512, 512), Image.Resampling.LANCZOS)
            bg_img = bg_img.resize((512, 512), Image.Resampling.LANCZOS)
            
            # Simple PIL alpha composite
            combined = Image.alpha_composite(bg_img, char_no_bg)
            
            # Convert to RGB and save
            combined = combined.convert('RGB')
            
            buffer = BytesIO()
            combined.save(buffer, format='JPEG', quality=95, optimize=True)
            buffer.seek(0)
            
            # Clean up
            char_no_bg.close()
            bg_img.close()
            combined.close()
            gc.collect()
            
            logger.info("🎉 Simple combination complete!")
            return buffer
            
        except Exception as e:
            logger.error(f"Error in simple combination: {str(e)}")
            return self._create_placeholder_image("Combined Scene")
    
    def _analyze_scene_context(self, bg_img: Image.Image) -> dict:
        """Analyze background image to determine lighting and style context"""
        # Convert to numpy for analysis
        img_array = np.array(bg_img)
        
        # Calculate average brightness
        brightness = np.mean(img_array)
        
        # Determine lighting style
        if brightness < 100:
            lighting = "dark moody lighting, shadows"
        elif brightness > 180:
            lighting = "bright natural lighting, warm tones"
        else:
            lighting = "balanced lighting, natural"
        
        # Determine general style (simple heuristic)
        style = "realistic digital art style"
        
        return {
            'lighting': lighting,
            'style': style,
            'brightness': brightness
        }
    
    def _analyze_character_context(self, char_img: Image.Image) -> dict:
        """Analyze character image to determine scale and perspective needs"""
        return {
            'scale': 'human scale proportions',
            'perspective': 'eye level perspective',
            'style': 'realistic character art'
        }
    
    def _optimize_prompt(self, prompt: str) -> str:
        """Optimize prompt for better Stable Diffusion results"""
        clean_prompt = prompt.replace("Portrait of ", "").replace("Scene: ", "")
        
        if "character" in prompt.lower() or "portrait" in prompt.lower():
            clean_prompt += ", portrait, detailed, high quality, digital art"
        elif "background" in prompt.lower() or "scene" in prompt.lower():
            clean_prompt += ", landscape, detailed environment, high quality, digital art"
        else:
            clean_prompt += ", detailed, high quality, digital art"
        
        return clean_prompt
    
    def _simple_background_removal(self, char_img: Image.Image) -> Image.Image:
        """Fallback background removal if rembg is not available"""
        if char_img.mode != 'RGBA':
            char_img = char_img.convert('RGBA')
        
        pixels = char_img.load()
        width, height = char_img.size
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                brightness = (r + g + b) / 3
                
                # Remove light backgrounds
                if brightness > 230:
                    pixels[x, y] = (r, g, b, 0)
                elif brightness > 200:
                    new_alpha = int(a * (230 - brightness) / 30)
                    pixels[x, y] = (r, g, b, new_alpha)
        
        return char_img
    
    def _create_placeholder_image(self, prompt: str) -> BytesIO:
        """Create a placeholder image when generation fails"""
        img = Image.new('RGB', (512, 512), color='#2c3e50')
        
        # Add simple gradient
        pixels = img.load()
        for y in range(512):
            for x in range(512):
                factor = y / 512
                r = int(44 + factor * 40)
                g = int(62 + factor * 50) 
                b = int(80 + factor * 60)
                pixels[x, y] = (r, g, b)
        
        # Add text
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([10, 10, 502, 60], fill='#34495e', outline='#ecf0f1', width=2)
        draw.text((20, 20), "AI IMAGE GENERATION", fill='#ecf0f1')
        draw.text((20, 40), "(Placeholder)", fill='#bdc3c7')
        
        # Add prompt
        words = prompt.split()[:10]  # First 10 words
        prompt_text = ' '.join(words)
        draw.text((20, 100), f"Prompt: {prompt_text}", fill='#ecf0f1')
        
        # Add center element
        draw.ellipse([200, 200, 312, 312], fill='#e74c3c', outline='#c0392b', width=3)
        draw.text((240, 245), "AI", fill='#ffffff')
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    
    def cleanup(self):
        """Clean up GPU memory and models"""
        try:
            if self.pipeline is not None:
                del self.pipeline
                self.pipeline = None
            
            if self.img2img_pipeline is not None:
                del self.img2img_pipeline
                self.img2img_pipeline = None
            
            if self.rembg_session is not None:
                del self.rembg_session
                self.rembg_session = None
            
            if self.vision_service is not None:
                del self.vision_service
                self.vision_service = None
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            gc.collect()
            logger.info("✅ ImageService cleaned up successfully")
            
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")

# Usage examples for iterative refinement:
"""
# Your existing API usage stays exactly the same:
image_service = ImageGenerationService()

# Generate initial images
char_img = image_service.generate_image("knight, armor, sword")
bg_img = image_service.generate_image("castle courtyard")

# Your existing combine_images method now automatically uses vision positioning if available
final_img = image_service.combine_images(char_img, bg_img)

# All your refinement methods work the same:
char_img_v2 = image_service.refine_image(char_img, "knight, armor, heroic stance", strength=0.4)
char_img_v3 = image_service.refine_character_for_scene(char_img_v2, bg_img, "knight, armor, castle lighting")
"""