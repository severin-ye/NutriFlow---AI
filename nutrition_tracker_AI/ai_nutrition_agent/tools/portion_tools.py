"""
PortionTool - Use Qwen-Plus to verify and refine dish portions
"""
import json
import os
from openai import OpenAI
from langchain.tools import tool
from typing import List, Dict, Any

from config.settings import (
    DASHSCOPE_API_KEY,
    QWEN_BASE_URL,
    QWEN_TEXT_MODEL,
    PROMPTS_DIR
)


# Initialize OpenAI client
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def check_and_refine_portions(vision_result: str) -> str:
    """
    Check if dish portion estimates are reasonable, re-estimate if unreasonable.
    
    Args:
        vision_result: Vision recognition result JSON string, containing {"dishes": [...], "image_path": "..."}
    
    Returns:
        JSON string format: {"dishes": [...], "image_path": "..."}
    """
    # Parse JSON string
    try:
        vision_data = json.loads(vision_result)
    except json.JSONDecodeError as e:
        print(f"⚠️  Unable to parse vision_result: {str(e)}")
        return json.dumps({"dishes": [], "image_path": "", "error": "JSON parsing failed"}, ensure_ascii=False)
    
    # Extract dish list and image path
    dishes = vision_data.get("dishes", [])
    image_path = vision_data.get("image_path", "")
    
    # Verify list is not empty
    if not dishes:
        print(f"⚠️  dishes list is empty")
        return json.dumps({"dishes": [], "image_path": image_path, "error": "Dish list is empty"}, ensure_ascii=False)
    
    # Read prompt
    prompt_path = os.path.join(PROMPTS_DIR, "portion_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # Prepare input data
    input_data = []
    for dish in dishes:
        input_data.append({
            "dish_id": dish.get("dish_id"),
            "name": dish.get("name"),
            "category": dish.get("category"),
            "estimated_weight_g": dish.get("estimated_weight_g")
        })
    
    try:
        # Call Qwen-Plus for verification
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(input_data, ensure_ascii=False, indent=2)
                }
            ],
            temperature=0.2
        )
        
        # Parse response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Model returned empty content")
        
        # Extract JSON
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()
        
        verification_results = json.loads(json_str)
        
        # 🔧 Fix: If LLM returns a single dict instead of list, convert to list
        if isinstance(verification_results, dict) and "dish_id" in verification_results:
            verification_results = [verification_results]
        
        # Merge verification results into original dish data
        result_dishes = []
        for dish in dishes:
            dish_id = dish.get("dish_id")
            
            # Find corresponding verification result
            verification = next(
                (v for v in verification_results if isinstance(v, dict) and v.get("dish_id") == dish_id),
                None
            )
            
            if verification:
                dish["final_weight_g"] = verification.get("final_weight_g", dish.get("estimated_weight_g"))
                dish["is_reasonable"] = verification.get("is_reasonable", True)
                dish["verification_reason"] = verification.get("reason", "")
            else:
                # If no verification result, use original estimate
                dish["final_weight_g"] = dish.get("estimated_weight_g")
                dish["is_reasonable"] = True
                dish["verification_reason"] = "Not verified"
            
            result_dishes.append(dish)
        
        print(f"✅ Portion verification complete, total {len(result_dishes)} dishes")
        result = {
            "dishes": result_dishes,
            "image_path": image_path
        }
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        print(f"Portion verification error: {str(e)}")
        # Return original data (add default final_weight_g)
        for dish in dishes:
            if "final_weight_g" not in dish:
                dish["final_weight_g"] = dish.get("estimated_weight_g", 200)
                dish["is_reasonable"] = True
                dish["verification_reason"] = "Verification failed, using initial estimate"
        
        result = {
            "dishes": dishes,
            "image_path": image_path,
            "error": str(e)
        }
        return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    # Test code
    test_dishes = [
        {
            "dish_id": "dish_1",
            "name": "White Rice",
            "category": "Staple",
            "estimated_weight_g": 30
        }
    ]
    result = check_and_refine_portions.invoke({"dishes": test_dishes})
    print(json.dumps(result, ensure_ascii=False, indent=2))
