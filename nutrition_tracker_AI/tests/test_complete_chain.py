#!/usr/bin/env python3
"""
完整测试工具链：vision → portion → add_nutrition → compute → save
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from tools.vision_tools import detect_dishes_and_portions
from tools.portion_tools import check_and_refine_portions
from tools.nutrition_tools import add_nutrition_to_dishes
from tools.compute_tools import compute_meal_nutrition
from tools.db_tools import save_meal

def test_complete_chain():
    """测试完整工具链"""
    print("="*70)
    print("🧪 测试完整工具链")
    print("="*70)
    print()
    
    # 1. 模拟 vision 结果
    print("1️⃣  模拟 vision_tools 返回值...")
    vision_result = json.dumps({
        "dishes": [{
            "dish_id": "dish_1",
            "name": "宫保鸡丁",
            "category": "荤菜",
            "estimated_weight_g": 300,
            "portion_level": "large",
            "reason": "测试数据"
        }],
        "image_path": "/test/image.png"
    }, ensure_ascii=False)
    print(f"   ✅ vision_result准备完成")
    print()
    
    # 2. portion 验证
    print("2️⃣  调用 check_and_refine_portions...")
    try:
        portion_result = check_and_refine_portions.invoke({"vision_result": vision_result})
        print(f"   ✅ portion完成")
        portion_data = json.loads(portion_result)
        print(f"   菜品数: {len(portion_data['dishes'])}")
        print(f"   有final_weight_g: {'final_weight_g' in portion_data['dishes'][0]}")
        print()
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return
    
    # 3. 添加营养数据 ← 关键步骤
    print("3️⃣  调用 add_nutrition_to_dishes...")
    try:
        nutrition_result = add_nutrition_to_dishes.invoke({"portion_result": portion_result})
        print(f"   ✅ nutrition完成")
        nutrition_data = json.loads(nutrition_result)
        print(f"   菜品数: {len(nutrition_data['dishes'])}")
        print(f"   有nutrition_per_100g: {'nutrition_per_100g' in nutrition_data['dishes'][0]}")
        if 'nutrition_per_100g' in nutrition_data['dishes'][0]:
            print(f"   营养数据: {nutrition_data['dishes'][0]['nutrition_per_100g']}")
        print()
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 计算总营养
    print("4️⃣  调用 compute_meal_nutrition...")
    try:
        compute_result = compute_meal_nutrition.invoke({"portion_result": nutrition_result})
        print(f"   ✅ compute完成")
        compute_data = json.loads(compute_result)
        print(f"   整餐总营养: {compute_data.get('meal_nutrition_total', {})}")
        print()
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 5. 保存到数据库
    print("5️⃣  调用 save_meal...")
    try:
        save_result = save_meal.invoke({"meal_data": compute_result})
        print(f"   ✅ save完成")
        print(f"   结果: {save_result}")
        print()
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("="*70)
    print("✅ 完整工具链测试通过！")
    print("="*70)

if __name__ == "__main__":
    test_complete_chain()
