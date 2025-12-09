"""
ComputeTool - Calculate total meal nutrition
"""
import json
from langchain.tools import tool
from typing import List, Dict, Any


@tool
def compute_meal_nutrition(portion_result: str) -> str:
    """
    Calculate total nutrition for the meal.
    
    Args:
        portion_result: Portion verification result JSON string, containing {"dishes": [...], "image_path": "..."}
    
    Returns:
        JSON string format: {"dishes": [...], "meal_nutrition_total": {...}, "image_path": "..."}
    """
    # Parse JSON string
    try:
        portion_data = json.loads(portion_result)
    except json.JSONDecodeError as e:
        print(f"⚠️  Unable to parse portion_result: {str(e)}")
        return json.dumps({"dishes": [], "meal_nutrition_total": {}, "error": "JSON parsing failed"}, ensure_ascii=False)
    
    # Extract dish list and image path
    dishes = portion_data.get("dishes", [])
    image_path = portion_data.get("image_path", "")
    
    if not dishes:
        error_msg = "❌ compute_meal_nutrition: dishes list is empty"
        print(error_msg)
        return json.dumps({
            "dishes": [],
            "meal_nutrition_total": {},
            "image_path": image_path,
            "error": error_msg
        }, ensure_ascii=False)
    
    print(f"[DEBUG compute] Starting calculation, total {len(dishes)} dishes")
    
    result_dishes = []
    meal_total = {
        "calories": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "carbs": 0.0,
        "sodium": 0.0
    }
    
    for dish in dishes:
        # 🔍 Strict check: must have final_weight_g
        if "final_weight_g" not in dish:
            error_msg = f"❌ compute: Dish {dish.get('name', 'unknown')} is missing final_weight_g field"
            print(error_msg)
            print(f"   Full dish data: {dish}")
            raise ValueError(error_msg)
        
        # 🔍 Strict check: must have nutrition_per_100g
        if "nutrition_per_100g" not in dish:
            error_msg = f"❌ compute: Dish {dish.get('name', 'unknown')} is missing nutrition_per_100g field"
            print(error_msg)
            print(f"   Full dish data: {dish}")
            raise ValueError(error_msg)
        
        # Get final weight
        weight_g = dish.get("final_weight_g", dish.get("estimated_weight_g", 100))
        
        # Get nutrition per 100g
        nutrition_per_100g = dish.get("nutrition_per_100g", {})
        
        print(f"[DEBUG compute] Dish: {dish.get('name')}")
        print(f"[DEBUG compute]   Weight: {weight_g}g")
        print(f"[DEBUG compute]   Nutrition per 100g: {nutrition_per_100g}")
        
        # Compute total nutrition for the dish
        nutrition_total = {
            "calories": nutrition_per_100g.get("calories", 0) * weight_g / 100,
            "protein": nutrition_per_100g.get("protein", 0) * weight_g / 100,
            "fat": nutrition_per_100g.get("fat", 0) * weight_g / 100,
            "carbs": nutrition_per_100g.get("carbs", 0) * weight_g / 100,
            "sodium": nutrition_per_100g.get("sodium", 0) * weight_g / 100
        }
        
        print(f"[DEBUG compute]   Total nutrition after calculation: {nutrition_total}")
        
        # Update dish data
        dish_copy = dish.copy()
        dish_copy["nutrition_total"] = nutrition_total
        result_dishes.append(dish_copy)
        
        # Add to overall meal total
        for key in meal_total:
            meal_total[key] += nutrition_total[key]
    
    # Round values
    for key in meal_total:
        meal_total[key] = round(meal_total[key], 2)
    
    print(f"[DEBUG compute] ✅ Calculation complete")
    print(f"[DEBUG compute]   Total meal nutrition: {meal_total}")
    
    # 🔍 Strict check: if everything is zero, error
    if all(v == 0 for v in meal_total.values()):
        error_msg = "❌ CRITICAL: All computed values are 0, data abnormal!"
        print(error_msg)
        print(f"   dishes data: {dishes}")
        raise ValueError(error_msg)
    
    result = {
        "dishes": result_dishes,
        "meal_nutrition_total": meal_total,
        "image_path": image_path
    }
    return json.dumps(result, ensure_ascii=False)
    return json.dumps(result, ensure_ascii=False)


@tool  
def score_current_meal(nutrition: Dict[str, float]) -> Dict[str, Any]:
    """
    Score the meal based on nutrition (simple rule-based version).
    Note: In the real Agent system, this will be handled by an LLM via prompt.
    This provides a simple fallback rule version.
    
    Parameters:
        nutrition: Nutrition dictionary
    
    Returns:
        Contains score and advice
    """
    score = 100
    advice_parts = []
    
    calories = nutrition.get("calories", 0)
    protein = nutrition.get("protein", 0)
    fat = nutrition.get("fat", 0)
    carbs = nutrition.get("carbs", 0)
    sodium = nutrition.get("sodium", 0)
    
    # Scoring rules
    # 1. Calories (recommended 500-800)
    if calories < 400:
        score -= 10
        advice_parts.append("Low calories")
    elif calories > 900:
        score -= 15
        advice_parts.append("High calories")
    
    # 2. Protein (recommended >20g)
    if protein < 15:
        score -= 15
        advice_parts.append("Insufficient protein")
    elif protein > 50:
        score -= 5
        advice_parts.append("Too much protein")
    else:
        advice_parts.append("Good protein level")
    
    # 3. Fat (recommended <30g)
    if fat > 35:
        score -= 15
        advice_parts.append("Fat content too high")
    
    # 4. Carbs (recommended 40-100g)
    if carbs < 30:
        score -= 10
        advice_parts.append("Carbs too low")
    elif carbs > 120:
        score -= 10
        advice_parts.append("Carbs too high")
    
    # 5. Sodium (recommended <1000mg)
    if sodium > 1200:
        score -= 15
        advice_parts.append("Sodium too high, reduce salt intake")
    elif sodium > 800:
        score -= 5
        advice_parts.append("Sodium slightly high")
    
    # Ensure 0–100 range
    score = max(0, min(100, score))
    
    advice = "；".join(advice_parts) if advice_parts else "Balanced nutrition"
    
    return {
        "score": score,
        "advice": advice
    }


if __name__ == "__main__":
    # Test code
    test_dishes = [
        {
            "dish_id": "dish_1",
            "name": "White rice",
            "final_weight_g": 180,
            "nutrition_per_100g": {
                "calories": 116,
                "protein": 2.6,
                "fat": 0.3,
                "carbs": 25.6,
                "sodium": 2
            }
        },
        {
            "dish_id": "dish_2",
            "name": "Kung Pao Chicken",
            "final_weight_g": 160,
            "nutrition_per_100g": {
                "calories": 195,
                "protein": 18.5,
                "fat": 11.2,
                "carbs": 7.8,
                "sodium": 850
            }
        }
    ]
    
    result = compute_meal_nutrition.invoke({"dishes": test_dishes})
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Test scoring
    score_result = score_current_meal.invoke({"nutrition": result["meal_nutrition_total"]})
    print("\nScore result:")
    print(json.dumps(score_result, ensure_ascii=False, indent=2))

