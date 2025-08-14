# vision_positioning.py
import logging
import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
import json

logger = logging.getLogger(__name__)

class JSONOutputParser(BaseOutputParser):
    """Parse JSON output from vision model"""
    
    def parse(self, text: str) -> dict:
        try:
            # Extract JSON from text (handle cases where model adds explanation)
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
            else:
                # Fallback if no JSON found
                return {"error": "No valid JSON found in response"}
                
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON: {text}")
            return {"error": "Invalid JSON format"}

class VisionPositioningService:
    def __init__(self, model_name="gemma3:latest"):
        # Initialize Ollama with vision capabilities
        self.vision_llm = Ollama(model=model_name)
        self._setup_vision_chains()
    
    def _setup_vision_chains(self):
        """Setup vision analysis chains for character positioning"""
        
        # Scene analysis chain - analyzes background for optimal placement areas
        scene_analysis_template = """
        Analyze this background scene image for character placement.

        Look for:
        1. FURNITURE/OBJECTS where a character could sit/stand/interact
        2. EMPTY SPACES suitable for character placement
        3. NATURAL FOCAL POINTS (center areas, clearings, etc.)
        4. INTERACTIVE ELEMENTS (chairs, desks, logs, platforms, etc.)
        5. SCALE/PERSPECTIVE to understand size requirements

        Return analysis in this JSON format:
        {
            "placement_areas": [
                {
                    "type": "chair/throne/log/ground/platform",
                    "position": "center/left/right/front/back", 
                    "coordinates": "approximate x,y as percentages",
                    "suitability": "excellent/good/fair",
                    "interaction": "sitting/standing/leaning/etc",
                    "reason": "why this spot works"
                }
            ],
            "best_placement": {
                "area_index": 0,
                "confidence": "high/medium/low"
            },
            "scene_scale": "human/large/small",
            "lighting_source": "left/right/center/above/ambient"
        }

        Scene Analysis:
        """
        
        # Character positioning chain - determines how character should be placed
        positioning_template = """
        Given this character image and the scene analysis, determine optimal positioning.

        Character image: {character_image}
        Scene analysis: {scene_analysis}

        Determine:
        1. CHARACTER SIZE relative to scene
        2. ROTATION/ORIENTATION needed
        3. EXACT POSITION coordinates
        4. INTERACTION POSE adjustments
        5. LIGHTING ADJUSTMENTS needed

        Return positioning in JSON format:
        {
            "final_position": {
                "x_percent": 50,
                "y_percent": 60,
                "scale_factor": 1.0,
                "rotation_degrees": 0
            },
            "pose_adjustments": "description of how character should be oriented",
            "lighting_match": "adjustments needed to match scene lighting",
            "interaction_details": "how character interacts with scene elements",
            "confidence": "high/medium/low"
        }

        Character Positioning:
        """
        
        self.scene_analysis_chain = LLMChain(
            llm=self.vision_llm,
            prompt=PromptTemplate(template=scene_analysis_template, input_variables=[]),
            output_parser=JSONOutputParser()
        )
        
        self.positioning_chain = LLMChain(
            llm=self.vision_llm,
            prompt=PromptTemplate(template=positioning_template, 
                                input_variables=["character_image", "scene_analysis"]),
            output_parser=JSONOutputParser()
        )
    
    def analyze_scene_for_placement(self, background_img_bytes: BytesIO) -> dict:
        """Analyze background scene using vision model to find placement areas"""
        try:
            # Convert image to base64 for vision model
            background_img_bytes.seek(0)
            img_base64 = base64.b64encode(background_img_bytes.read()).decode('utf-8')
            
            # Use vision model to analyze scene
            analysis = self.scene_analysis_chain.run(image=img_base64)
            
            logger.info("Scene analyzed for character placement")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing scene: {str(e)}")
            # Fallback to center placement
            return {
                "placement_areas": [{
                    "type": "ground",
                    "position": "center",
                    "coordinates": "50,70",
                    "suitability": "good",
                    "interaction": "standing",
                    "reason": "default center placement"
                }],
                "best_placement": {"area_index": 0, "confidence": "medium"},
                "scene_scale": "human",
                "lighting_source": "ambient"
            }
    
    def determine_character_positioning(self, character_img_bytes: BytesIO, 
                                      scene_analysis: dict) -> dict:
        """Determine optimal character positioning using vision analysis"""
        try:
            # Convert character image to base64
            character_img_bytes.seek(0)
            char_img_base64 = base64.b64encode(character_img_bytes.read()).decode('utf-8')
            
            # Use vision model to determine positioning
            positioning = self.positioning_chain.run(
                character_image=char_img_base64,
                scene_analysis=json.dumps(scene_analysis)
            )
            
            logger.info("Character positioning determined")
            return positioning
            
        except Exception as e:
            logger.error(f"Error determining positioning: {str(e)}")
            # Fallback positioning
            return {
                "final_position": {
                    "x_percent": 50,
                    "y_percent": 70,
                    "scale_factor": 1.0,
                    "rotation_degrees": 0
                },
                "pose_adjustments": "center standing",
                "lighting_match": "match scene lighting",
                "interaction_details": "standing in scene",
                "confidence": "medium"
            }
    
    def apply_opencv_positioning(self, character_img_bytes: BytesIO, 
                               background_img_bytes: BytesIO, 
                               positioning: dict) -> BytesIO:
        """Apply the vision-determined positioning using OpenCV"""
        try:
            # Load images
            char_img = cv2.imdecode(
                np.frombuffer(character_img_bytes.getvalue(), np.uint8), 
                cv2.IMREAD_UNCHANGED
            )
            bg_img = cv2.imdecode(
                np.frombuffer(background_img_bytes.getvalue(), np.uint8), 
                cv2.IMREAD_COLOR
            )
            
            # Get positioning parameters
            pos = positioning["final_position"]
            x_percent = pos.get("x_percent", 50)
            y_percent = pos.get("y_percent", 70)
            scale_factor = pos.get("scale_factor", 1.0)
            rotation = pos.get("rotation_degrees", 0)
            
            # Resize background to standard size
            bg_height, bg_width = 512, 512
            bg_img = cv2.resize(bg_img, (bg_width, bg_height))
            
            # Process character image
            if char_img.shape[2] == 4:  # Has alpha channel
                char_bgr = char_img[:, :, :3]
                char_alpha = char_img[:, :, 3]
            else:
                char_bgr = char_img
                char_alpha = np.ones(char_img.shape[:2], dtype=np.uint8) * 255
            
            # Scale character
            char_height, char_width = char_bgr.shape[:2]
            new_width = int(char_width * scale_factor)
            new_height = int(char_height * scale_factor)
            
            char_bgr = cv2.resize(char_bgr, (new_width, new_height))
            char_alpha = cv2.resize(char_alpha, (new_width, new_height))
            
            # Rotate if needed
            if rotation != 0:
                center = (new_width // 2, new_height // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, rotation, 1.0)
                char_bgr = cv2.warpAffine(char_bgr, rotation_matrix, (new_width, new_height))
                char_alpha = cv2.warpAffine(char_alpha, rotation_matrix, (new_width, new_height))
            
            # Calculate position
            x_pos = int((x_percent / 100) * bg_width - new_width // 2)
            y_pos = int((y_percent / 100) * bg_height - new_height // 2)
            
            # Ensure character fits in frame
            x_pos = max(0, min(x_pos, bg_width - new_width))
            y_pos = max(0, min(y_pos, bg_height - new_height))
            
            # Apply character to background
            result = bg_img.copy()
            
            # Alpha blending
            alpha_normalized = char_alpha.astype(float) / 255.0
            
            for c in range(3):
                result[y_pos:y_pos+new_height, x_pos:x_pos+new_width, c] = (
                    alpha_normalized * char_bgr[:, :, c] +
                    (1 - alpha_normalized) * result[y_pos:y_pos+new_height, x_pos:x_pos+new_width, c]
                )
            
            # Convert back to BytesIO
            _, buffer = cv2.imencode('.jpg', result)
            result_bytes = BytesIO(buffer.tobytes())
            
            logger.info(f"Character positioned at ({x_percent}%, {y_percent}%) with scale {scale_factor}")
            
            return result_bytes
            
        except Exception as e:
            logger.error(f"Error applying OpenCV positioning: {str(e)}")
            raise e
    
    def smart_position_character(self, character_img_bytes: BytesIO, 
                               background_img_bytes: BytesIO) -> BytesIO:
        """Intelligently position character using vision analysis"""
        try:
            logger.info("🧠 Starting vision-based character positioning...")
            
            # Step 1: Analyze scene for placement opportunities
            scene_analysis = self.analyze_scene_for_placement(background_img_bytes)
            
            # Step 2: Determine optimal character positioning
            positioning = self.determine_character_positioning(
                character_img_bytes, scene_analysis
            )
            
            # Step 3: Apply positioning using OpenCV
            positioned_image = self.apply_opencv_positioning(
                character_img_bytes, background_img_bytes, positioning
            )
            
            logger.info("✅ Vision-based positioning complete!")
            return positioned_image
            
        except Exception as e:
            logger.error(f"Error in smart positioning: {str(e)}")
            raise e