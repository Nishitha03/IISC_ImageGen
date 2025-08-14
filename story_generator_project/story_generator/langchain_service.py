# # import logging
# # import gc
# # from typing import Dict, Any
# # from langchain.llms import Ollama
# # from langchain.prompts import PromptTemplate
# # from langchain.chains import LLMChain
# # from langchain.schema import BaseOutputParser

# # logger = logging.getLogger(__name__)

# # class SimpleTextParser(BaseOutputParser):
# #     def parse(self, text: str) -> str:
# #         return text.strip()

# # class StoryGenerationService:
# #     def __init__(self):
# #         # Using Ollama with llama2 - free and runs locally
# #         self.llm = Ollama(model="gemma2:2b")
# #         self._setup_chains()
    
# #     def _setup_chains(self):
# #         # Story generation chain
# #         story_template = """
# #         Create a short story (2-3 paragraphs) based on this prompt: {user_prompt}
        
# #         Make it engaging and creative. Include vivid descriptions.
        
# #         Story:
# #         """
        
# #         # Character description chain
# #         character_template = """
# #         Based on this story: {story}
        
# #         Create a detailed character description for the main character. Include:
# #         - Physical appearance
# #         - Clothing/attire
# #         - Facial features
# #         - Age and build
        
# #         Character Description:
# #         """
        
# #         # Background description chain
# #         background_template = """
# #         Based on this story: {story}
        
# #         Create a detailed background/scene description. Include:
# #         - Setting and location
# #         - Time of day/weather
# #         - Environmental details
# #         - Atmosphere and mood
        
# #         Background Description:
# #         """
        
# #         # Create chains
# #         self.story_chain = LLMChain(
# #             llm=self.llm,
# #             prompt=PromptTemplate(template=story_template, input_variables=["user_prompt"]),
# #             output_parser=SimpleTextParser()
# #         )
        
# #         self.character_chain = LLMChain(
# #             llm=self.llm,
# #             prompt=PromptTemplate(template=character_template, input_variables=["story"]),
# #             output_parser=SimpleTextParser()
# #         )
        
# #         self.background_chain = LLMChain(
# #             llm=self.llm,
# #             prompt=PromptTemplate(template=background_template, input_variables=["story"]),
# #             output_parser=SimpleTextParser()
# #         )
    
# #     def generate_story_content(self, user_prompt: str) -> Dict[str, str]:
# #         """Generate story, character, and background descriptions"""
# #         try:
# #             logger.info(f"Generating story for prompt: {user_prompt[:50]}...")
            
# #             # Generate story
# #             story = self.story_chain.run(user_prompt=user_prompt)
# #             logger.info("Story generated successfully")
            
# #             # Generate character description
# #             character_desc = self.character_chain.run(story=story)
# #             logger.info("Character description generated")
            
# #             # Generate background description
# #             background_desc = self.background_chain.run(story=story)
# #             logger.info("Background description generated")
            
# #             # Clean up memory
# #             gc.collect()
            
# #             return {
# #                 'story': story,
# #                 'character_description': character_desc,
# #                 'background_description': background_desc
# #             }
            
# #         except Exception as e:
# #             logger.error(f"Error generating story content: {str(e)}")
# #             raise

# #     def create_image_prompts(self, character_desc: str, background_desc: str) -> Dict[str, str]:
# #         """Convert descriptions to image generation prompts"""
        
# #         # Simple prompt engineering for Stable Diffusion
# #         character_prompt = f"Portrait of {character_desc.lower()}, high quality, detailed, digital art style"
        
# #         background_prompt = f"Scene: {background_desc.lower()}, atmospheric, detailed environment, digital art style"
        
# #         return {
# #             'character_prompt': character_prompt,
# #             'background_prompt': background_prompt
# #         }


# import logging
# import gc
# from typing import Dict, Any
# from langchain.llms import Ollama
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain.schema import BaseOutputParser

