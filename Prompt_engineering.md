# Story Generator Prompt Engineering

This document outlines the prompt engineering techniques implemented in the `langchain_service.py` file for generating coherent stories and optimized image generation prompts.

## Overview

The system uses a multi-stage LLM pipeline to transform user prompts into rich story content and precise visual prompts for AI image generation. Each stage employs specific prompt engineering strategies to maximize output quality and consistency.

## Core Prompt Engineering Strategies

### 1. **Chain-Based Processing Pipeline**

The system breaks down complex generation tasks into specialized chains:

- **Story Chain**: Initial narrative generation
- **Character Chain**: Character description extraction
- **Background Chain**: Scene/environment description
- **Scene Analysis Chain**: Camera angles and pose determination
- **Visual Prompt Chains**: Optimized image generation prompts

This approach ensures each LLM call has a focused, specific task rather than attempting complex multi-modal generation in one step.

### 2. **Contextual Prompt Templates**

#### Story Generation Template
```
Create a short story (2-3 paragraphs) based on this prompt: {user_prompt}
Make it engaging and creative. Include vivid descriptions.
```

**Strategy**: Simple, clear instruction with emphasis on vivid descriptions to provide rich source material for subsequent chains.

#### Character Description Template
```
Based on this story: {story}
Create a detailed character description for the main character. Include:
- Physical appearance
- Clothing/attire  
- Facial features
- Age and build
```

**Strategy**: Structured bullet points ensure comprehensive character details needed for visual generation.

### 3. **Advanced Background Prompt Engineering**

The background template uses sophisticated constraints:

```
Describe the BACKGROUND/SCENE for image generation.
Include in detail:
1) Setting & location (specific, recognizable, story-appropriate)
2) Time of day & lighting conditions
3) Weather or atmospheric effects
4) Key environmental features
5) Mood & tone conveyed by the setting
6) Camera perspective & framing

Rules:
- Do NOT describe the main character — leave them out entirely
- Focus on setting elements that support a character being placed into it
- Keep it under 50 words
```

**Key Strategies**:
- **Explicit exclusion rules** prevent character contamination in background descriptions
- **Structured requirements** ensure all visual elements are covered
- **Word limits** maintain prompt efficiency
- **Compositional awareness** (camera perspective) for better image layout

### 4. **Token-Limited Visual Prompt Generation**

#### Character Visual Prompt (20-Token Strategy)
```
Output must be exactly 20 descriptive tokens, comma-separated, no filler, no sentences.
Token order:
[character role/identity], [age/gender/physical trait], [clothing], [accessory/prop], 
[pose], [action], [center object], [facial expression], [lighting], [scene-specific detail], 
[mood], [extra relevant visual], [hair style], [body build], [secondary accessory], 
[background element], [color tone], [material/texture], [emotion], [weather/extra atmosphere]
```

**Strategy**: 
- **Fixed token count** ensures consistent prompt length
- **Ordered structure** prioritizes important visual elements
- **Eliminates prompt bloat** common in AI image generation
- **Examples provided** for few-shot learning

#### Background Visual Prompt (20-Token Strategy)
```
You are describing a BACKGROUND PLATE only (no people, no characters, no actions).
Reserve a clear open space in the center for a subject to be added later.
Output exactly 20 short comma-separated descriptive tokens (nouns/adjectives only).
```

**Strategy**:
- **Explicit character exclusion** prevents conflicts during image compositing
- **Compositional planning** reserves space for character placement
- **Token type specification** (nouns/adjectives only) improves AI image model understanding

### 5. **Scene Analysis for Dynamic Prompting**

```
Consider:
- Is this an action scene or peaceful moment?
- What camera angle fits the environment?
- Should the character be in motion or static?
- What pose would fit this scene naturally?

Provide:
- Camera angle (low angle, eye level, high angle, close-up, medium shot, full body)
- Character pose (standing, walking, fighting, casting, sitting, etc.)
- Character positioning (facing forward, profile, three-quarter view)
- Action/emotion (determined, peaceful, alert, etc.)
```

**Strategy**: Scene-responsive prompt generation that adapts character presentation based on narrative context.

### 6. **Fallback Prompt Engineering**

The system includes keyword-based fallback methods when LLM chains fail:

```python
# Look for key visual descriptors
appearance_words = ['young', 'old', 'tall', 'short', 'man', 'woman', 'knight', 'wizard', 'warrior']
clothing_words = ['armor', 'robes', 'cloak', 'dress', 'tunic', 'helmet', 'crown']
```

**Strategy**: Rule-based extraction ensures system reliability even when advanced prompting fails.

### 7. **Atmospheric Consistency Mapping**

```python
def _extract_scene_atmosphere(self, background_elements: str) -> str:
    if any(word in elements for word in ['dark', 'night', 'shadow', 'cave']):
        return "dark moody lighting, shadows"
    elif any(word in elements for word in ['bright', 'sunny', 'day', 'golden']):
        return "bright natural lighting, warm tones"
```

**Strategy**: Ensures lighting consistency between character and background prompts through semantic mapping.

## Key Innovations

1. **Separation of Concerns**: Character and background prompts are generated independently to prevent cross-contamination
2. **Token Economy**: Fixed 20-token limits optimize AI image model performance
3. **Structured Templates**: Bullet points and numbered lists improve LLM comprehension
4. **Contextual Integration**: Character prompts incorporate scene analysis for natural positioning
5. **Robust Fallbacks**: Multiple layers of prompt generation ensure system reliability

## Prompt Evolution Analysis

The file shows three distinct iterations of prompt engineering:

### Version 1 (Lines 1-118): Basic Chain Implementation
- Simple story/character/background chains
- Basic prompt templates
- Manual prompt construction for image generation

### Version 2 (Lines 120-351): Enhanced Visual Extraction
- Introduction of specialized image prompt chains
- LLM-based visual element extraction
- Fallback mechanisms for reliability

### Version 3 (Lines 353-684): Advanced Token-Limited System
- 20-token constraint system
- Scene analysis integration
- Atmospheric consistency mapping
- Sophisticated compositional planning

## Results

This prompt engineering approach produces:
- Coherent visual narratives
- Optimized image generation prompts
- Consistent character-environment relationships
- Reliable system performance with graceful degradation

The multi-stage approach transforms simple user prompts into sophisticated, structured prompts that maximize AI image generation quality while maintaining narrative consistency.
