"""
Intelligent Meal Type Inference Tool
Combines fixed rules (cold start) and LLM intelligent analysis (learn user schedule habits)
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


# Initialize OpenAI client (compatible with Qwen API)
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL
)


@tool
def infer_meal_type(timestamp: Optional[str] = None, recent_meals: Optional[list] = None) -> str:
    """
    Intelligently infer meal type.
    
    Strategy:
    - Cold start (historical data < 3 days): Use fixed time rules
    - With historical data: Call LLM to analyze user schedule habits to intelligently infer
    
    Args:
        timestamp: ISO format timestamp (optional, defaults to current time)
        recent_meals: Recent meal records (optional)
    
    Returns:
        Meal type: Breakfast/Lunch/Dinner/Midnight Snack/Snack, etc.
    """
    # Parse time
    if timestamp:
        dt = datetime.fromisoformat(timestamp)
    else:
        dt = datetime.now()
    
    current_hour = dt.hour
    current_minute = dt.minute
    today_str = dt.strftime("%Y-%m-%d")
    current_time_str = dt.strftime("%H:%M")
    
    # Count number of days with historical data
    if recent_meals and len(recent_meals) >= 3:
        # Enough history → use LLM analysis
        return _infer_with_llm(current_time_str, today_str, recent_meals)
    else:
        # Cold start → use fixed rules
        return _infer_with_rules(current_hour, today_str, recent_meals)


def _infer_with_rules(hour: int, today: str, recent_meals: Optional[list]) -> str:
    """
    Cold start: Determine meal type using fixed time rules
    """
    # Basic time rules
    if 5 <= hour < 10:
        base_type = "Breakfast"
    elif 10 <= hour < 14:
        base_type = "Lunch"
    elif 14 <= hour < 17:
        base_type = "Afternoon Tea"
    elif 17 <= hour < 21:
        base_type = "Dinner"
    elif 21 <= hour < 24:
        base_type = "Midnight Snack"
    else:  # 0-5 AM
        base_type = "Midnight Snack"
    
    # Check if user already had same meal type today
    if recent_meals:
        today_meal_types = []
        for day_record in recent_meals:
            if day_record.get("date") == today:
                meals = day_record.get("meals", [])
                today_meal_types = [meal.get("meal_type") for meal in meals]
                break
        
        # If already eaten → return snack-type variation
        if base_type in today_meal_types:
            if hour < 10:
                return "Morning Snack"
            elif hour < 17:
                return "Afternoon Snack"
            else:
                return "Midnight Snack"
    
    return base_type


def _infer_with_llm(current_time: str, today: str, recent_meals: List[Dict]) -> str:
    """
    Use LLM to analyze user eating habits and intelligently infer meal type
    """
    # Prompt for analyzing meal habits
    prompt = f"""
You are an intelligent meal-type analysis assistant. Based on the user's historical meal records, analyze their daily eating habits and determine what meal type it should be at the current time.

**Current Information:**
- Current time: {today} {current_time}
- Today's date: {today}

**User’s recent meal records:**
{json.dumps(recent_meals, ensure_ascii=False, indent=2)}

**Analysis Requirements:**
1. Observe the user’s eating schedule (e.g., do they only eat two meals a day? What times do they usually eat?)
2. Identify personalized habits (some people eat breakfast at 11:00, others eat dinner at 20:00)
3. Determine whether certain meal types have already been eaten today
4. If the current time matches the user’s historical pattern for a specific meal type, return that meal type
5. If it is a snack time (between meals), return "Snack" or "Afternoon Tea"

**Possible meal types:**
- Breakfast
- Lunch
- Dinner
- Midnight Snack
- Snack
- Afternoon Tea
- Brunch (if the user usually eats their first meal between 10:00–12:00)
- Morning Snack
- Afternoon Snack
- Evening Snack

**Output Format (only output the meal type name, no explanation):**
Meal Type Name

**Examples:**
If the user's history shows:
- First meal at 14:00
- Second meal at 20:00
- Current time 14:30
→ Output: Lunch

