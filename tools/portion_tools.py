"""
PortionTool - 使用Qwen-Plus验证和修正菜品分量
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


# 初始化OpenAI客户端
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def check_and_refine_portions(dishes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检查菜品分量估计是否合理，不合理则重新估算。
    
    参数:
        dishes: 菜品列表，包含初步的重量估计
    
    返回:
        修正后的菜品列表，包含最终确认的重量
    """
    # 读取提示词
    prompt_path = os.path.join(PROMPTS_DIR, "portion_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # 准备输入数据
    input_data = []
    for dish in dishes:
        input_data.append({
            "dish_id": dish.get("dish_id"),
            "name": dish.get("name"),
            "category": dish.get("category"),
            "estimated_weight_g": dish.get("estimated_weight_g")
        })
    
    try:
        # 调用Qwen-Plus进行验证
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
        
        # 解析响应
        content = response.choices[0].message.content
        if not content:
            raise ValueError("模型返回内容为空")
        
        # 提取JSON
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()
        
        verification_results = json.loads(json_str)
        
        # 将验证结果合并到原始菜品数据中
        result_dishes = []
        for dish in dishes:
            dish_id = dish.get("dish_id")
            
            # 查找对应的验证结果
            verification = next(
                (v for v in verification_results if v.get("dish_id") == dish_id),
                None
            )
            
            if verification:
                dish["final_weight_g"] = verification.get("final_weight_g", dish.get("estimated_weight_g"))
                dish["is_reasonable"] = verification.get("is_reasonable", True)
                dish["verification_reason"] = verification.get("reason", "")
            else:
                # 如果没有验证结果，使用原始估计
                dish["final_weight_g"] = dish.get("estimated_weight_g")
                dish["is_reasonable"] = True
                dish["verification_reason"] = "未进行验证"
            
            result_dishes.append(dish)
        
        return result_dishes
    
    except Exception as e:
        print(f"分量验证错误: {str(e)}")
        # 如果验证失败，使用原始估计
        for dish in dishes:
            dish["final_weight_g"] = dish.get("estimated_weight_g")
            dish["is_reasonable"] = True
            dish["verification_reason"] = f"验证失败: {str(e)}"
        return dishes


if __name__ == "__main__":
    # 测试代码
    test_dishes = [
        {
            "dish_id": "dish_1",
            "name": "白米饭",
            "category": "主食",
            "estimated_weight_g": 30
        }
    ]
    result = check_and_refine_portions.invoke({"dishes": test_dishes})
    print(json.dumps(result, ensure_ascii=False, indent=2))
