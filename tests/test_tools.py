#!/usr/bin/env python3
"""
快速测试工具链的数据传递
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from tools.vision_tools import detect_dishes_and_portions
from tools.portion_tools import check_and_refine_portions
from tools.compute_tools import compute_meal_nutrition

def test_tool_chain():
    """测试工具链数据传递"""
    print("="*70)
    print("🧪 测试工具链数据传递")
    print("="*70)
    print()
    
    # 1. 模拟 vision_tools 的返回值
    print("1️⃣  模拟 vision_tools 返回值...")
    mock_vision_result = {
        "dishes": [
            {
                "dish_id": "dish_1",
                "name": "宫保鸡丁",
                "category": "荤菜",
                "estimated_weight_g": 150,
                "portion_level": "medium",
                "reason": "测试数据"
            }
        ],
        "image_path": "/test/image.png"
    }
    
    # 转换为 JSON 字符串（模拟 LangChain 的行为）
    vision_result_str = json.dumps(mock_vision_result, ensure_ascii=False)
    print(f"   返回类型: {type(vision_result_str)}")
    print(f"   返回内容: {vision_result_str[:100]}...")
    print()
    
    # 2. 测试 portion_tools 接收
    print("2️⃣  测试 portion_tools.check_and_refine_portions...")
    print("   ⚠️  注意：这会真实调用 Qwen-Plus API")
    try:
        # 使用 .invoke() 方法调用（LangChain 标准方式）
        portion_result = check_and_refine_portions.invoke({"vision_result": vision_result_str})
        print(f"   ✅ 调用成功")
        print(f"   返回类型: {type(portion_result)}")
        
        # 解析返回结果查看
        if isinstance(portion_result, str):
            parsed = json.loads(portion_result)
            print(f"   返回的dishes数量: {len(parsed.get('dishes', []))}")
            if parsed.get('dishes'):
                first_dish = parsed['dishes'][0]
                print(f"   第一个dish有final_weight_g: {'final_weight_g' in first_dish}")
        print()
        
        # 3. 测试 compute_tools 接收
        print("3️⃣  测试 compute_tools.compute_meal_nutrition...")
        compute_result = compute_meal_nutrition.invoke({"portion_result": portion_result})
        print(f"   ✅ 调用成功")
        print(f"   返回类型: {type(compute_result)}")
        print(f"   返回内容: {compute_result[:200] if isinstance(compute_result, str) else compute_result}...")
        print()
        
        print("="*70)
        print("✅ 所有测试通过！工具链数据传递正常")
        print("="*70)
        
    except Exception as e:
        print(f"   ❌ 调用失败: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        print("="*70)
        print("❌ 测试失败！需要修复")
        print("="*70)

if __name__ == "__main__":
    test_tool_chain()
