"""
Main Agent file - Nutrition Analysis Agent
Built using LangChain 1.0 create_agent
"""
import os
import sys
from datetime import datetime
from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Add project root to path
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
    """Nutrition Analysis Agent class"""
    
    def __init__(self):
        """Initialize Agent"""
        # Check if API Key is configured
        if not DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY is not configured, please set it in .env file")
        
        # Initialize model - ChatTongyi will automatically read DASHSCOPE_API_KEY from environment variables
        self.model = ChatTongyi()  # type: ignore
        
        # Initialize tool list
        self.tools = [
            detect_dishes_and_portions,
            check_and_refine_portions,
            add_nutrition_to_dishes,  # 🆕 Batch add nutrition data
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
        
        # Create Agent using LangGraph (LangChain 1.0 recommended approach)
        self.agent_executor = create_react_agent(
            model=self.model,
            tools=self.tools
        )
    
    def analyze_meal(self, image_path: str, meal_type: str = "Lunch") -> dict:
        """
        Complete workflow for analyzing meal image
        
        Args:
            image_path: Image file path
            meal_type: Meal type (Breakfast/Lunch/Dinner/Snack)
        
        Returns:
            Analysis result dictionary
        """
        query = f"""
Please analyze this meal image: {image_path}
This is a {meal_type}.

Please complete the following tasks:
1. Identify all dishes and estimate portions
2. Calculate nutritional content
3. Provide health score and recommendations
4. Analyze trends based on historical data
5. Recommend next meal foods
6. Save data to database

Please execute step by step and provide me with a complete analysis report.
"""
        
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            print(result)
            return result
        except Exception as e:
            print(f"Agent execution error: {str(e)}")
            return {"error": str(e)}
    
    def query_history(self, days: int = 7) -> dict:
        """Query historical data"""
        query = f"Please help me query diet records and nutrition trends for the recent {days} days."
        
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            return result
        except Exception as e:
            print(f"History query error: {str(e)}")
            return {"error": str(e)}
    
    def get_recommendation(self) -> dict:
        """Get next meal recommendation"""
        query = "Based on my recent diet situation, give me recommendations for my next meal."
        
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            return result
        except Exception as e:
            print(f"Recommendation generation error: {str(e)}")
            return {"error": str(e)}


def main():
    """Main function - CLI test interface"""
    print("=" * 60)
    print("🍽️  Intelligent Nutrition Analysis System")
    print("=" * 60)
    print()
    
    # Initialize Agent
    print("Initializing Agent...")
    agent = NutritionAgent()
    print("✅ Agent initialization complete!")
    print()
    
    while True:
        print("\nPlease select a function:")
        print("1. Analyze meal image")
        print("2. Query history records")
        print("3. Get next meal recommendation")
        print("4. Exit")
        print()
        
        choice = input("Please enter option (1-4): ").strip()
        
        if choice == "1":
            image_path = input("Please enter image path: ").strip()
            if not os.path.exists(image_path):
                print("❌ Image file does not exist!")
                continue
            
            meal_type = input("Please enter meal type (Breakfast/Lunch/Dinner/Snack, default Lunch): ").strip()
            if not meal_type:
                meal_type = "Lunch"
            
            print("\n🔄 Starting analysis...")
            result = agent.analyze_meal(image_path, meal_type)
            print("\n" + "=" * 60)
            print("📊 Analysis Results:")
            print("=" * 60)
            print(result.get("output", result))
            
        elif choice == "2":
            days = input("Query recent days (default 7 days): ").strip()
            days = int(days) if days.isdigit() else 7
            
            print("\n🔄 Querying...")
            result = agent.query_history(days)
            print("\n" + "=" * 60)
            print("📈 History Records:")
            print("=" * 60)
            print(result.get("output", result))
            
        elif choice == "3":
            print("\n🔄 Generating recommendations...")
            result = agent.get_recommendation()
            print("\n" + "=" * 60)
            print("💡 Recommendation:")
            print("=" * 60)
            print(result.get("output", result))
            
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option, please try again!")


if __name__ == "__main__":
    main()
