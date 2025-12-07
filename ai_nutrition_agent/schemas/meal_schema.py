"""
营养分析系统的数据模型定义
使用 Pydantic 确保数据结构的一致性和类型安全
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Nutrition(BaseModel):
    """营养成分数据模型"""
    calories: float = Field(..., description="热量(kcal)")
    protein: float = Field(..., description="蛋白质(g)")
    fat: float = Field(..., description="脂肪(g)")
    carbs: float = Field(..., description="碳水化合物(g)")
    sodium: float = Field(..., description="钠(mg)")


class PortionEstimation(BaseModel):
    """分量估计数据模型"""
    estimated_weight_g: float = Field(..., description="估计重量(克)")
    portion_level: str = Field(..., description="份量等级: small/medium/large")
    final_weight_g: float = Field(..., description="最终确认重量(克)")
    is_reasonable: bool = Field(..., description="重量估计是否合理")
    reason: str = Field(..., description="估计理由或修正原因")


class Dish(BaseModel):
    """单道菜品数据模型"""
    dish_id: str = Field(..., description="菜品ID")
    name: str = Field(..., description="菜品名称")
    category: str = Field(..., description="菜品类别: 主食/荤菜/蔬菜/汤类/小吃/甜品")
    portion_estimation: PortionEstimation = Field(..., description="分量估计信息")
    nutrition_per_100g: Nutrition = Field(..., description="每100g营养成分")
    nutrition_total: Nutrition = Field(..., description="该菜品总营养成分")


class MealScores(BaseModel):
    """餐食评分数据模型"""
    current_meal_score: int = Field(..., ge=0, le=100, description="本餐评分(0-100)")
    week_adjusted_score: int = Field(..., ge=0, le=100, description="趋势修正后评分(0-100)")


class MealAdvice(BaseModel):
    """餐食建议数据模型"""
    current_meal_advice: str = Field(..., description="本餐营养建议")
    week_adjusted_advice: str = Field(..., description="结合一周趋势的建议")


class NextMealOption(BaseModel):
    """下一餐推荐选项"""
    title: str = Field(..., description="推荐标题")
    recommended_dishes: List[str] = Field(..., description="推荐菜品列表")
    reason: str = Field(..., description="推荐理由")


class NextMealRecommendation(BaseModel):
    """下一餐推荐数据模型"""
    options: List[NextMealOption] = Field(..., description="推荐选项列表")
    overall_reason: str = Field(..., description="总体推荐理由")


class Meal(BaseModel):
    """完整餐食记录数据模型"""
    meal_id: str = Field(..., description="餐食ID")
    timestamp: str = Field(..., description="记录时间(ISO格式)")
    meal_type: str = Field(..., description="餐型: 早餐/午餐/晚餐/加餐")
    dishes: List[Dish] = Field(..., description="菜品列表")
    nutrition_total: Nutrition = Field(..., description="整餐营养总计")
    scores: MealScores = Field(..., description="评分信息")
    advice: MealAdvice = Field(..., description="建议信息")
    next_meal_recommendation: NextMealRecommendation = Field(..., description="下一餐推荐")


class DailySummary(BaseModel):
    """每日营养汇总"""
    total_calories: float = Field(default=0, description="日总热量")
    total_protein: float = Field(default=0, description="日总蛋白质")
    total_fat: float = Field(default=0, description="日总脂肪")
    total_carbs: float = Field(default=0, description="日总碳水化合物")
    total_sodium: float = Field(default=0, description="日总钠")
    daily_score: float = Field(default=0, description="日总评分")


class Day(BaseModel):
    """单日记录数据模型"""
    date: str = Field(..., description="日期(YYYY-MM-DD)")
    daily_summary: DailySummary = Field(..., description="日营养汇总")
    meals: List[Meal] = Field(default_factory=list, description="餐食列表")


class NutritionDatabase(BaseModel):
    """整个数据库的数据模型"""
    user_id: str = Field(..., description="用户ID")
    days: List[Day] = Field(default_factory=list, description="日期列表")