If user ate lunch at 12:00 and current time is 16:00:
→ Output: Afternoon Tea
"""    
    try:
        # Call Qwen model
        response = client.chat.completions.create(
            model=QWEN_TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional daily-routine analysis expert who can accurately determine the meal type based on historical data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )
        
        content = response.choices[0].message.content
        
        if not content:
            raise ValueError("Model returned empty content")
        
        meal_type = content.strip()
        
        valid_types = [
            "Breakfast",
            "Lunch",
            "Dinner",
            "Midnight Snack",
            "Snack",
            "Afternoon Tea",
            "Brunch",
            "Morning Snack",
            "Afternoon Snack",
            "Evening Snack"
        ]

        # Exact match
        if meal_type in valid_types:
            print(f"✅ LLM Inference: {current_time} -> {meal_type}")
            return meal_type
        
        # Partial match
        for vtype in valid_types:
            if vtype in meal_type:
                print(f"✅ LLM Inference: {current_time} -> {vtype} (extracted from '{meal_type}')")
                return vtype
        
        # Fallback
        print(f"⚠️ LLM returned unknown meal type '{meal_type}', falling back to rule-based")
        hour = int(current_time.split(":")[0])
        return _infer_with_rules(hour, today, recent_meals)
    
    except Exception as e:
        print(f"⚠️ LLM inference failed: {str(e)}, falling back to rule-based")
        hour = int(current_time.split(":")[0])
        return _infer_with_rules(hour, today, recent_meals)


def get_meal_type_from_time(hour: int) -> str:
    """
    Rule-only meal type inference (simple)
    """
    if 5 <= hour < 10:
        return "Breakfast"
    elif 10 <= hour < 14:
        return "Lunch"
    elif 14 <= hour < 17:
        return "Afternoon Tea"
    elif 17 <= hour < 21:
        return "Dinner"
    else:
        return "Midnight Snack"


# Test code
if __name__ == "__main__":
    print("="*70)
    print("Testing Meal Type Inference")
    print("="*70)
    
    print("\n[Scenario 1] Cold Start - No history, use rule-based")
    print("-"*70)
    test_times = [
        ("2025-12-08T07:30:00", "7:30 AM"),
        ("2025-12-08T12:00:00", "12:00 PM"),
        ("2025-12-08T15:00:00", "3:00 PM"),
        ("2025-12-08T18:30:00", "6:30 PM"),
        ("2025-12-08T22:00:00", "10:00 PM"),
    ]
    
    for timestamp, desc in test_times:
        result = infer_meal_type.invoke({
            "timestamp": timestamp,
            "recent_meals": None
        })
        print(f"  {desc} -> {result}")
    
    print("\n[Scenario 2] With History - Already ate same meal today")
    print("-"*70)
    mock_history_1 = [
        {
            "date": "2025-12-08",
            "meals": [
                {"meal_type": "Breakfast", "timestamp": "2025-12-08T07:30:00"},
                {"meal_type": "Lunch", "timestamp": "2025-12-08T12:00:00"}
            ]
        }
    ]
    
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T13:00:00",
        "recent_meals": mock_history_1
    })
    print(f"  1:00 PM (already had Lunch today) -> {result}")
    
    print("\n[Scenario 3] LLM Analysis - User eats only 2 meals (14:00 & 20:00)")
    print("-"*70)
    
    mock_history_2days = [
        {
            "date": "2025-12-06",
            "meals": [
                {"meal_type": "Lunch", "timestamp": "2025-12-06T14:00:00"},
                {"meal_type": "Dinner", "timestamp": "2025-12-06T20:00:00"}
            ]
        },
        {
            "date": "2025-12-07",
            "meals": [
                {"meal_type": "Lunch", "timestamp": "2025-12-07T14:30:00"},
                {"meal_type": "Dinner", "timestamp": "2025-12-07T20:15:00"}
            ]
        },
        {
            "date": "2025-12-08",
            "meals": []
        }
    ]
    
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T14:20:00",
        "recent_meals": mock_history_2days
    })
    print(f"  14:20 (user usually eats first meal around 14:00) -> {result}")
    
    result = infer_meal_type.invoke({
        "timestamp": "2025-12-08T20:00:00",
        "recent_meals": mock_history_2days
    })
    print(f"  20:00 (user usually eats second meal at 20:00) -> {result}")
    
    print("\n[Scenario 4] LLM - User habit: Brunch at 11:00, dinner at 19:00")
    print("-"*70)
    
    mock_history_brunch = [
        {
            "date": "2025-12-05",
            "meals": [
                {"meal_type": "Brunch", "timestamp": "2025-12-05T11:00:00"},
                {"meal_type": "Dinner", "timestamp": "2025-12-05T19:00:00"}
            ]
        },
        {
            "date": "2025-12-06",
            "meals": [
                {"meal_type": "Brunch", "timestamp": "2025-12-06T11:30:00"},
                {"meal_type": "Dinner", "timestamp": "2025-12-06T19:30:00"}
            ]
        },
        {
            "date": "2025-12-07",
            "meals": [
                {"meal_type": "Brunch", "timestamp": "2025-12-07T10:45:00"},
                {"meal_type": "Dinner", "timestamp": "2025-12-07T19:00:00"}
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
    print(f"  11:15 (user usually eats brunch around 11) -> {result}")
    
    print("\n" + "="*70)
