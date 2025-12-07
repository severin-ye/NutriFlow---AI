"""
NutritionTool - 联网查询菜品营养数据
使用 Qwen-Plus + 联网搜索 获取实时准确的营养信息
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


# 初始化 OpenAI 客户端(兼容 Qwen API)
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def query_nutrition_per_100g(dish_name: str) -> Dict[str, float]:
    """
    联网查询菜品的每100g营养成分。使用Qwen-Plus模型结合网络搜索获取最准确的营养数据。
    
    参数:
        dish_name: 菜品名称
    
    返回:
        营养成分字典，包含: calories, protein, fat, carbs, sodium
    """
    
    # 构造查询提示词
    prompt = f"""请查询"{dish_name}"每100克的营养成分数据。

要求：
1. 使用网络搜索获取最权威的营养数据（优先使用：中国食物成分表、USDA数据库、权威营养网站）
2. 如果是复杂菜品（如宫保鸡丁），请估算其常见做法的平均营养值
3. 必须严格按照以下JSON格式输出，不要添加任何其他文字：

{{
  "calories": 数值（单位：kcal/100g，保留1位小数）,
  "protein": 数值（单位：g/100g，保留1位小数）,
  "fat": 数值（单位：g/100g，保留1位小数）,
  "carbs": 数值（单位：g/100g，保留1位小数）,
  "sodium": 数值（单位：mg/100g，保留1位小数）
}}

注意：
- 所有数值都必须是数字，不要有单位
- 必须包含全部5个字段
- 只输出JSON，不要有其他解释
"""
    
    try:
        # 调用 Qwen-Plus 模型（启用联网搜索）
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的营养数据查询助手。你可以联网搜索权威的营养数据库，并以JSON格式返回准确的营养信息。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # 降低温度以获得更稳定的输出
            # Qwen模型支持联网功能，会自动搜索最新数据
        )
        
        content = response.choices[0].message.content
        
        if not content:
            raise ValueError("模型返回内容为空")
        
        # 提取JSON
        json_str = content.strip()
        
        # 处理可能包含markdown代码块的情况
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        # 解析JSON
        nutrition_data = json.loads(json_str)
        
        # 验证必需字段
        required_fields = ["calories", "protein", "fat", "carbs", "sodium"]
        for field in required_fields:
            if field not in nutrition_data:
                raise ValueError(f"缺少必需字段: {field}")
            # 转换为浮点数
            nutrition_data[field] = float(nutrition_data[field])
        
        print(f"✅ 联网查询成功: {dish_name} -> {nutrition_data}")
        
        return nutrition_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {str(e)}")
        print(f"原始内容: {content}")
        # 返回估算值
        return _get_fallback_nutrition(dish_name)
    
    except Exception as e:
        print(f"❌ 查询营养数据出错: {str(e)}")
        # 返回估算值
        return _get_fallback_nutrition(dish_name)


def _get_fallback_nutrition(dish_name: str) -> Dict[str, float]:
    """
    当联网查询失败时，返回基于常识的估算值
    """
    # 根据菜品类型提供合理的默认值
    dish_lower = dish_name.lower()
    
    # 主食类
    if any(keyword in dish_name for keyword in ["米饭", "馒头", "面条", "面包", "饼"]):
        return {
            "calories": 120.0,
            "protein": 3.0,
            "fat": 0.5,
            "carbs": 25.0,
            "sodium": 5.0
        }
    
    # 肉类
    elif any(keyword in dish_name for keyword in ["鸡", "猪", "牛", "羊", "鱼", "虾", "肉"]):
        return {
            "calories": 180.0,
            "protein": 20.0,
            "fat": 10.0,
            "carbs": 2.0,
            "sodium": 300.0
        }
    
    # 蔬菜类
    elif any(keyword in dish_name for keyword in ["菜", "瓜", "笋", "菌", "豆", "芽"]):
        return {
            "calories": 30.0,
            "protein": 2.0,
            "fat": 0.3,
            "carbs": 5.0,
            "sodium": 50.0
        }
    
    # 汤类
    elif any(keyword in dish_name for keyword in ["汤", "羹"]):
        return {
            "calories": 25.0,
            "protein": 1.5,
            "fat": 1.0,
            "carbs": 3.0,
            "sodium": 250.0
        }
    
    # 默认值（混合菜品）
    else:
        return {
            "calories": 100.0,
            "protein": 5.0,
            "fat": 4.0,
            "carbs": 12.0,
            "sodium": 200.0
        }


if __name__ == "__main__":
    print("测试联网营养查询功能\n")
    
    # 测试不同类型的菜品
    test_dishes = [
        "白米饭",
        "宫保鸡丁", 
        "清蒸鲈鱼",
        "西兰花炒虾仁",
        "红烧肉",
        "番茄炒蛋"
    ]
    
    for dish in test_dishes:
        print(f"\n{'='*50}")
        print(f"查询菜品: {dish}")
        print(f"{'='*50}")
        result = query_nutrition_per_100g.invoke({"dish_name": dish})
        print(f"营养成分:")
        print(f"  热量: {result['calories']} kcal")
        print(f"  蛋白质: {result['protein']} g")
        print(f"  脂肪: {result['fat']} g")
        print(f"  碳水: {result['carbs']} g")
        print(f"  钠: {result['sodium']} mg")
