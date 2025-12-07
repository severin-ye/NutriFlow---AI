"""
智能餐型推断工具
结合固定规则（冷启动）和LLM智能分析（学习用户作息习惯）
"""
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from openai import OpenAI
from langchain.tools import tool

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
def infer_meal_type(timestamp: Optional[str] = None, recent_meals: Optional[list] = None) -> str:
    """
    智能推断餐型。
    
    策略：
    - 冷启动（历史数据<3天）：使用固定时间规则
    - 有历史数据：调用LLM分析用户作息习惯，智能推断
    
    参数:
        timestamp: ISO格式时间戳（可选，默认当前时间）
        recent_meals: 最近的用餐记录（可选）
    
    返回:
        餐型: 早餐/午餐/晚餐/夜宵/加餐等
    """
    # 解析时间
    if timestamp:
        dt = datetime.fromisoformat(timestamp)
    else:
        dt = datetime.now()
    
    current_hour = dt.hour
    current_minute = dt.minute
    today_str = dt.strftime("%Y-%m-%d")
    current_time_str = dt.strftime("%H:%M")
    
    # 统计历史数据天数
    if recent_meals and len(recent_meals) >= 3:
        # 有足够历史数据，使用LLM智能分析
        return _infer_with_llm(current_time_str, today_str, recent_meals)
    else:
        # 冷启动：使用固定规则
        return _infer_with_rules(current_hour, today_str, recent_meals)


def _infer_with_rules(hour: int, today: str, recent_meals: Optional[list]) -> str:
    """
    冷启动：使用固定时间规则判断餐型
    """
    # 基础时间规则
    if 5 <= hour < 10:
        base_type = "早餐"
    elif 10 <= hour < 14:
        base_type = "午餐"
    elif 14 <= hour < 17:
        base_type = "下午茶"
    elif 17 <= hour < 21:
        base_type = "晚餐"
    elif 21 <= hour < 24:
        base_type = "夜宵"
    else:  # 0-5点
        base_type = "夜宵"
    
    # 检查今天是否已经有相同餐型
    if recent_meals:
        today_meal_types = []
        for day_record in recent_meals:
            if day_record.get("date") == today:
                meals = day_record.get("meals", [])
                today_meal_types = [meal.get("meal_type") for meal in meals]
                break
        
        # 如果今天已经吃过该餐型，标记为加餐
        if base_type in today_meal_types:
            if hour < 10:
                return "早餐加餐"
            elif hour < 17:
                return "午后加餐"
            else:
                return "夜宵"
    
    return base_type


def _infer_with_llm(current_time: str, today: str, recent_meals: List[Dict]) -> str:
    """
    使用LLM分析用户作息习惯，智能推断餐型
    """
    # 构建用户作息分析提示词
    prompt = f"""你是一个智能餐型分析助手。请根据用户的历史用餐记录，分析其作息习惯，并判断当前时间应该是什么餐型。

**当前信息：**
- 当前时间：{today} {current_time}
- 今天日期：{today}

**用户最近的用餐记录：**
{json.dumps(recent_meals, ensure_ascii=False, indent=2)}

**分析要求：**
1. 观察用户的用餐时间规律（例如：每天只吃2顿？通常几点吃早餐/午餐/晚餐？）
2. 识别用户的个性化作息（有人早餐在11点，有人晚餐在20点）
3. 判断今天是否已经吃过某些餐型
4. 如果当前时间与用户历史规律匹配某个餐型，返回该餐型
5. 如果是加餐时间（两餐之间），返回"加餐"或"下午茶"

**可选餐型：**
- 早餐
- 午餐
- 晚餐
- 夜宵
- 加餐
- 下午茶
- 早午餐（如果用户习惯10-12点吃第一餐）

**输出格式（只输出餐型名称，不要其他解释）：**
餐型名称

**示例：**
如果用户历史记录显示：
- 通常14:00吃第一餐
- 通常20:00吃第二餐
- 当前时间是14:30
→ 输出：午餐

如果用户已经在12:00吃过午餐，当前时间16:00
→ 输出：下午茶
"""
    
    try:
        # 调用 Qwen-Plus 进行推断
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的作息分析专家，能够根据用户的历史数据准确判断餐型。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # 较低温度确保稳定输出
        )
        
        content = response.choices[0].message.content
        
        if not content:
            raise ValueError("模型返回内容为空")
        
        # 提取餐型（去除多余空格和换行）
        meal_type = content.strip()
        
        # 验证餐型是否合法
        valid_types = ["早餐", "午餐", "晚餐", "夜宵", "加餐", "下午茶", "早午餐", 
                      "早餐加餐", "午后加餐", "晚间加餐"]
        
        if meal_type in valid_types:
            print(f"✅ LLM智能推断: {current_time} -> {meal_type}")
            return meal_type
        else:
            # 如果返回的不是标准餐型，尝试从文本中提取
            for vtype in valid_types:
                if vtype in meal_type:
                    print(f"✅ LLM智能推断: {current_time} -> {vtype} (从'{meal_type}'提取)")
                    return vtype
            
            # 都失败了，fallback到规则推断
            print(f"⚠️  LLM返回非标准餐型'{meal_type}'，使用规则推断")
            hour = int(current_time.split(":")[0])
            return _infer_with_rules(hour, today, recent_meals)
    
    except Exception as e:
        print(f"⚠️  LLM推断失败: {str(e)}，使用规则推断")
        hour = int(current_time.split(":")[0])
        return _infer_with_rules(hour, today, recent_meals)


