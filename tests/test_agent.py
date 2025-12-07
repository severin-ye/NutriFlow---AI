"""
测试脚本 - 使用示例图片测试Agent
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from agent import NutritionAgent


def test_with_sample_image():
    """使用示例图片测试Agent"""
    print("=" * 60)
    print("🧪 测试模式 - 智能营养分析系统")
    print("=" * 60)
    print()
    
    # 初始化Agent
    print("正在初始化Agent...")
    agent = NutritionAgent()
    print("✅ Agent初始化完成！")
    print()
    
    # 使用langchain 1.0教程.md中的图片路径
    test_image = "/home/severin/Codelib/HCI/doc/langchain 1.0教程.md"
    
    # 检查文件是否存在
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        print("请提供一个有效的图片路径")
        return
    
    print(f"📸 使用测试图片: {test_image}")
    print()
    
    # 测试1: 分析餐盘图片
    print("\n" + "=" * 60)
    print("测试 1: 分析餐盘图片")
    print("=" * 60)
    result = agent.analyze_meal(test_image, "午餐")
    print("\n📊 分析结果：")
    print(result)
    
    # 测试2: 查询历史记录
    print("\n\n" + "=" * 60)
    print("测试 2: 查询历史记录")
    print("=" * 60)
    result = agent.query_history(7)
    print("\n📈 历史记录：")
    print(result)
    
    # 测试3: 获取下一餐推荐
    print("\n\n" + "=" * 60)
    print("测试 3: 获取下一餐推荐")
    print("=" * 60)
    result = agent.get_recommendation()
    print("\n💡 推荐内容：")
    print(result)
    
    print("\n\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_with_sample_image()
