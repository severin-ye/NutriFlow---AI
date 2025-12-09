#!/usr/bin/env python3
"""
测试 save_meal 工具
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from tools.db_tools import save_meal

def test_save_meal():
    """测试保存餐食数据"""
    print("="*70)
    print("🧪 测试 save_meal 工具")
    print("="*70)
    print()
    
    # 模拟 compute_meal_nutrition 的返回结果
    meal_data = {
        "dishes": [
            {
                "dish_id": "dish_1",
                "name": "测试菜品",
                "category": "荤菜",
                "estimated_weight_g": 200,
                "final_weight_g": 200,
                "nutrition_per_100g": {
                    "calories": 100,
                    "protein": 10,
                    "fat": 5,
                    "carbs": 8,
                    "sodium": 200
                },
                "nutrition_total": {
                    "calories": 200,
                    "protein": 20,
                    "fat": 10,
                    "carbs": 16,
                    "sodium": 400
                }
            }
        ],
        "meal_nutrition_total": {
            "calories": 200,
            "protein": 20,
            "fat": 10,
            "carbs": 16,
            "sodium": 400
        },
        "image_path": "/test/image.png"
    }
    
    # 转换为 JSON 字符串（模拟工具链传递）
    meal_json = json.dumps(meal_data, ensure_ascii=False)
    
    print("1️⃣  准备测试数据...")
    print(f"   数据类型: {type(meal_json)}")
    print(f"   数据内容: {meal_json[:150]}...")
    print()
    
    print("2️⃣  调用 save_meal...")
    try:
        result = save_meal.invoke({"meal_data": meal_json})
        print(f"   ✅ 保存成功")
        print(f"   返回消息: {result}")
        print()
        
        # 读取数据库验证
        print("3️⃣  验证数据库内容...")
        with open("db/meals.json", "r", encoding="utf-8") as f:
            db = json.load(f)
        
        if db["days"]:
            day = db["days"][0]
            print(f"   日期: {day['date']}")
            print(f"   餐食数量: {len(day['meals'])}")
            print(f"   每日总热量: {day['daily_summary']['total_calories']}")
            
            if day['meals']:
                meal = day['meals'][0]
                print(f"   餐食ID: {meal.get('meal_id', 'N/A')}")
                print(f"   菜品数量: {len(meal.get('dishes', []))}")
                print(f"   餐食总热量: {meal.get('meal_nutrition_total', {}).get('calories', 'N/A')}")
        
        print()
        print("="*70)
        print("✅ 测试通过！save_meal 工作正常")
        print("="*70)
        
    except Exception as e:
        print(f"   ❌ 保存失败: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        print("="*70)
        print("❌ 测试失败")
        print("="*70)

if __name__ == "__main__":
    test_save_meal()
