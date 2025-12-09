"""
VisionTool - Use Qwen-VL to recognize dishes and portions in images
"""
import json
import os
import base64
from openai import OpenAI
from langchain.tools import tool
from typing import List, Dict, Any

from config.settings import (
    DASHSCOPE_API_KEY,
    QWEN_BASE_URL,
    QWEN_VL_MODEL,
    PROMPTS_DIR
)
from schemas.tool_schema import VisionInput


# Initialize OpenAI client (compatible with Qwen API)
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def detect_dishes_and_portions(image_path: str) -> str:
    """
    Use Qwen-VL to recognize dishes in meal image and estimate portions.
    
    Args:
        image_path: Absolute path to the image file
    
    Returns:
        JSON string format: {"dishes": [...], "image_path": "..."}
        Each dish contains: dish_id, name, category, estimated_weight_g, portion_level, reason
    """
    # Read prompt
    prompt_path = os.path.join(PROMPTS_DIR, "vision_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # Read image and perform base64 encoding
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        # Correct base64 encoding
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    try:
        # Call Qwen-VL model
        response = client.chat.completions.create(
            model=QWEN_VL_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Please identify all dishes in the image and output JSON."
                        }
                    ]
                }
            ],
            temperature=0.3
        )
        
        # Parse response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Model returned empty content")
        
        # Try to extract JSON
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()
        
        dishes = json.loads(json_str)
        
        # Add dish_id for each dish
        for i, dish in enumerate(dishes):
            dish["dish_id"] = f"dish_{i+1}"
            
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(dishes, f, ensure_ascii=False, indent=2)

        
        # Return JSON string format
        result = {
            "dishes": dishes,
            "image_path": image_path
        }
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        print(f"Vision recognition error: {str(e)}")
        # Return default result (JSON string format)
        result = {
            "dishes": [
                {
                    "dish_id": "dish_1",
                    "name": "Unrecognized dish",
                    "category": "Unknown",
                    "estimated_weight_g": 200,
                    "portion_level": "medium",
                    "reason": f"Recognition failed: {str(e)}"
                }
            ],
            "image_path": image_path,
            "error": str(e)
        }
        return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    # Test code
    test_image = "test_meal.jpg"
    if os.path.exists(test_image):
        result = detect_dishes_and_portions.invoke({"image_path": test_image})
        print(json.dumps(result, ensure_ascii=False, indent=2))
