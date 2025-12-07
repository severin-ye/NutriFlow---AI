"""
工具调用的输入输出Schema定义
用于LangChain工具的参数验证
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class VisionInput(BaseModel):
    """图像识别工具输入"""
    image_path: str = Field(..., description="图片文件路径")


class DishDetectionOutput(BaseModel):
    """菜品识别输出"""
    name: str = Field(..., description="菜品名称")
    category: str = Field(..., description="菜品类别")
    estimated_weight_g: float = Field(..., description="估计重量(克)")
    portion_level: str = Field(..., description="份量等级")
    reason: str = Field(..., description="估计理由")


class PortionCheckInput(BaseModel):
    """分量校验工具输入"""
    dishes: List[Dict[str, Any]] = Field(..., description="待校验的菜品列表")


class PortionCheckOutput(BaseModel):
    """分量校验输出"""
    dish_id: str = Field(..., description="菜品ID")
    is_reasonable: bool = Field(..., description="是否合理")
    reason: str = Field(..., description="判断理由")
    final_weight_g: float = Field(..., description="最终重量(克)")


class NutritionQuery(BaseModel):
    """营养查询工具输入"""
    dish_name: str = Field(..., description="菜品名称")


class NutritionQueryOutput(BaseModel):
    """营养查询输出"""
    calories: float = Field(..., description="热量(kcal/100g)")
    protein: float = Field(..., description="蛋白质(g/100g)")
    fat: float = Field(..., description="脂肪(g/100g)")
    carbs: float = Field(..., description="碳水化合物(g/100g)")
    sodium: float = Field(..., description="钠(mg/100g)")


class ComputeNutritionInput(BaseModel):
    """营养计算工具输入"""
    dishes: List[Dict[str, Any]] = Field(..., description="菜品列表(含重量和每100g营养)")


class ScoreInput(BaseModel):
    """评分工具输入"""
    nutrition: Dict[str, float] = Field(..., description="营养数据")


class ScoreOutput(BaseModel):
    """评分输出"""
    score: int = Field(..., ge=0, le=100, description="评分(0-100)")
    advice: str = Field(..., description="建议")


class TrendScoreInput(BaseModel):
    """趋势评分工具输入"""
    current_meal: Dict[str, Any] = Field(..., description="当前餐营养")
    weekly_trend: Dict[str, Any] = Field(..., description="一周趋势数据")


class RecommendationInput(BaseModel):
    """推荐工具输入"""
    current_nutrition: Dict[str, Any] = Field(..., description="当前餐营养")
    recent_history: Dict[str, Any] = Field(..., description="最近历史数据")


class SaveMealInput(BaseModel):
    """保存餐食工具输入"""
    meal: Dict[str, Any] = Field(..., description="完整的餐食数据")
