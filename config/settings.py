"""
配置文件 - 模型和API配置
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

# 阿里云 Qwen API 配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 模型配置
QWEN_VL_MODEL = "qwen-vl-plus"  # 多模态视觉模型
QWEN_TEXT_MODEL = "qwen-plus"    # 文本模型

# 数据库配置
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "meals.json")

# Prompt文件路径
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")

# 营养数据库路径(CSV)
NUTRITION_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "nutrition_db.csv")

# 系统配置
DEFAULT_USER_ID = "user001"
RECENT_DAYS = 7  # 查询最近N天的记录

# Agent 系统提示词
AGENT_SYSTEM_PROMPT = """你是一个智能营养分析 Agent。

你的任务是：
1. 分析用户提供的餐盘图片
2. 识别所有菜品并估算分量
3. 计算营养成分
4. 给出健康评分和建议
5. 基于历史数据提供下一餐推荐
6. 保存数据到数据库

请严格调用工具并保持 JSON 输出格式的准确性。
"""
