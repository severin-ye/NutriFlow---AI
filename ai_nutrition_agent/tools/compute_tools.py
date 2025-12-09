"""
ComputeTool - 计算整餐营养总量
"""
import json
from langchain.tools import tool
from typing import List, Dict, Any


@tool
def compute_meal_nutrition(portion_result: str) -> str:
    """
    计算整餐的营养总量。
    
    参数:
        portion_result: 分量验证结果JSON字符串，包含 {"dishes": [...], "image_path": "..."}
    
    返回:
        JSON字符串格式: {"dishes": [...], "meal_nutrition_total": {...}, "image_path": "..."}
    """
    # 解析JSON字符串
    try:
        portion_data = json.loads(portion_result)
    except json.JSONDecodeError as e:
        print(f"⚠️  无法解析portion_result: {str(e)}")
        return json.dumps({"dishes": [], "meal_nutrition_total": {}, "error": "JSON解析失败"}, ensure_ascii=False)
    
    # 提取菜品列表和图片路径
    dishes = portion_data.get("dishes", [])
    image_path = portion_data.get("image_path", "")
    
    if not dishes:
        error_msg = "❌ compute_meal_nutrition: dishes列表为空"
        print(error_msg)
        return json.dumps({
            "dishes": [],
            "meal_nutrition_total": {},
            "image_path": image_path,
            "error": error_msg
        }, ensure_ascii=False)
    
    print(f"[DEBUG compute] 开始计算，共 {len(dishes)} 道菜")
    
    result_dishes = []
    meal_total = {
        "calories": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "carbs": 0.0,
        "sodium": 0.0
    }
    
    for dish in dishes:
        # 🔍 严格检查：必须有 final_weight_g
        if "final_weight_g" not in dish:
            error_msg = f"❌ compute: 菜品 {dish.get('name', 'unknown')} 缺少 final_weight_g 字段"
            print(error_msg)
            print(f"   菜品完整数据: {dish}")
            raise ValueError(error_msg)
        
        # 🔍 严格检查：必须有 nutrition_per_100g
        if "nutrition_per_100g" not in dish:
            error_msg = f"❌ compute: 菜品 {dish.get('name', 'unknown')} 缺少 nutrition_per_100g 字段"
            print(error_msg)
            print(f"   菜品完整数据: {dish}")
            raise ValueError(error_msg)
        
        # 获取最终重量
        weight_g = dish.get("final_weight_g", dish.get("estimated_weight_g", 100))
        
        # 获取每100g营养
        nutrition_per_100g = dish.get("nutrition_per_100g", {})
        
        print(f"[DEBUG compute] 菜品: {dish.get('name')}")
        print(f"[DEBUG compute]   重量: {weight_g}g")
        print(f"[DEBUG compute]   每100g营养: {nutrition_per_100g}")
        
        # 计算该菜品的总营养
        nutrition_total = {
            "calories": nutrition_per_100g.get("calories", 0) * weight_g / 100,
            "protein": nutrition_per_100g.get("protein", 0) * weight_g / 100,
            "fat": nutrition_per_100g.get("fat", 0) * weight_g / 100,
            "carbs": nutrition_per_100g.get("carbs", 0) * weight_g / 100,
            "sodium": nutrition_per_100g.get("sodium", 0) * weight_g / 100
        }
        
        print(f"[DEBUG compute]   计算后总营养: {nutrition_total}")
        
        # 更新菜品数据
        dish_copy = dish.copy()
        dish_copy["nutrition_total"] = nutrition_total
        result_dishes.append(dish_copy)
        
        # 累加到整餐总计
        for key in meal_total:
            meal_total[key] += nutrition_total[key]
    
    # 四舍五入
    for key in meal_total:
        meal_total[key] = round(meal_total[key], 2)
    
    print(f"[DEBUG compute] ✅ 计算完成")
    print(f"[DEBUG compute]   整餐总营养: {meal_total}")
    
    # 🔍 严格检查：如果所有营养值都是0，抛出错误
    if all(v == 0 for v in meal_total.values()):
        error_msg = "❌ CRITICAL: 计算结果全为0，数据异常！"
        print(error_msg)
        print(f"   dishes数据: {dishes}")
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
    根据营养数据给本餐打分(使用简单规则)。
    注意：在实际Agent中，这个功能会由LLM通过prompt完成。
    这里提供一个简单的规则版本作为备用。
    
    参数:
        nutrition: 营养数据字典
    
    返回:
        包含score和advice
    """
    score = 100
    advice_parts = []
    
    calories = nutrition.get("calories", 0)
    protein = nutrition.get("protein", 0)
    fat = nutrition.get("fat", 0)
    carbs = nutrition.get("carbs", 0)
    sodium = nutrition.get("sodium", 0)
    
    # 评分规则
    # 1. 热量评估 (建议500-800)
    if calories < 400:
        score -= 10
        advice_parts.append("热量偏低")
    elif calories > 900:
        score -= 15
        advice_parts.append("热量偏高")
    
    # 2. 蛋白质评估 (建议>20g)
    if protein < 15:
        score -= 15
        advice_parts.append("蛋白质不足")
    elif protein > 50:
        score -= 5
        advice_parts.append("蛋白质偏多")
    else:
        advice_parts.append("蛋白质充足")
    
    # 3. 脂肪评估 (建议<30g)
    if fat > 35:
        score -= 15
        advice_parts.append("脂肪含量偏高")
    
    # 4. 碳水评估 (建议40-100g)
    if carbs < 30:
        score -= 10
        advice_parts.append("碳水不足")
    elif carbs > 120:
        score -= 10
        advice_parts.append("碳水偏多")
    
    # 5. 钠评估 (建议<1000mg)
    if sodium > 1200:
        score -= 15
        advice_parts.append("钠含量偏高，建议减少盐分摄入")
    elif sodium > 800:
        score -= 5
        advice_parts.append("钠含量略高")
    
    # 确保分数在0-100之间
    score = max(0, min(100, score))
    
    advice = "；".join(advice_parts) if advice_parts else "营养均衡"
    
    return {
        "score": score,
        "advice": advice
    }


if __name__ == "__main__":
    # 测试代码
    test_dishes = [
        {
            "dish_id": "dish_1",
            "name": "白米饭",
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
            "name": "宫保鸡丁",
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
    
    # 测试评分
    score_result = score_current_meal.invoke({"nutrition": result["meal_nutrition_total"]})
    print("\n评分结果:")
    print(json.dumps(score_result, ensure_ascii=False, indent=2))