# logger = logging.getLogger(__name__)

# class SimpleTextParser(BaseOutputParser):
#     def parse(self, text: str) -> str:
#         return text.strip()

# class StoryGenerationService:
#     def __init__(self):
#         # Using Ollama with gemma2:2b - free, lightweight and runs locally
#         self.llm = Ollama(model="gemma2:2b")
#         self._setup_chains()
    
#     def _setup_chains(self):
#         # Story generation chain
#         story_template = """
#         Create a short story (2-3 paragraphs) based on this prompt: {user_prompt}
        
#         Make it engaging and creative. Include vivid descriptions.
        
#         Story:
#         """
        
#         # Character description chain
#         character_template = """
#         Based on this story: {story}
        
#         Create a detailed character description for the main character. Include:
#         - Physical appearance
#         - Clothing/attire
#         - Facial features
#         - Age and build
        
#         Character Description:
#         """
        
#         # Background description chain
#         background_template = """
#         Based on this story: {story}
        
#         Create a detailed background/scene description. Include:
#         - Setting and location
#         - Time of day/weather
#         - Environmental details
#         - Atmosphere and mood
        
#         Background Description:
#         """
        
#         # NEW: Image prompt extraction chains
#         character_prompt_template = """
#         From this character description, extract only the key visual elements for image generation:
        
#         Character Description: {character_description}
        
#         Extract and list only:
#         - Main appearance (age, gender, build)
#         - Key clothing/armor pieces
#         - Hair color and style
#         - Most distinctive features
        
#         Format as a short, comma-separated list for AI image generation.
        
#         Visual Prompt:
#         """
        
#         background_prompt_template = """
#         From this scene description, extract only the key visual elements for image generation:
        
#         Scene Description: {background_description}
        
#         Extract and list only:
#         - Main location/setting
#         - Key environmental elements
#         - Lighting/time of day
#         - Atmosphere/mood
        
#         Format as a short, comma-separated list for AI image generation.
        
#         Visual Prompt:
#         """
        
#         # Create chains
#         self.story_chain = LLMChain(
#             llm=self.llm,
#             prompt=PromptTemplate(template=story_template, input_variables=["user_prompt"]),
#             output_parser=SimpleTextParser()
#         )
        
#         self.character_chain = LLMChain(
#             llm=self.llm,
#             prompt=PromptTemplate(template=character_template, input_variables=["story"]),
#             output_parser=SimpleTextParser()
#         )
        
#         self.background_chain = LLMChain(
#             llm=self.llm,
#             prompt=PromptTemplate(template=background_template, input_variables=["story"]),
#             output_parser=SimpleTextParser()
#         )
        
#         # NEW: Image prompt extraction chains
#         self.character_prompt_chain = LLMChain(
#             llm=self.llm,
#             prompt=PromptTemplate(template=character_prompt_template, input_variables=["character_description"]),
#             output_parser=SimpleTextParser()
#         )
        
#         self.background_prompt_chain = LLMChain(
#             llm=self.llm,
#             prompt=PromptTemplate(template=background_prompt_template, input_variables=["background_description"]),
#             output_parser=SimpleTextParser()
#         )
    
#     def generate_story_content(self, user_prompt: str) -> Dict[str, str]:
#         """Generate story, character, and background descriptions"""
#         try:
#             logger.info(f"Generating story for prompt: {user_prompt[:50]}...")
            
#             # Generate story
#             story = self.story_chain.run(user_prompt=user_prompt)
#             logger.info("Story generated successfully")
            
#             # Generate character description
#             character_desc = self.character_chain.run(story=story)
#             logger.info("Character description generated")
            
#             # Generate background description
#             background_desc = self.background_chain.run(story=story)
#             logger.info("Background description generated")
            
#             # Clean up memory
#             gc.collect()
            
#             return {
#                 'story': story,
#                 'character_description': character_desc,
#                 'background_description': background_desc
#             }
            
