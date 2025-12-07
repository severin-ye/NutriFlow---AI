#!/usr/bin/env python3
"""
Intelligent Nutrition Analysis System - Main Program
Based on LangChain 1.0 + LangGraph + Alibaba Qwen
"""
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from ai_nutrition_agent.agent import NutritionAgent
from ai_nutrition_agent.tools.meal_type_tools import infer_meal_type
from ai_nutrition_agent.tools.db_tools import load_recent_meals


def print_header():
    """Print welcome screen"""
    print("\n" + "="*70)
    print("🍽️  Intelligent Nutrition Analysis System".center(70))
    print("Based on LangChain 1.0 + Alibaba Qwen".center(70))
    print("="*70)
    print()


def print_progress(message):
    """Print progress message"""
    print(f"🔄 {message}")


def print_success(message):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message):
    """Print error message"""
    print(f"❌ {message}")


def analyze_meal_from_image():
    """Fully automated meal image analysis"""
    print_header()
    
    # Initialize Agent
    print_progress("Initializing Agent...")
    try:
        agent = NutritionAgent()
        print_success("Agent initialized successfully!")
        print()
    except Exception as e:
        print_error(f"Initialization failed: {str(e)}")
        return
    
    # Input image path
    print("📸 Please enter meal image path:")
    print("   Tip: You can drag image to terminal or paste full path")
    print()
    image_path = input("Image path: ").strip().strip("'\"")  # Remove quotes
    
    if not image_path:
        print_error("未Input image path")
        return
    
    if not os.path.exists(image_path):
        print_error(f"Image does not exist: {image_path}")
        return
    
    print()
    
    # 🆕 Auto infer meal type (based on timestamp and history)
    print_progress("Inferring meal type based on time and history...")
    try:
        # Load recent meal records
        recent_data = load_recent_meals.invoke({"days": 1})  # Only today's records needed
        recent_meals = recent_data.get("days", [])
        
        # Infer meal type
        current_time = datetime.now().isoformat()
        meal_type = infer_meal_type.invoke({
            "timestamp": current_time,
            "recent_meals": recent_meals
        })
        
        print_success(f"Auto-identified meal type: {meal_type}")
        print()
        
    except Exception as e:
        # If inference fails, use time-based default rules
        hour = datetime.now().hour
        if 5 <= hour < 10:
            meal_type = "Breakfast"
        elif 10 <= hour < 14:
            meal_type = "Lunch"
        elif 14 <= hour < 17:
            meal_type = "Afternoon Tea"
        elif 17 <= hour < 21:
            meal_type = "Dinner"
        else:
            meal_type = "Late-night Snack"
        print(f"⚠️  Meal type inference error, using default rules: {meal_type}")
        print()
    
    print("="*70)
    print(f"📊 Starting automatic analysis - {meal_type}".center(70))
    print(f"📸 Image: {os.path.basename(image_path)}".center(70))
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(70))
    print("="*70)
    print()
    
    # 显示执行步骤
    print("🤖 Agent will automatically execute the following steps:")
    print("   1️⃣  Image Recognition (Qwen-VL) - Identify all dishes")
    print("   2️⃣  Portion Verification - Confirm weight reasonability")
    print("   3️⃣  Nutrition Query - Online query nutrition data for each dish")
    print("   4️⃣  Nutrition Calculation - Calculate total meal nutrition")
    print("   5️⃣  Health Scoring - Score based on nutritional balance")
    print("   6️⃣  Trend Analysis - Analyze with historical data")
    print("   7️⃣  Smart Recommendation - Recommend next meal foods")
    print("   8️⃣  Auto Save - Automatically save to database")
    print()
    print_progress("Agent starting work, please wait...")
    print()
    
    # 记录开始Time
    start_time = datetime.now()
    
    # 执行分析
    try:
        result = agent.analyze_meal(image_path, meal_type)
        
        # 计算耗时
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print()
        print("="*70)
        print_success(f"Analysis complete! Time elapsed {duration:.2f} seconds")
        print("="*70)
        print()
        
        # 提取并显示结果
        if "messages" in result:
            messages = result["messages"]
            if messages:
                final_message = messages[-1]
                if hasattr(final_message, 'content'):
                    print("📋 Analysis Report:")
                    print("-"*70)
                    print(final_message.content)
                    print("-"*70)
                else:
                    print(str(final_message))
        else:
            print(str(result))
        
        print()
        print_success("✅ Data automatically saved to database: db/meals.json")
        print()
        
    except Exception as e:
        print()
        print_error(f"Error during analysis: {str(e)}")
        print()
        import traceback
        print("Detailed error information:")
        print(traceback.format_exc())
        
    except Exception as e:
        print()
        print_error(f"Error during analysis: {str(e)}")
        print()
        import traceback
        print("Detailed error information:")
        print(traceback.format_exc())


def quick_query_history():
    """Quick query history"""
    print_header()
    
    print_progress("Initializing Agent...")
    try:
        agent = NutritionAgent()
        print_success("Agent initialized successfully!")
        print()
    except Exception as e:
        print_error(f"Initialization failed: {str(e)}")
        return
    
    days = input("Query recent days of records (default 7 days): ").strip()
    days = int(days) if days.isdigit() else 7
    
    print()
    print_progress(f"Querying recent {days} days of data...")
    print()
    
    try:
        result = agent.query_history(days)
        
        print("="*70)
        print(f"📈 最近 {days} 天的饮食记录".center(70))
        print("="*70)
        print()
        
        if "messages" in result:
            messages = result["messages"]
            if messages:
                final_message = messages[-1]
                if hasattr(final_message, 'content'):
                    print(final_message.content)
                else:
                    print(str(final_message))
        else:
            print(str(result))
        
        print()
        
    except Exception as e:
        print_error(f"查询失败: {str(e)}")


def main_menu():
    """主菜单"""
    print_header()
    
    print("Please select a function:")
    print()
    print("  1. 📸 分析餐盘Image (一键完成所有步骤)")
    print("  2. 📈 Query history")
    print("  3. 💡 Get next meal recommendation")
    print("  4. 🚪 Exit")
    print()
    
    choice = input("Enter number (1-4): ").strip()
    
    if choice == "1":
        analyze_meal_from_image()
    elif choice == "2":
        quick_query_history()
    elif choice == "3":
        print_header()
        print_progress("Initializing Agent...")
        try:
            agent = NutritionAgent()
            print_success("Agent initialized successfully!")
            print()
            print_progress("Generating recommendations...")
            print()
            result = agent.get_recommendation()
            
            print("="*70)
            print("💡 下一餐推荐".center(70))
            print("="*70)
            print()
            
            if "messages" in result:
                messages = result["messages"]
                if messages:
                    final_message = messages[-1]
                    if hasattr(final_message, 'content'):
                        print(final_message.content)
                    else:
                        print(str(final_message))
            else:
                print(str(result))
            
            print()
        except Exception as e:
            print_error(f"推荐生成失败: {str(e)}")
    elif choice == "4":
        print()
        print("👋 谢谢使用，Goodbye!")
        print()
        return
    else:
        print_error("无效选项")
    
    # 询问是否继续
    print()
    continue_choice = input("Return to main menu? (y/n，defaulty): ").strip().lower()
    if continue_choice != "n":
        main_menu()


if __name__ == "__main__":
    main_menu()
