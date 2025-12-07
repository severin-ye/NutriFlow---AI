"""
DatabaseTools - JSON数据库读写工具
"""
import json
import os
from datetime import datetime, timedelta
from langchain.tools import tool
from typing import Dict, Any, List

from config.settings import DB_PATH, RECENT_DAYS


def _load_json() -> Dict[str, Any]:
    """加载JSON数据库"""
    if not os.path.exists(DB_PATH):
        # 如果文件不存在，创建初始结构
        initial_data = {
            "user_id": "user001",
            "days": []
        }
        _save_json(initial_data)
        return initial_data
    
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载数据库错误: {str(e)}")
        return {"user_id": "user001", "days": []}


def _save_json(data: Dict[str, Any]) -> None:
    """保存JSON数据库"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存数据库错误: {str(e)}")


@tool
def load_recent_meals(days: int = RECENT_DAYS) -> Dict[str, Any]:
    """
    读取最近N天的餐食记录。
    
    参数:
        days: 查询最近几天的记录，默认7天
    
    返回:
        包含最近N天的餐食数据和营养趋势统计
    """
    db = _load_json()
    
    # 计算日期范围
    today = datetime.now().date()
    start_date = today - timedelta(days=days-1)
    
    # 过滤最近N天的数据
    recent_days = []
    for day in db.get("days", []):
        day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
        if start_date <= day_date <= today:
            recent_days.append(day)
    
    # 计算趋势统计
    total_meals = 0
    total_nutrition = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "sodium": 0
    }
    
    for day in recent_days:
        for meal in day.get("meals", []):
            total_meals += 1
            meal_nutrition = meal.get("nutrition_total", {})
            for key in total_nutrition:
                total_nutrition[key] += meal_nutrition.get(key, 0)
    
    # 计算平均值
    avg_nutrition = {}
    if total_meals > 0:
        for key in total_nutrition:
            avg_nutrition[f"{key}_avg"] = round(total_nutrition[key] / total_meals, 2)
    
    return {
        "recent_days": recent_days,
        "total_meals": total_meals,
        "weekly_trend": avg_nutrition,
        "days_included": days
    }


@tool
def save_meal(meal_data: Dict[str, Any]) -> str:
    """
    将餐食记录保存到JSON数据库。
    
    参数:
        meal_data: 完整的餐食数据，包含所有必要字段
    
    返回:
        保存状态消息
    """
    try:
        db = _load_json()
        
        # 获取当前日期
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 查找今天的记录
        day_index = None
        for i, day in enumerate(db.get("days", [])):
            if day["date"] == today:
                day_index = i
                break
        
        # 如果今天的记录不存在，创建新的
        if day_index is None:
            new_day = {
                "date": today,
                "daily_summary": {
                    "total_calories": 0,
                    "total_protein": 0,
                    "total_fat": 0,
                    "total_carbs": 0,
                    "total_sodium": 0,
                    "daily_score": 0
                },
                "meals": []
            }
            db["days"].append(new_day)
            day_index = len(db["days"]) - 1
        
        # 添加meal_id和timestamp(如果没有)
        if "meal_id" not in meal_data:
            meal_count = len(db["days"][day_index]["meals"])
            meal_data["meal_id"] = f"meal_{today}_{meal_count+1}"
        
        if "timestamp" not in meal_data:
            meal_data["timestamp"] = datetime.now().isoformat()
        
        # 添加餐食到今天的记录
        db["days"][day_index]["meals"].append(meal_data)
        
        # 更新每日汇总
        daily_summary = db["days"][day_index]["daily_summary"]
        meal_nutrition = meal_data.get("nutrition_total", {})
        
        daily_summary["total_calories"] += meal_nutrition.get("calories", 0)
        daily_summary["total_protein"] += meal_nutrition.get("protein", 0)
        daily_summary["total_fat"] += meal_nutrition.get("fat", 0)
        daily_summary["total_carbs"] += meal_nutrition.get("carbs", 0)
        daily_summary["total_sodium"] += meal_nutrition.get("sodium", 0)
        
        # 更新每日评分(取所有餐的平均分)
        all_scores = []
        for meal in db["days"][day_index]["meals"]:
            if "scores" in meal and "current_meal_score" in meal["scores"]:
                all_scores.append(meal["scores"]["current_meal_score"])
        
        if all_scores:
            daily_summary["daily_score"] = round(sum(all_scores) / len(all_scores), 2)
        
        # 四舍五入营养值
        for key in ["total_calories", "total_protein", "total_fat", "total_carbs", "total_sodium"]:
            daily_summary[key] = round(daily_summary[key], 2)
        
        # 保存数据库
        _save_json(db)
        
        return f"成功保存餐食记录到 {today}，餐食ID: {meal_data['meal_id']}"
    
    except Exception as e:
        error_msg = f"保存餐食失败: {str(e)}"
        print(error_msg)
        return error_msg


@tool
def get_daily_summary(date: str = None) -> Dict[str, Any]:
    """
    获取指定日期的营养汇总。
    
    参数:
        date: 日期(YYYY-MM-DD格式)，默认为今天
    
    返回:
        该日期的营养汇总数据
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    db = _load_json()
    
    for day in db.get("days", []):
        if day["date"] == date:
            return day["daily_summary"]
    
    # 如果没找到，返回空汇总
    return {
        "total_calories": 0,
        "total_protein": 0,
        "total_fat": 0,
        "total_carbs": 0,
        "total_sodium": 0,
        "daily_score": 0,
        "note": f"未找到 {date} 的数据"
    }


if __name__ == "__main__":
    # 测试代码
    print("测试加载最近餐食:")
    recent = load_recent_meals(7)
    print(json.dumps(recent, ensure_ascii=False, indent=2))
    
    print("\n测试获取每日汇总:")
    summary = get_daily_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
