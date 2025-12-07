"""
主Agent文件 - 营养分析智能体
使用LangChain 1.0 create_agent构建
"""
import os
import sys
from datetime import datetime
from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import AGENT_SYSTEM_PROMPT, DASHSCOPE_API_KEY
from tools.vision_tools import detect_dishes_and_portions
from tools.portion_tools import check_and_refine_portions
from tools.nutrition_tools import query_nutrition_per_100g, add_nutrition_to_dishes
from tools.compute_tools import compute_meal_nutrition, score_current_meal
from tools.db_tools import load_recent_meals, save_meal, get_daily_summary
from tools.recommendation_tools import (
    score_current_meal_llm,
    score_weekly_adjusted,
    recommend_next_meal
)


class NutritionAgent:
    """营养分析Agent类"""
    
    def __init__(self):
        """初始化Agent"""
        # 检查API Key是否配置
        if not DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY未配置，请在.env文件中设置")
        
        # 初始化模型 - ChatTongyi会自动从环境变量读取DASHSCOPE_API_KEY
        self.model = ChatTongyi()  # type: ignore
        
        # 初始化工具列表
        self.tools = [
            detect_dishes_and_portions,
            check_and_refine_portions,
            add_nutrition_to_dishes,  # 🆕 批量添加营养数据
            query_nutrition_per_100g,
            compute_meal_nutrition,
            score_current_meal,
            load_recent_meals,
            save_meal,
            get_daily_summary,
            score_current_meal_llm,
            score_weekly_adjusted,
            recommend_next_meal
        ]
        
        # 使用LangGraph创建Agent (LangChain 1.0推荐方式)
        self.agent_executor = create_react_agent(
            model=self.model,
            tools=self.tools
        )
    
    def analyze_meal(self, image_path: str, meal_type: str = "午餐") -> dict:
        """
        分析餐盘图片的完整流程
        
        参数:
            image_path: 图片路径
            meal_type: 餐型(早餐/午餐/晚餐/加餐)
        
        返回:
            分析结果字典
        """
        query = f"""
请分析这张餐盘图片: {image_path}
这是一份{meal_type}。

请完成以下任务：
1. 识别所有菜品并估算分量
2. 计算营养成分
3. 给出健康评分和建议
4. 基于历史数据给出趋势分析
5. 推荐下一餐食物
6. 保存数据到数据库

请逐步执行并给我完整的分析报告。
"""
        
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            return result
        except Exception as e:
            print(f"Agent执行错误: {str(e)}")
            return {"error": str(e)}
    
    def query_history(self, days: int = 7) -> dict:
        """查询历史数据"""
        query = f"请帮我查询最近{days}天的饮食记录和营养趋势。"
        
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            return result
        except Exception as e:
            print(f"查询历史错误: {str(e)}")
            return {"error": str(e)}
    
    def get_recommendation(self) -> dict:
        """获取下一餐推荐"""
        query = "根据我最近的饮食情况，给我下一餐的推荐。"
        
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            return result
        except Exception as e:
            print(f"推荐生成错误: {str(e)}")
            return {"error": str(e)}


def main():
    """主函数 - CLI测试界面"""
    print("=" * 60)
    print("🍽️  智能营养分析系统")
    print("=" * 60)
    print()
    
    # 初始化Agent
    print("正在初始化Agent...")
    agent = NutritionAgent()
    print("✅ Agent初始化完成！")
    print()
    
    while True:
        print("\n请选择功能：")
        print("1. 分析餐盘图片")
        print("2. 查询历史记录")
        print("3. 获取下一餐推荐")
        print("4. 退出")
        print()
        
        choice = input("请输入选项(1-4): ").strip()
        
        if choice == "1":
            image_path = input("请输入图片路径: ").strip()
            if not os.path.exists(image_path):
                print("❌ 图片文件不存在！")
                continue
            
            meal_type = input("请输入餐型(早餐/午餐/晚餐/加餐，默认午餐): ").strip()
            if not meal_type:
                meal_type = "午餐"
            
            print("\n🔄 开始分析...")
            result = agent.analyze_meal(image_path, meal_type)
            print("\n" + "=" * 60)
            print("📊 分析结果：")
            print("=" * 60)
            print(result.get("output", result))
            
        elif choice == "2":
            days = input("查询最近几天(默认7天): ").strip()
            days = int(days) if days.isdigit() else 7
            
            print("\n🔄 查询中...")
            result = agent.query_history(days)
            print("\n" + "=" * 60)
            print("📈 历史记录：")
            print("=" * 60)
            print(result.get("output", result))
            
        elif choice == "3":
            print("\n🔄 生成推荐中...")
            result = agent.get_recommendation()
            print("\n" + "=" * 60)
            print("💡 推荐内容：")
            print("=" * 60)
            print(result.get("output", result))
            
        elif choice == "4":
            print("\n👋 再见！")
            break
        
        else:
            print("❌ 无效选项，请重新选择！")


if __name__ == "__main__":
    main()