#         except Exception as e:
#             logger.error(f"Error generating story content: {str(e)}")
#             raise

#     def create_image_prompts(self, character_desc: str, background_desc: str) -> Dict[str, str]:
#         """Convert descriptions to optimized image generation prompts using LLM"""
#         try:
#             logger.info("Extracting visual elements for image prompts...")
            
#             # Use LLM to extract key visual elements for character
#             character_visual_elements = self.character_prompt_chain.run(
#                 character_description=character_desc
#             )
#             logger.info("Character visual elements extracted")
            
#             # Use LLM to extract key visual elements for background
#             background_visual_elements = self.background_prompt_chain.run(
#                 background_description=background_desc
#             )
#             logger.info("Background visual elements extracted")
            
#             # Construct optimized Stable Diffusion prompts
#             character_prompt = f"{character_visual_elements.strip()}, portrait, high quality, detailed, digital art"
            
#             background_prompt = f"{background_visual_elements.strip()}, landscape, atmospheric, detailed environment, digital art"
            
#             logger.info("Image prompts constructed successfully")
            
#             # Clean up memory
#             gc.collect()
            
#             return {
#                 'character_prompt': character_prompt,
#                 'background_prompt': background_prompt,
#                 'character_elements': character_visual_elements,  # For debugging
#                 'background_elements': background_visual_elements  # For debugging
#             }
            
#         except Exception as e:
#             logger.error(f"Error creating image prompts: {str(e)}")
#             # Fallback to simple extraction if LLM fails
#             return self._create_fallback_prompts(character_desc, background_desc)
    
#     def _create_fallback_prompts(self, character_desc: str, background_desc: str) -> Dict[str, str]:
#         """Fallback prompt creation using simple keyword extraction"""
#         logger.info("Using fallback prompt creation method")
        
#         # Simple keyword extraction for character
#         char_keywords = []
#         char_words = character_desc.lower().split()
        
#         # Look for key visual descriptors
#         appearance_words = ['young', 'old', 'tall', 'short', 'man', 'woman', 'knight', 'wizard', 'warrior']
#         clothing_words = ['armor', 'robes', 'cloak', 'dress', 'tunic', 'helmet', 'crown']
#         feature_words = ['blonde', 'brown', 'black', 'blue eyes', 'green eyes', 'beard', 'mustache']
        
#         for word in char_words:
#             if any(w in word for w in appearance_words + clothing_words + feature_words):
#                 char_keywords.append(word)
        
#         # Simple keyword extraction for background
#         bg_keywords = []
#         bg_words = background_desc.lower().split()
        
#         location_words = ['forest', 'castle', 'library', 'mountain', 'ocean', 'city', 'village', 'cave']
#         atmosphere_words = ['dark', 'bright', 'misty', 'sunny', 'stormy', 'magical', 'ancient']
        
#         for word in bg_words:
#             if any(w in word for w in location_words + atmosphere_words):
#                 bg_keywords.append(word)
        
#         # Construct clean prompts (different from LLM method)
#         character_elements = ' '.join(char_keywords[:6])  # Limit to 6 keywords
#         background_elements = ' '.join(bg_keywords[:6])   # Limit to 6 keywords
        
#         character_prompt = f"{character_elements}, character portrait, detailed, digital art"
#         background_prompt = f"{background_elements}, environment scene, atmospheric, digital art"
        
#         return {
#             'character_prompt': character_prompt,
#             'background_prompt': background_prompt,
#             'character_elements': character_elements,
#             'background_elements': background_elements
#         }


import logging
import gc
from typing import Dict, Any
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

logger = logging.getLogger(__name__)

class SimpleTextParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        return text.strip()

