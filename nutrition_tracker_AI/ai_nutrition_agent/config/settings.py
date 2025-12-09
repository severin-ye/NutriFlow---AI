"""
Configuration File - Model and API Configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Alibaba Cloud Qwen API Configuration
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# Model Configuration
QWEN_VL_MODEL = "qwen-vl-plus"  # Multimodal vision model
QWEN_TEXT_MODEL = "qwen-plus"    # Text model

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "meals.json")

# Prompt file path
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")

# Nutrition database path (CSV)
NUTRITION_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "nutrition_db.csv")

# System Configuration
DEFAULT_USER_ID = "user001"
RECENT_DAYS = 7  # Query records for recent N days

# Agent System Prompt
AGENT_SYSTEM_PROMPT = """You are an intelligent English speaking nutrition analysis Agent.

Your tasks are:
1. Analyze the meal image provided by the user
2. Identify all dishes and estimate portions
3. Query nutrition content (must call add_nutrition_to_dishes for batch addition)
4. Calculate nutrition totals
5. Provide health scores and recommendations
6. Provide next meal recommendations based on historical data
7. Automatically save data to database

⚠️ Key tool calling sequence:
1. detect_dishes_and_portions(image_path) → vision_result
2. check_and_refine_portions(vision_result) → portion_result  
3. add_nutrition_to_dishes(portion_result) → nutrition_result  ← 🔴 Must call!
4. compute_meal_nutrition(nutrition_result) → compute_result
5. save_meal(compute_result)

Note: All tools return JSON strings, just pass directly to the next tool.
"""
