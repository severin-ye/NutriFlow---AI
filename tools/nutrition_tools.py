"""
NutritionTool - 查询菜品营养数据(本地CSV数据库)
"""
import os
import pandas as pd
from langchain.tools import tool
from typing import Dict, Any
from difflib import get_close_matches

from config.settings import NUTRITION_DB_PATH


# 创建一个简单的营养数据库(如果CSV不存在)
def initialize_nutrition_db():
    """初始化营养数据库CSV文件"""
    if not os.path.exists(NUTRITION_DB_PATH):
        # 创建示例营养数据
        data = {
            "菜品名": [
                "白米饭", "糙米饭", "馒头", "面条",
                "宫保鸡丁", "红烧肉", "清蒸鱼", "鸡胸肉", "牛肉",
                "西兰花", "番茄", "白菜", "菠菜", "黄瓜",
                "鸡蛋", "豆腐", "牛奶",
                "紫菜蛋花汤", "番茄蛋汤", "冬瓜汤"
            ],
            "热量(kcal/100g)": [
                116, 112, 221, 138,
                195, 489, 104, 133, 250,
                34, 19, 17, 24, 15,
                147, 81, 54,
                15, 30, 11
            ],
            "蛋白质(g/100g)": [
                2.6, 2.6, 7.0, 4.5,
                18.5, 9.5, 17.8, 24.6, 26.1,
                4.3, 0.9, 1.5, 2.9, 0.8,
                13.3, 8.1, 3.0,
                1.5, 2.0, 0.5
            ],
            "脂肪(g/100g)": [
                0.3, 0.8, 1.0, 0.5,
                11.2, 48.0, 3.7, 5.0, 17.5,
                0.4, 0.2, 0.2, 0.3, 0.2,
                8.8, 3.7, 3.2,
                1.0, 2.0, 0.2
            ],
            "碳水化合物(g/100g)": [
                25.6, 23.3, 47.0, 29.9,
                7.8, 0.1, 0.0, 0.0, 0.3,
                6.6, 4.0, 3.2, 2.9, 2.9,
                2.8, 4.8, 4.9,
                1.5, 3.0, 2.0
            ],
            "钠(mg/100g)": [
                2, 2, 201, 142,
                850, 800, 120, 65, 60,
                24, 5, 73, 85, 4,
                131, 7, 42,
                350, 300, 100
            ]
        }
        
        df = pd.DataFrame(data)
        
        # 创建目录
        os.makedirs(os.path.dirname(NUTRITION_DB_PATH), exist_ok=True)
        
        # 保存CSV
        df.to_csv(NUTRITION_DB_PATH, index=False, encoding="utf-8-sig")
        print(f"营养数据库已创建: {NUTRITION_DB_PATH}")
        
        return df
    else:
        return pd.read_csv(NUTRITION_DB_PATH, encoding="utf-8-sig")


# 加载营养数据库
nutrition_db = initialize_nutrition_db()


@tool
def query_nutrition_per_100g(dish_name: str) -> Dict[str, float]:
    """
    查询菜品的每100g营养成分。使用模糊匹配查找最接近的菜品。
    
    参数:
        dish_name: 菜品名称
    
    返回:
        营养成分字典，包含: calories, protein, fat, carbs, sodium
    """
    global nutrition_db
    
    try:
        # 重新加载数据库(防止更新)
        nutrition_db = pd.read_csv(NUTRITION_DB_PATH, encoding="utf-8-sig")
        
        # 获取所有菜品名
        all_dishes = nutrition_db["菜品名"].tolist()
        
        # 精确匹配
        if dish_name in all_dishes:
            matched_dish = dish_name
        else:
            # 模糊匹配
            matches = get_close_matches(dish_name, all_dishes, n=1, cutoff=0.3)
            if matches:
                matched_dish = matches[0]
                print(f"模糊匹配: '{dish_name}' -> '{matched_dish}'")
            else:
                # 使用默认值
                print(f"未找到菜品 '{dish_name}'，使用默认营养值")
                return {
                    "calories": 100.0,
                    "protein": 5.0,
                    "fat": 3.0,
                    "carbs": 15.0,
                    "sodium": 200.0
                }
        
        # 查询营养数据
        row = nutrition_db[nutrition_db["菜品名"] == matched_dish].iloc[0]
        
        return {
            "calories": float(row["热量(kcal/100g)"]),
            "protein": float(row["蛋白质(g/100g)"]),
            "fat": float(row["脂肪(g/100g)"]),
            "carbs": float(row["碳水化合物(g/100g)"]),
            "sodium": float(row["钠(mg/100g)"])
        }
    
    except Exception as e:
        print(f"营养查询错误: {str(e)}")
        # 返回默认值
        return {
            "calories": 100.0,
            "protein": 5.0,
            "fat": 3.0,
            "carbs": 15.0,
            "sodium": 200.0
        }


if __name__ == "__main__":
    # 测试代码
    result = query_nutrition_per_100g.invoke({"dish_name": "宫保鸡丁"})
    print(result)
    
    result2 = query_nutrition_per_100g.invoke({"dish_name": "鸡丁"})  # 测试模糊匹配
    print(result2)
