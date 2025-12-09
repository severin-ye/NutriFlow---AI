"""
Data model definitions for Nutrition Analysis System
Use Pydantic to ensure data structure consistency and type safety
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Nutrition(BaseModel):
    """Nutrition component data model"""
    calories: float = Field(..., description="Calories (kcal)")
    protein: float = Field(..., description="Protein (g)")
    fat: float = Field(..., description="Fat (g)")
    carbs: float = Field(..., description="Carbohydrates (g)")
    sodium: float = Field(..., description="Sodium (mg)")


class PortionEstimation(BaseModel):
    """Portion estimation data model"""
    estimated_weight_g: float = Field(..., description="Estimated weight (grams)")
    portion_level: str = Field(..., description="Portion level: small/medium/large")
    final_weight_g: float = Field(..., description="Final confirmed weight (grams)")
    is_reasonable: bool = Field(..., description="Whether weight estimation is reasonable")
    reason: str = Field(..., description="Estimation reason or correction reason")


class Dish(BaseModel):
    """Single dish data model"""
    dish_id: str = Field(..., description="Dish ID")
    name: str = Field(..., description="Dish name")
    category: str = Field(..., description="Dish category: Staple/Meat/Vegetable/Soup/Snack/Dessert")
    portion_estimation: PortionEstimation = Field(..., description="Portion estimation information")
    nutrition_per_100g: Nutrition = Field(..., description="Nutrition per 100g")
    nutrition_total: Nutrition = Field(..., description="Total nutrition for this dish")


class MealScores(BaseModel):
    """Meal scoring data model"""
    current_meal_score: int = Field(..., ge=0, le=100, description="Current meal score (0-100)")
    week_adjusted_score: int = Field(..., ge=0, le=100, description="Trend-adjusted score (0-100)")


class MealAdvice(BaseModel):
    """Meal advice data model"""
    current_meal_advice: str = Field(..., description="Current meal nutrition advice")
    week_adjusted_advice: str = Field(..., description="Advice combined with weekly trend")


class NextMealOption(BaseModel):
    """Next meal recommendation option"""
    title: str = Field(..., description="Recommendation title")
    recommended_dishes: List[str] = Field(..., description="Recommended dishes list")
    reason: str = Field(..., description="Recommendation reason")


class NextMealRecommendation(BaseModel):
    """Next meal recommendation data model"""
    options: List[NextMealOption] = Field(..., description="Recommendation options list")
    overall_reason: str = Field(..., description="Overall recommendation reason")


class Meal(BaseModel):
    """Complete meal record data model"""
    meal_id: str = Field(..., description="Meal ID")
    timestamp: str = Field(..., description="Record time (ISO format)")
    meal_type: str = Field(..., description="Meal type: Breakfast/Lunch/Dinner/Snack")
    dishes: List[Dish] = Field(..., description="Dishes list")
    nutrition_total: Nutrition = Field(..., description="Total meal nutrition")
    scores: MealScores = Field(..., description="Scoring information")
    advice: MealAdvice = Field(..., description="Advice information")
    next_meal_recommendation: NextMealRecommendation = Field(..., description="Next meal recommendation")


class DailySummary(BaseModel):
    """Daily nutrition summary"""
    total_calories: float = Field(default=0, description="Daily total calories")
    total_protein: float = Field(default=0, description="Daily total protein")
    total_fat: float = Field(default=0, description="Daily total fat")
    total_carbs: float = Field(default=0, description="Daily total carbohydrates")
    total_sodium: float = Field(default=0, description="Daily total sodium")
    daily_score: float = Field(default=0, description="Daily total score")


class Day(BaseModel):
    """Single day record data model"""
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    daily_summary: DailySummary = Field(..., description="Daily nutrition summary")
    meals: List[Meal] = Field(default_factory=list, description="Meals list")


class NutritionDatabase(BaseModel):
    """Entire database data model"""
    user_id: str = Field(..., description="User ID")
    days: List[Day] = Field(default_factory=list, description="Days list")
