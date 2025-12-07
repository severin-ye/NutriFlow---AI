"""
主Agent文件 - 营养分析智能体
使用LangChain 1.0 create_agent构建
"""
import os
import sys
from datetime import datetime
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import AGENT_SYSTEM_PROMPT, DASHSCOPE_API_KEY
from tools.vision_tools import detect_dishes_and_portions
from tools.portion_tools import check_and_refine_portions
from tools.nutrition_tools import query_nutrition_per_100g
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
        # 初始化模型
        self.model = ChatTongyi(
            model="qwen-plus",
            dashscope_api_key=DASHSCOPE_API_KEY
        )
        
        # 初始化工具列表
        self.tools = [
            detect_dishes_and_portions,
            check_and_refine_portions,
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
        
        # 创建Agent提示词模板
        template = """你是一个智能营养分析助手。

你拥有以下工具：
{tools}

工具名称：{tool_names}

请按照以下格式回答用户问题：

Question: 用户的输入问题
Thought: 你应该思考该做什么
Action: 要使用的工具，必须是 [{tool_names}] 中的一个
Action Input: 工具的输入参数
Observation: 工具的输出结果
... (这个 Thought/Action/Action Input/Observation 可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 给用户的最终回答

当处理餐盘图片时，请按以下流程：
1. 使用 detect_dishes_and_portions 识别菜品
2. 使用 check_and_refine_portions 验证分量
3. 对每道菜使用 query_nutrition_per_100g 查询营养
4. 使用 compute_meal_nutrition 计算总营养
5. 使用 load_recent_meals 加载历史数据
6. 使用 score_current_meal_llm 评分
7. 使用 score_weekly_adjusted 趋势评分
8. 使用 recommend_next_meal 生成推荐
9. 使用 save_meal 保存数据

开始！

Question: {input}
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
        )
        
        # 创建Agent
        self.agent = create_react_agent(
            llm=self.model,
            tools=self.tools,
            prompt=prompt
        )
        
        # 创建Agent执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=15
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
            result = self.agent_executor.invoke({"input": query})
            return result
        except Exception as e:
            print(f"Agent执行错误: {str(e)}")
            return {"error": str(e)}
    
    def query_history(self, days: int = 7) -> dict:
        """查询历史数据"""
        query = f"请帮我查询最近{days}天的饮食记录和营养趋势。"
        
        try:
            result = self.agent_executor.invoke({"input": query})
            return result
        except Exception as e:
            print(f"查询历史错误: {str(e)}")
            return {"error": str(e)}
    
    def get_recommendation(self) -> dict:
        """获取下一餐推荐"""
        query = "根据我最近的饮食情况，给我下一餐的推荐。"
        
        try:
            result = self.agent_executor.invoke({"input": query})
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
