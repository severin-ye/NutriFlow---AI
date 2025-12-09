"""
RecommendationTools - Use Qwen-Plus to provide next meal recommendations and trend scoring
"""
import json
import os
from openai import OpenAI
from langchain.tools import tool
from typing import Dict, Any

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
def score_current_meal_llm(nutrition: Dict[str, float]) -> Dict[str, Any]:
    """
    Use Qwen-Plus to score and advise on current meal (LLM-based).
    
    Args:
        nutrition: Current meal nutrition data
    
    Returns:
        Contains score and advice
    """
    # Read prompt
    prompt_path = os.path.join(PROMPTS_DIR, "score_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    try:
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(nutrition, ensure_ascii=False, indent=2)}
            ],
            temperature=0.3
        )
        
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
        
        result = json.loads(json_str)
        return result
    
    except Exception as e:
        print(f"本餐评分错误: {str(e)}")
        return {
            "score": 70,
            "advice": "评分系统暂时不可用"
        }


@tool
def score_weekly_adjusted(current_meal: Dict[str, Any], weekly_trend: Dict[str, Any]) -> Dict[str, Any]:
    """
    基于一周趋势给出调整后的评分和建议。
    
    参数:
        current_meal: 当前餐的营养数据
        weekly_trend: 最近一周的营养趋势统计
    
    返回:
        包含score和advice
    """
    # 读取提示词
    prompt_path = os.path.join(PROMPTS_DIR, "trend_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    input_data = {
        "current_meal": current_meal,
        "weekly_trend": weekly_trend
    }
    
    try:
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(input_data, ensure_ascii=False, indent=2)}
            ],
            temperature=0.3
        )
        
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
        
        result = json.loads(json_str)
        return result
    
    except Exception as e:
        print(f"趋势评分错误: {str(e)}")
        return {
            "score": 70,
            "advice": "趋势分析暂时不可用"
        }


@tool
def recommend_next_meal(current_nutrition: Dict[str, Any], recent_history: Dict[str, Any]) -> Dict[str, Any]:
    """
    基于当前餐和历史数据推荐下一餐。
    
    参数:
        current_nutrition: 当前餐的营养数据
        recent_history: 最近的历史数据(包含weekly_trend)
    
    返回:
        包含options(推荐列表)和overall_reason
    """
    # 读取提示词
    prompt_path = os.path.join(PROMPTS_DIR, "nextmeal_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    input_data = {
        "current_meal": current_nutrition,
        "weekly_trend": recent_history.get("weekly_trend", {})
    }
    
    try:
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(input_data, ensure_ascii=False, indent=2)}
            ],
            temperature=0.5
        )
        
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
        
        result = json.loads(json_str)
        return result
    
    except Exception as e:
        print(f"推荐生成错误: {str(e)}")
        return {
            "options": [
                {
                    "title": "均衡餐",
                    "recommended_dishes": ["清蒸鱼", "西兰花", "糙米饭"],
                    "reason": "推荐系统暂时不可用，提供默认建议"
                }
            ],
            "overall_reason": "建议选择清淡均衡的食物"
        }


if __name__ == "__main__":
    # 测试代码
    test_nutrition = {
        "calories": 720,
        "protein": 35,
        "fat": 22,
        "carbs": 60,
        "sodium": 1500
    }
    
    print("测试本餐评分:")
    score = score_current_meal_llm.invoke({"nutrition": test_nutrition})
    print(json.dumps(score, ensure_ascii=False, indent=2))
    
    print("\n测试趋势评分:")
    trend_score = score_weekly_adjusted.invoke({
        "current_meal": test_nutrition,
        "weekly_trend": {"protein_avg": 40, "sodium_avg": 2200}
    })
    print(json.dumps(trend_score, ensure_ascii=False, indent=2))
    
    print("\n测试下一餐推荐:")
    recommendation = recommend_next_meal.invoke({
        "current_nutrition": test_nutrition,
        "recent_history": {"weekly_trend": {"protein_avg": 35, "sodium_avg": 2100}}
    })
    print(json.dumps(recommendation, ensure_ascii=False, indent=2))