class StoryGenerationService:
    def __init__(self):
        # Using Ollama with gemma2:2b - free, lightweight and runs locally
        self.llm = Ollama(model="gemma3:4b")
        self._setup_chains()
    
    def _setup_chains(self):
        # Story generation chain
        story_template = """
        Create a short story (2-3 paragraphs) based on this prompt: {user_prompt}
        
        Make it engaging and creative. Include vivid descriptions.
        
        Story:
        """
        
        # Character description chain
        character_template = """ Based on this story: {story} Create a detailed character description for the main character. Include: - Physical appearance - Clothing/attire - Facial features - Age and build Character Description: """

        
        # Background description chain
        background_template = """
Based on this story: {story}

Describe the BACKGROUND/SCENE for image generation.

Include in detail:
1) Setting & location (specific, recognizable, story-appropriate)
2) Time of day & lighting conditions (morning sunlight, sunset glow, overcast, etc.)
3) Weather or atmospheric effects (rain, mist, dust, clear skies, etc.)
4) Key environmental features (structures, terrain, vegetation, objects) — focus on elements that surround, not replace, the character
5) Mood & tone conveyed by the setting
6) Camera perspective & framing (wide shot, medium shot, aerial view, over-the-shoulder, etc.)

Rules:
- Do NOT describe the main character — leave them out entirely.
- Focus on setting elements that support a character being placed into it.
- Avoid overloading with unrelated props; keep only visually relevant details.
- Write as a single compact paragraph of vivid, sensory-rich detail.
- Keep it under 50 words.

Background Description:
"""

        
        # NEW: Scene analysis chain for character pose/camera
        scene_analysis_template = """
        Analyze this scene description and determine the best character pose and camera angle:
        
        Scene: {background_description}
        
        Consider:
        - Is this an action scene or peaceful moment?
        - What camera angle fits the environment (low angle, eye level, etc.)?
        - Should the character be in motion or static?
        - What pose would fit this scene naturally?
        
        Provide:
        - Camera angle (low angle, eye level, high angle, close-up, medium shot, full body)
        - Character pose (standing, walking, fighting, casting, sitting, etc.)
        - Character positioning (facing forward, profile, three-quarter view)
        - Action/emotion (determined, peaceful, alert, etc.)
        
        Do not include any salutations questions or any other text , just give me the final analysis thats it
        Analysis:
        """
        
        # Image prompt extraction chains (updated)
