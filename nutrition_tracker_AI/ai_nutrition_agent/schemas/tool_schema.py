"""
Input/Output Schema definitions for tool invocation
Used for parameter validation in LangChain tools
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class VisionInput(BaseModel):
    """Image recognition tool input"""
    image_path: str = Field(..., description="Image file path")


class DishDetectionOutput(BaseModel):
    """Dish detection output"""
    name: str = Field(..., description="Dish name")
    category: str = Field(..., description="Dish category")
    estimated_weight_g: float = Field(..., description="Estimated weight (grams)")
    portion_level: str = Field(..., description="Portion level")
    reason: str = Field(..., description="Estimation reason")


class PortionCheckInput(BaseModel):
    """Portion verification tool input"""
    dishes: List[Dict[str, Any]] = Field(..., description="List of dishes to verify")


class PortionCheckOutput(BaseModel):
    """Portion verification output"""
    dish_id: str = Field(..., description="Dish ID")
    is_reasonable: bool = Field(..., description="Whether it is reasonable")
    reason: str = Field(..., description="Judgment reason")
    final_weight_g: float = Field(..., description="Final weight (grams)")


class NutritionQuery(BaseModel):
    """Nutrition query tool input"""
    dish_name: str = Field(..., description="Dish name")


class NutritionQueryOutput(BaseModel):
    """Nutrition query output"""
    calories: float = Field(..., description="Calories (kcal/100g)")
    protein: float = Field(..., description="Protein (g/100g)")
    fat: float = Field(..., description="Fat (g/100g)")
    carbs: float = Field(..., description="Carbohydrates (g/100g)")
    sodium: float = Field(..., description="Sodium (mg/100g)")


class ComputeNutritionInput(BaseModel):
    """Nutrition calculation tool input"""
    dishes: List[Dict[str, Any]] = Field(..., description="Dishes list (with weight and nutrition per 100g)")


class ScoreInput(BaseModel):
    """Scoring tool input"""
    nutrition: Dict[str, float] = Field(..., description="Nutrition data")


class ScoreOutput(BaseModel):
    """Scoring output"""
    score: int = Field(..., ge=0, le=100, description="Score (0-100)")
    advice: str = Field(..., description="Advice")


class TrendScoreInput(BaseModel):
    """Trend scoring tool input"""
    current_meal: Dict[str, Any] = Field(..., description="Current meal nutrition")
    weekly_trend: Dict[str, Any] = Field(..., description="Weekly trend data")


class RecommendationInput(BaseModel):
    """Recommendation tool input"""
    current_nutrition: Dict[str, Any] = Field(..., description="Current meal nutrition")
    recent_history: Dict[str, Any] = Field(..., description="Recent history data")


class SaveMealInput(BaseModel):
    """Save meal tool input"""
    meal: Dict[str, Any] = Field(..., description="Complete meal data")
