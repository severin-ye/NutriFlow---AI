#!/usr/bin/env python3
"""
智能营养分析系统 - 主程序
基于 LangChain 1.0 + LangGraph + 阿里通义千问
"""
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from ai_nutrition_agent.agent import NutritionAgent
from ai_nutrition_agent.tools.meal_type_tools import infer_meal_type
from ai_nutrition_agent.tools.db_tools import load_recent_meals


def print_header():
    """打印欢迎界面"""
    print("\n" + "="*70)
    print("🍽️  智能营养分析系统".center(70))
    print("基于 LangChain 1.0 + 阿里通义千问".center(70))
    print("="*70)
    print()


def print_progress(message):
    """打印进度信息"""
    print(f"🔄 {message}")


def print_success(message):
    """打印成功信息"""
    print(f"✅ {message}")


def print_error(message):
    """打印错误信息"""
    print(f"❌ {message}")


def analyze_meal_from_image():
    """完全自动化分析餐盘图片"""
    print_header()
    
    # 初始化Agent
    print_progress("正在初始化 Agent...")
    try:
        agent = NutritionAgent()
        print_success("Agent 初始化完成！")
        print()
    except Exception as e:
        print_error(f"初始化失败: {str(e)}")
        return
    
    # 输入图片路径
    print("📸 请输入餐盘图片路径:")
    print("   提示: 可以拖拽图片到终端，或粘贴完整路径")
    print()
    image_path = input("图片路径: ").strip().strip("'\"")  # 去除引号
    
    if not image_path:
        print_error("未输入图片路径")
        return
    
    if not os.path.exists(image_path):
        print_error(f"图片不存在: {image_path}")
        return
    
    print()
    
    # 🆕 自动推断餐型（基于时间戳和历史记录）
    print_progress("正在根据时间和历史记录推断餐型...")
    try:
        # 加载最近的用餐记录
        recent_data = load_recent_meals.invoke({"days": 1})  # 只需要今天的记录
        recent_meals = recent_data.get("days", [])
        
        # 推断餐型
        current_time = datetime.now().isoformat()
        meal_type = infer_meal_type.invoke({
            "timestamp": current_time,
            "recent_meals": recent_meals
        })
        
        print_success(f"自动识别餐型: {meal_type}")
        print()
        
    except Exception as e:
        # 如果推断失败，使用时间段默认规则
        hour = datetime.now().hour
        if 5 <= hour < 10:
            meal_type = "早餐"
        elif 10 <= hour < 14:
            meal_type = "午餐"
        elif 14 <= hour < 17:
            meal_type = "下午茶"
        elif 17 <= hour < 21:
            meal_type = "晚餐"
        else:
            meal_type = "夜宵"
        print(f"⚠️  餐型推断异常，使用默认规则: {meal_type}")
        print()
    
    print("="*70)
    print(f"📊 开始自动分析 - {meal_type}".center(70))
    print(f"📸 图片: {os.path.basename(image_path)}".center(70))
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(70))
    print("="*70)
    print()
    
    # 显示执行步骤
    print("🤖 Agent 将自动执行以下步骤:")
    print("   1️⃣  图像识别 (Qwen-VL) - 识别所有菜品")
    print("   2️⃣  分量验证 - 确认重量合理性")
    print("   3️⃣  营养查询 - 联网查询每道菜营养数据")
    print("   4️⃣  营养计算 - 计算整餐营养总和")
    print("   5️⃣  健康评分 - 基于营养均衡度评分")
    print("   6️⃣  趋势分析 - 结合历史数据分析")
    print("   7️⃣  智能推荐 - 推荐下一餐食物")
    print("   8️⃣  自动保存 - 自动保存到数据库")
    print()
    print_progress("Agent 开始工作，请稍候...")
    print()
    
    # 记录开始时间
    start_time = datetime.now()
    
    # 执行分析
    try:
        result = agent.analyze_meal(image_path, meal_type)
        
        # 计算耗时
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print()
        print("="*70)
        print_success(f"分析完成！耗时 {duration:.2f} 秒")
        print("="*70)
        print()
        
        # 提取并显示结果
        if "messages" in result:
            messages = result["messages"]
            if messages:
                final_message = messages[-1]
                if hasattr(final_message, 'content'):
                    print("📋 分析报告:")
                    print("-"*70)
                    print(final_message.content)
                    print("-"*70)
                else:
                    print(str(final_message))
        else:
            print(str(result))
        
        print()
        print_success("✅ 数据已自动保存到数据库: db/meals.json")
        print()
        
    except Exception as e:
        print()
        print_error(f"分析过程出错: {str(e)}")
        print()
        import traceback
        print("详细错误信息:")
        print(traceback.format_exc())
        
    except Exception as e:
        print()
        print_error(f"分析过程出错: {str(e)}")
        print()
        import traceback
        print("详细错误信息:")
        print(traceback.format_exc())


def quick_query_history():
    """快速查询历史"""
    print_header()
    
    print_progress("正在初始化 Agent...")
    try:
        agent = NutritionAgent()
        print_success("Agent 初始化完成！")
        print()
    except Exception as e:
        print_error(f"初始化失败: {str(e)}")
        return
    
    days = input("查询最近几天的记录 (默认7天): ").strip()
    days = int(days) if days.isdigit() else 7
    
    print()
    print_progress(f"正在查询最近 {days} 天的数据...")
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
    
    print("请选择功能:")
    print()
    print("  1. 📸 分析餐盘图片 (一键完成所有步骤)")
    print("  2. 📈 查询历史记录")
    print("  3. 💡 获取下一餐推荐")
    print("  4. 🚪 退出")
    print()
    
    choice = input("请输入数字 (1-4): ").strip()
    
    if choice == "1":
        analyze_meal_from_image()
    elif choice == "2":
        quick_query_history()
    elif choice == "3":
        print_header()
        print_progress("正在初始化 Agent...")
        try:
            agent = NutritionAgent()
            print_success("Agent 初始化完成！")
            print()
            print_progress("正在生成推荐...")
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
        print("👋 谢谢使用，再见！")
        print()
        return
    else:
        print_error("无效选项")
    
    # 询问是否继续
    print()
    continue_choice = input("是否返回主菜单? (y/n，默认y): ").strip().lower()
    if continue_choice != "n":
        main_menu()


if __name__ == "__main__":
    main_menu()
