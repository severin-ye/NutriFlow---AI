"""
VisionTool - 使用Qwen-VL识别图像中的菜品和分量
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


# 初始化OpenAI客户端(兼容Qwen API)
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def detect_dishes_and_portions(image_path: str) -> str:
    """
    使用Qwen-VL识别餐盘图像中的菜品，并粗估分量。
    
    参数:
        image_path: 图片文件的绝对路径
    
    返回:
        JSON字符串格式: {"dishes": [...], "image_path": "..."}
        每个菜品包含：dish_id, name, category, estimated_weight_g, portion_level, reason
    """
    # 读取提示词
    prompt_path = os.path.join(PROMPTS_DIR, "vision_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # 读取图片并进行base64编码
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        # 正确的base64编码
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    try:
        # 调用Qwen-VL模型
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
                            "text": "请识别图像中的所有菜品并输出 JSON。"
                        }
                    ]
                }
            ],
            temperature=0.3
        )
        
        # 解析响应
        content = response.choices[0].message.content
        if not content:
            raise ValueError("模型返回内容为空")
        
        # 尝试提取JSON
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()
        
        dishes = json.loads(json_str)
        
        # 为每道菜添加dish_id
        for i, dish in enumerate(dishes):
            dish["dish_id"] = f"dish_{i+1}"
        
        # 返回JSON字符串格式
        result = {
            "dishes": dishes,
            "image_path": image_path
        }
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        print(f"视觉识别错误: {str(e)}")
        # 返回默认结果（JSON字符串格式）
        result = {
            "dishes": [
                {
                    "dish_id": "dish_1",
                    "name": "未识别菜品",
                    "category": "未知",
                    "estimated_weight_g": 200,
                    "portion_level": "medium",
                    "reason": f"识别失败: {str(e)}"
                }
            ],
            "image_path": image_path,
            "error": str(e)
        }
        return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    # 测试代码
    test_image = "test_meal.jpg"
    if os.path.exists(test_image):
        result = detect_dishes_and_portions.invoke({"image_path": test_image})
        print(json.dumps(result, ensure_ascii=False, indent=2))
