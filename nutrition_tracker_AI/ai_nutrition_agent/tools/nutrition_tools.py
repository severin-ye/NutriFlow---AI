"""
NutritionTool - Online query dish nutrition data
Use Qwen-Plus + web search to get real-time accurate nutrition information
"""
import json
from openai import OpenAI
from langchain.tools import tool
from typing import Dict, Any, Optional

from config.settings import (
    DASHSCOPE_API_KEY,
    QWEN_BASE_URL,
    QWEN_TEXT_MODEL
)


# Initialize OpenAI client (compatible with Qwen API)
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def query_nutrition_per_100g(dish_name: str) -> Dict[str, float]:
    """
    Query nutrition per 100g of a dish online. Use Qwen-Plus model combined with web search to get the most accurate nutrition data.
    
    Args:
        dish_name: Dish name
    
    Returns:
        Nutrition dictionary containing: calories, protein, fat, carbs, sodium
    """
    print(f"[DEBUG nutrition] Querying dish: {dish_name}")
    
    # Build query prompt
    prompt = f"""Please search for the nutritional components per 100g of "{dish_name}".

Requirements:
1. Use web search to obtain authoritative nutrition data (priority: Chinese Food Composition Table, USDA database, official nutrition sites)
2. If it is a complex dish (e.g., Kung Pao Chicken), estimate the average nutrition based on common preparation
3. You must output strictly in the following JSON format, do NOT add any extra text:

{{
  "calories": number (kcal/100g),
  "protein": number (g/100g),
  "fat": number (g/100g),
  "carbs": number (g/100g),
  "sodium": number (mg/100g)
}}

Notes:
- All values must be numbers, no units
- All 5 fields must be included
- Only output JSON, no explanation
"""
    
    try:
        # Call Qwen-Plus model (supports web search)
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional nutrition data assistant. You can search the web and return accurate nutrition information in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
        )
        
        content = response.choices[0].message.content
        
        if not content:
            raise ValueError("Model returned empty content")
        
        json_str = content.strip()
        
        # Handle possible markdown code blocks
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        nutrition_data = json.loads(json_str)
        
        required_fields = ["calories", "protein", "fat", "carbs", "sodium"]
        for field in required_fields:
            if field not in nutrition_data:
                raise ValueError(f"Missing required field: {field}")
            nutrition_data[field] = float(nutrition_data[field])
        
        print(f"✅ Nutrition query success: {dish_name} -> {nutrition_data}")
        
        return nutrition_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse failed: {str(e)}")
        print(f"Raw content: {content}")
        return _get_fallback_nutrition(dish_name)
    
    except Exception as e:
        print(f"❌ Nutrition query error: {str(e)}")
        return _get_fallback_nutrition(dish_name)


def _get_fallback_nutrition(dish_name: str) -> Dict[str, float]:
    """
    Return estimated values when online query fails
    """
    dish_lower = dish_name.lower()
    
    # Staple foods
    if any(keyword in dish_name for keyword in ["米饭", "馒头", "面条", "面包", "饼"]):
        return {
            "calories": 120.0,
            "protein": 3.0,
            "fat": 0.5,
            "carbs": 25.0,
            "sodium": 5.0
        }
    
    # Meats
    elif any(keyword in dish_name for keyword in ["鸡", "猪", "牛", "羊", "鱼", "虾", "肉"]):
        return {
            "calories": 180.0,
            "protein": 20.0,
            "fat": 10.0,
            "carbs": 2.0,
            "sodium": 300.0
        }
    
    # Vegetables
    elif any(keyword in dish_name for keyword in ["菜", "瓜", "笋", "菌", "豆", "芽"]):
        return {
            "calories": 30.0,
            "protein": 2.0,
            "fat": 0.3,
            "carbs": 5.0,
            "sodium": 50.0
        }
    
    # Soups
    elif any(keyword in dish_name for keyword in ["汤", "羹"]):
        return {
            "calories": 25.0,
            "protein": 1.5,
            "fat": 1.0,
            "carbs": 3.0,
            "sodium": 250.0
        }
    
    # Default (mixed dishes)
    else:
        return {
            "calories": 100.0,
            "protein": 5.0,
            "fat": 4.0,
            "carbs": 12.0,
            "sodium": 200.0
        }


@tool
def add_nutrition_to_dishes(portion_result: str) -> str:
    """
    Add nutrition data to dish list. Must be called before compute!
    """
    print("[DEBUG add_nutrition] Starting nutrition lookup")
    
    try:
        portion_data = json.loads(portion_result)
    except json.JSONDecodeError as e:
        error_msg = f"❌ add_nutrition: Failed to parse portion_result - {str(e)}"
        print(error_msg)
        return json.dumps({"dishes": [], "image_path": "", "error": error_msg}, ensure_ascii=False)
    
    dishes = portion_data.get("dishes", [])
    image_path = portion_data.get("image_path", "")
    
    if not dishes:
        error_msg = "❌ add_nutrition: dishes list is empty"
        print(error_msg)
        return json.dumps({"dishes": [], "image_path": image_path, "error": error_msg}, ensure_ascii=False)
    
    print(f"[DEBUG add_nutrition] {len(dishes)} dishes need nutrition lookup")
    
    result_dishes = []
    for i, dish in enumerate(dishes, 1):
        dish_name = dish.get("name", "Unknown dish")
        print(f"[DEBUG add_nutrition] {i}/{len(dishes)} Querying: {dish_name}")
        
        try:
            nutrition = query_nutrition_per_100g.invoke({"dish_name": dish_name})
            dish["nutrition_per_100g"] = nutrition
            print(f"[DEBUG add_nutrition]   ✅ Success: {nutrition}")
            
        except Exception as e:
            error_msg = f"Query failed: {str(e)}"
            print(f"[DEBUG add_nutrition]   ⚠️  {error_msg}")
            dish["nutrition_per_100g"] = _get_fallback_nutrition(dish_name)
            print(f"[DEBUG add_nutrition]   Using fallback: {dish['nutrition_per_100g']}")
        
        result_dishes.append(dish)
    
    result = {
        "dishes": result_dishes,
        "image_path": image_path
    }
    
    print(f"[DEBUG add_nutrition] ✅ All dishes updated with nutrition")
    return json.dumps(result, ensure_ascii=False)