def get_meal_type_from_time(hour: int) -> str:
    """
    纯粹基于小时数判断餐型（简化版本，向后兼容）
    """
    if 5 <= hour < 10:
        return "早餐"
    elif 10 <= hour < 14:
        return "午餐"
    elif 14 <= hour < 17:
        return "下午茶"
    elif 17 <= hour < 21:
        return "晚餐"
    else:
        return "夜宵"


# 测试代码
if __name__ == "__main__":
    print("="*70)
    print("测试餐型推断功能")
    print("="*70)
    
    print("\n【场景1】冷启动 - 无历史数据，使用固定规则")
    print("-"*70)
    test_times = [
        ("2025-12-08T07:30:00", "早上7:30"),
        ("2025-12-08T12:00:00", "中午12:00"),
        ("2025-12-08T15:00:00", "下午3:00"),
        ("2025-12-08T18:30:00", "晚上6:30"),
        ("2025-12-08T22:00:00", "晚上10:00"),
    ]
    
    for timestamp, desc in test_times:
        result = infer_meal_type.invoke({
            "timestamp": timestamp,
            "recent_meals": None
        })
        print(f"  {desc} -> {result}")
    
    print("\n【场景2】有历史数据 - 今天已吃过同类餐型")
    print("-"*70)
    mock_history_1 = [
        {
            "date": "2025-12-08",
            "meals": [
                {"meal_type": "早餐", "timestamp": "2025-12-08T07:30:00"},
                {"meal_type": "午餐", "timestamp": "2025-12-08T12:00:00"}
            ]
        }
    ]
    
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T13:00:00",
        "recent_meals": mock_history_1
    })
    print(f"  下午1:00 (今天已吃过午餐) -> {result}")
    
    print("\n【场景3】LLM智能分析 - 用户每天只吃2顿（14:00 和 20:00）")
    print("-"*70)
    # 模拟一个每天只吃2顿的用户（下午2点和晚上8点）
    mock_history_2days = [
        {
            "date": "2025-12-06",
            "meals": [
                {"meal_type": "午餐", "timestamp": "2025-12-06T14:00:00"},
                {"meal_type": "晚餐", "timestamp": "2025-12-06T20:00:00"}
            ]
        },
        {
            "date": "2025-12-07",
            "meals": [
                {"meal_type": "午餐", "timestamp": "2025-12-07T14:30:00"},
                {"meal_type": "晚餐", "timestamp": "2025-12-07T20:15:00"}
            ]
        },
        {
            "date": "2025-12-08",
            "meals": []
        }
    ]
    
    # 测试当前时间14:20
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T14:20:00",
        "recent_meals": mock_history_2days
    })
    print(f"  当前14:20 (用户习惯14:00吃第一餐) -> {result}")
    
    # 测试当前时间20:00
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T20:00:00",
        "recent_meals": mock_history_2days
    })
    print(f"  当前20:00 (用户习惯20:00吃第二餐) -> {result}")
    
    print("\n【场景4】LLM智能分析 - 用户习惯11点早午餐，19点晚餐")
    print("-"*70)
    mock_history_brunch = [
        {
            "date": "2025-12-05",
            "meals": [
                {"meal_type": "早午餐", "timestamp": "2025-12-05T11:00:00"},
                {"meal_type": "晚餐", "timestamp": "2025-12-05T19:00:00"}
            ]
        },
        {
            "date": "2025-12-06",
            "meals": [
                {"meal_type": "早午餐", "timestamp": "2025-12-06T11:30:00"},
                {"meal_type": "晚餐", "timestamp": "2025-12-06T19:30:00"}
            ]
        },
        {
            "date": "2025-12-07",
            "meals": [
                {"meal_type": "早午餐", "timestamp": "2025-12-07T10:45:00"},
                {"meal_type": "晚餐", "timestamp": "2025-12-07T19:00:00"}
            ]
        },
        {
            "date": "2025-12-08",
            "meals": []
        }
    ]
    
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T11:15:00",
        "recent_meals": mock_history_brunch
    })
    print(f"  当前11:15 (用户习惯11点早午餐) -> {result}")
    
    print("\n" + "="*70)
