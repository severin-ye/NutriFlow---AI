"""
Schemas包初始化文件
"""
from .meal_schema import (
    Nutrition,
    PortionEstimation,
    Dish,
    MealScores,
    MealAdvice,
    NextMealOption,
    NextMealRecommendation,
    Meal,
    DailySummary,
    Day,
    NutritionDatabase
)

from .tool_schema import (
    VisionInput,
    DishDetectionOutput,
    PortionCheckInput,
    PortionCheckOutput,
    NutritionQuery,
    NutritionQueryOutput,
    ComputeNutritionInput,
    ScoreInput,
    ScoreOutput,
    TrendScoreInput,
    RecommendationInput,
    SaveMealInput
)

__all__ = [
    "Nutrition",
    "PortionEstimation",
    "Dish",
    "MealScores",
    "MealAdvice",
    "NextMealOption",
    "NextMealRecommendation",
    "Meal",
    "DailySummary",
    "Day",
    "NutritionDatabase",
    "VisionInput",
    "DishDetectionOutput",
    "PortionCheckInput",
    "PortionCheckOutput",
    "NutritionQuery",
    "NutritionQueryOutput",
    "ComputeNutritionInput",
    "ScoreInput",
    "ScoreOutput",
    "TrendScoreInput",
    "RecommendationInput",
    "SaveMealInput",
]