#         
        character_prompt_template = """
You are generating a precise visual description for a CHARACTER in a scene.

Character context (must appear in output in some way):
- {character_description}

Scene context:
- {scene_analysis}

Lighting / Atmosphere:
- {scene_atmosphere}

Rules:
1. Identify the **main CENTER OBJECT** from the scene description.
2. Choose a POSE + ACTION that uses that object naturally.
3. Integrate **character traits** from the given character context (role, personality, age, style).
4. Clothing, accessories, and expression must match BOTH the scene and character.
5. Lighting must match atmosphere.
6. Output must be **exactly 20 descriptive tokens**, comma-separated, no filler, no sentences.
7. Token order:
   [character role/identity], [age/gender/physical trait], [clothing], [accessory/prop], [pose], [action], [center object], [facial expression], [lighting], [scene-specific detail], [mood], [extra relevant visual], [hair style], [body build], [secondary accessory], [background element], [color tone], [material/texture], [emotion], [weather/extra atmosphere]

Examples (20 tokens each):

Cafe scene (character: young artist, role: sketching):
"artist, young female, denim jacket, sketchbook, sitting pose, drawing lines, center chair, focused smile, warm lighting, wooden table, calm mood, coffee steam, tied hair, slim build, pencil case, blurred patrons, soft brown tone, leather texture, creative joy, rain outside"

Blacksmith scene (character: aging dwarf, role: crafting weapons):
"blacksmith, stout male, leather apron, heavy hammer, standing pose, forging blade, center anvil, intense gaze, forge lighting, glowing metal, determined mood, flying sparks, braided beard, muscular build, iron tongs, hanging tools, deep orange tone, rough metal texture, pride, smoke haze"

Now:
1. Pick the CENTER OBJECT.
2. Match pose & action to object.
3. Integrate **character traits** visibly.
4. Produce the 20-token comma-separated prompt with no extra commentary.
"""

        
        # background_prompt_template = """
        # From this scene description, extract only the key visual elements for image generation:
        
        # Scene Description: {background_description}
        
        # Extract and list only 5 CRISP WORDS EACH:
        # - Main location/setting 
        # - Key environmental elements
        # - Lighting/time of day
        # - Atmosphere/mood
        # - Camera perspective
        
        # Format as a short, comma-separated list for AI image generation.
        
        # Background Image Prompt:
        # """
        background_prompt_template = """
You are describing a BACKGROUND PLATE only (no people, no characters, no actions).

Scene: {background_description}

Rules:
1) Do NOT mention people or actions.
2) Reserve a clear open space in the center for a subject to be added later.
3) Focus on layout, materials, lighting, atmosphere, and environment.
4) Output exactly 20 short comma-separated descriptive tokens (nouns/adjectives only, no full sentences).

Example outputs:

# Cafe
"cozy cafe interior, warm tones, wood furniture, tiled floor, golden light, soft shadows, pastry counter, shelves with mugs, clear center floor, scattered tables, hanging lights, menu board, potted plants, wall art, textured walls, quiet ambience, clean surfaces, warm glow, inviting space, subtle reflections"

# Forest
"forest clearing, lush greenery, mossy ground, dappled sunlight, tall trees, light mist, clear center patch, wildflowers, leaf litter, low shrubs, uneven terrain, distant hills, soft haze, earthy colors, winding path, rock edges, calm atmosphere, gentle breeze, natural textures, serene mood"

Now generate only the 20-token description for the given scene:
"""
        
        # Create chains
        self.story_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=story_template, input_variables=["user_prompt"]),
            output_parser=SimpleTextParser()
        )
        
        self.character_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=character_template, input_variables=["story"]),
            output_parser=SimpleTextParser()
        )
        
        self.background_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=background_template, input_variables=["story"]),
            output_parser=SimpleTextParser()
        )
        
        # NEW: Scene analysis chain
        self.scene_analysis_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=scene_analysis_template, input_variables=["background_description"]),
            output_parser=SimpleTextParser()
        )
        
        # Updated image prompt chains
        self.character_prompt_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=character_prompt_template, 
                                input_variables=["character_description", "scene_analysis", "scene_atmosphere"]),
            output_parser=SimpleTextParser()
        )
        
        self.background_prompt_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=background_prompt_template, input_variables=["background_description"]),
            output_parser=SimpleTextParser()
        )
    
    def generate_story_content(self, user_prompt: str) -> Dict[str, str]:
        """Generate story, character, and background descriptions"""
        try:
            logger.info(f"Generating story for prompt: {user_prompt[:50]}...")
            
            # Generate story
            story = self.story_chain.run(user_prompt=user_prompt)
            logger.info("Story generated successfully")
            
            # Generate character description
            character_desc = self.character_chain.run(story=story)
            logger.info("Character description generated")
            
            # Generate background description
            background_desc = self.background_chain.run(story=story)
            logger.info("Background description generated")
            
            # Clean up memory
            gc.collect()
            
            return {
                'story': story,
                'character_description': character_desc,
                'background_description': background_desc
            }
            
        except Exception as e:
            logger.error(f"Error generating story content: {str(e)}")
            raise

    def create_image_prompts(self, character_desc: str, background_desc: str) -> Dict[str, str]:
        """Create CLEAN image prompts without gunk"""
        try:
            logger.info("Creating clean, focused image prompts...")
            
            # Step 1: Quick scene analysis
            scene_analysis = self.scene_analysis_chain.run(background_description=background_desc)
            scene_atmosphere = self._extract_scene_atmosphere(background_desc)
            
            # Step 2: Generate CLEAN character prompt
            character_prompt_raw = self.character_prompt_chain.run(
                character_description=character_desc,
                scene_analysis=scene_analysis,
                scene_atmosphere=scene_atmosphere
            )
            
            # Step 3: Generate CLEAN background prompt  
            background_prompt_raw = self.background_prompt_chain.run(
                background_description=background_desc
            )
            
            
            # Step 4: Clean up and finalize prompts
            character_prompt = f"{character_prompt_raw.strip()}, digital art"
            background_prompt = f"{background_prompt_raw.strip()}, detailed environment, digital art"
            print(character_prompt)
            print(background_prompt)
            logger.info("✅ Clean prompts created successfully")
            gc.collect()
            
            return {
                'character_prompt': character_prompt,
                'background_prompt': background_prompt,
                'character_elements': character_prompt_raw.strip(),
                'background_elements': background_prompt_raw.strip(),
                'scene_analysis': scene_analysis,
                'scene_atmosphere': scene_atmosphere
            }
            
        except Exception as e:
            logger.error(f"Error creating clean prompts: {str(e)}")
            return self._create_fallback_prompts(character_desc, background_desc)
    
    def _extract_scene_atmosphere(self, background_elements: str) -> str:
        """Extract lighting and atmosphere from scene for character consistency"""
        elements = background_elements.lower()
        
        # Simple atmosphere mapping
        if any(word in elements for word in ['dark', 'night', 'shadow', 'cave']):
            return "dark moody lighting, shadows"
        elif any(word in elements for word in ['bright', 'sunny', 'day', 'golden']):
            return "bright natural lighting, warm tones"
        elif any(word in elements for word in ['magical', 'glowing', 'mystical', 'enchanted']):
            return "magical lighting, ethereal glow"
        elif any(word in elements for word in ['forest', 'green', 'nature']):
            return "dappled forest lighting, natural"
        elif any(word in elements for word in ['library', 'indoor', 'ancient']):
            return "warm indoor lighting, ambient"
        else:
            return "natural lighting, balanced exposure"
    
    def _create_fallback_prompts(self, character_desc: str, background_desc: str) -> Dict[str, str]:
        """Fallback prompt creation using simple keyword extraction"""
        logger.info("Using fallback prompt creation method")
        
        # Simple keyword extraction for character
        char_keywords = []
        char_words = character_desc.lower().split()
        
        # Look for key visual descriptors
        appearance_words = ['young', 'old', 'tall', 'short', 'man', 'woman', 'knight', 'wizard', 'warrior']
        clothing_words = ['armor', 'robes', 'cloak', 'dress', 'tunic', 'helmet', 'crown']
        feature_words = ['blonde', 'brown', 'black', 'blue eyes', 'green eyes', 'beard', 'mustache']
        
        for word in char_words:
            if any(w in word for w in appearance_words + clothing_words + feature_words):
                char_keywords.append(word)
        
        # Simple keyword extraction for background
        bg_keywords = []
        bg_words = background_desc.lower().split()
        
        location_words = ['forest', 'castle', 'library', 'mountain', 'ocean', 'city', 'village', 'cave']
        atmosphere_words = ['dark', 'bright', 'misty', 'sunny', 'stormy', 'magical', 'ancient']
        
        for word in bg_words:
            if any(w in word for w in location_words + atmosphere_words):
                bg_keywords.append(word)
        
        # Construct clean prompts (different from LLM method)
        character_elements = ' '.join(char_keywords[:6])  # Limit to 6 keywords
        background_elements = ' '.join(bg_keywords[:6])   # Limit to 6 keywords
        
        character_prompt = f"{character_elements}, character portrait, detailed, digital art"
        background_prompt = f"{background_elements}, environment scene, atmospheric, digital art"
        
        return {
            'character_prompt': character_prompt,
            'background_prompt': background_prompt,
            'character_elements': character_elements,
            'background_elements': background_elements
        }
