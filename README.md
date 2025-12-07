# 🍽️ NutriFlow · AI - Intelligent Nutrition Analysis System

An intelligent nutrition analysis assistant built with **LangChain 1.0 + LangGraph**, utilizing Alibaba Cloud Qwen multimodal models to achieve meal image recognition, nutritional analysis, health scoring, and intelligent recommendations.

---

## ✨ Key Features

- 🔍 **Smart Image Recognition** - Uses Qwen-VL-Plus multimodal model to identify all dishes on the plate
- ⚖️ **Portion Estimation & Verification** - AI-powered intelligent estimation and verification of dish weights (small/medium/large portions)
- 🌐 **Online Nutrition Query** - Real-time online query for latest nutrition data, no local database maintenance needed
- 📊 **Nutrition Calculation** - Precise calculation of five major nutrients (calories, protein, fat, carbohydrates, sodium)
- 🎯 **Health Scoring** - Provides health scores and personalized recommendations based on nutritional balance
- 📈 **Dietary Trend Analysis** - Analyzes dietary patterns and trends using the last 7 days of data
- 🕐 **Intelligent Meal Type Inference** - Automatically infers meal type (breakfast/lunch/dinner/snack) based on timestamp and history
- 💡 **Next Meal Recommendation** - Recommends next meal foods based on dietary history and nutritional gaps
- 💾 **Data Persistence** - Stores all meal records using JSON database

---

## 🏗️ Project Structure

```
HCI/
├── main.py                          # Main program entry
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (create yourself)
├── image.png                       # Sample image
├── README.md                       # This file
│
├── ai_nutrition_agent/             # Core business logic
│   ├── __init__.py
│   ├── agent.py                    # LangGraph Agent main file
│   │
│   ├── config/                     # Configuration module
│   │   ├── __init__.py
│   │   └── settings.py             # API, model, path configuration
│   │
│   ├── tools/                      # Tools module (12 tools)
│   │   ├── __init__.py
│   │   ├── vision_tools.py         # Image recognition (Qwen-VL)
│   │   ├── portion_tools.py        # Portion verification & refinement
│   │   ├── nutrition_tools.py      # Online nutrition query + batch add
│   │   ├── compute_tools.py        # Nutrition calculation & summary
│   │   ├── db_tools.py             # Database read/write
│   │   ├── meal_type_tools.py      # Meal type inference
│   │   └── recommendation_tools.py # Health scoring & recommendations
│   │
│   ├── schemas/                    # Data models
│   │   ├── __init__.py
│   │   ├── meal_schema.py          # Meal data structure (Pydantic)
│   │   └── tool_schema.py          # Tool input/output structure
│   │
│   ├── prompts/                    # Prompt templates
│   │   ├── vision_prompt.txt       # Image recognition prompt
│   │   ├── portion_prompt.txt      # Portion verification prompt
│   │   ├── score_prompt.txt        # Health scoring prompt
│   │   ├── trend_prompt.txt        # Trend analysis prompt
│   │   ├── nextmeal_prompt.txt     # Next meal recommendation prompt
│   │   └── summary_prompt.txt      # Summary report prompt
│   │
│   └── db/                         # Database (auto-created)
│       └── meals.json              # Meal records database
│
├── db/                             # Database backup directory
│   └── meals.json
│
├── tests/                          # Test files
│   ├── __init__.py
│   ├── test_tools.py               # Tool unit tests
│   ├── test_complete_chain.py      # Complete tool chain test
│   ├── test_save.py                # Database save test
│   └── verify_db.py                # Database verification script
│
└── doc/                            # Design documents
    ├── Design_Online_Version.md
    ├── Online_Query_Guide.md
    ├── Implementation_Order.md
    └── LangChain_1.0_Tutorial.md
```

---

## 🚀 Quick Start

### 1. Environment Setup

**System Requirements**:
- Python 3.12+
- Alibaba Cloud DashScope API Key (Qwen)

**Install Dependencies**:

```bash
# Clone the project
cd /path/to/HCI

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file and add your Alibaba Cloud API Key:

```bash
# .env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

**Get API Key**:
1. Visit [Alibaba Cloud Bailian Platform](https://bailian.console.aliyun.com/)
2. Enable Qwen service
3. Get API Key

### 3. Run the Program

```bash
python main.py
```

**Main Menu**:

```
======================================================================
              🍽️  Intelligent Nutrition Analysis System                             
              Based on LangChain 1.0 + Alibaba Qwen                       
======================================================================

Please select a function:

  1. 📸 Analyze meal image (one-click complete process)
  2. 📈 Query history
  3. 💡 Get next meal recommendation
  4. 🚪 Exit

Enter number (1-4):
```

### 4. Analyze Meal Image

Select option `1`, enter image path:

```bash
Image path: /path/to/your/meal_image.png
```

The system will automatically:
1. ✅ Automatically infer meal type based on time (breakfast/lunch/dinner/snack)
2. ✅ Qwen-VL recognizes all dishes and estimates portions
3. ✅ AI verifies portion reasonability
4. ✅ Online query for nutrition data of each dish
5. ✅ Calculate total meal nutrition
6. ✅ Health scoring and recommendations
7. ✅ Analyze trends with historical data
8. ✅ Recommend next meal foods
9. ✅ Auto-save to database

**Sample Output**:

```
📋 Analysis Report:
----------------------------------------------------------------------
# Meal Analysis Report

## 1. Dish Recognition & Portion Estimation
- **Kung Pao Chicken**: 300g (large portion), dishes are stacked high on the plate, with abundant ingredients like chicken, peanuts, carrots visible

## 2. Nutrition Calculation
- **Total Calories**: 345 kcal
- **Protein**: 25.5 g
- **Fat**: 18.6 g
- **Carbohydrates**: 21.9 g
- **Sodium**: 960 mg

## 3. Health Score & Recommendations
- **Score**: 75 points
- **Recommendations**:
  - Moderate calories
  - Sufficient protein
  - Sodium slightly high, recommend low-sodium foods for next meal

## 4. Trend Analysis
- **Recent Nutrition Trends**: Average 1850 kcal/day in last 7 days, sufficient protein intake

## 5. Next Meal Recommendations
### Option 1: High Protein Low Sodium Balanced Meal
- **Recommended Dishes**: Steamed chicken breast, boiled broccoli, brown rice (small portion)
- **Reason**: Supplement fiber, reduce sodium intake

## 6. Data Saved
- **Successfully saved meal record to 2025-12-08, Meal ID: meal_2025-12-08_1**
----------------------------------------------------------------------
```

---

## 🛠️ Technical Architecture

### Core Technology Stack

- **LangChain 1.0** - Agent framework
- **LangGraph** - Workflow orchestration (`create_react_agent`)
- **Pydantic 2.12** - Data validation
- **Qwen-VL-Plus** - Multimodal vision model (image recognition)
- **Qwen-Plus** - Text reasoning model (portion verification, nutrition query)
- **OpenAI SDK** - Compatible with DashScope API

### Agent Workflow

The system uses **12 tools** working collaboratively, strictly following this sequence:

```
1. detect_dishes_and_portions(image_path)
   ↓ Returns vision_result (JSON)
   
2. check_and_refine_portions(vision_result)
   ↓ Returns portion_result (JSON)
   
3. add_nutrition_to_dishes(portion_result)  ← 🔴 Critical step
   ↓ Returns nutrition_result (JSON)
   
4. compute_meal_nutrition(nutrition_result)
   ↓ Returns compute_result (JSON)
   
5. save_meal(compute_result)
   ↓ Saves to database
```

### Key Design Decisions

#### 1. **JSON String Communication**
All tools return JSON strings (not Python dicts) because LangChain automatically serializes complex types. This avoids `'str' object has no attribute 'get'` errors.

#### 2. **Online Nutrition Query**
Does not rely on local nutrition database, but uses Qwen-Plus + Web Search for real-time queries, ensuring data is latest and comprehensive.

#### 3. **Intelligent Meal Type Inference**
Automatically infers meal type based on time and history:
- 06:00-09:30 → Breakfast
- 11:00-13:30 → Lunch
- 17:00-20:00 → Dinner
- Other times → Snack (intelligently judged with historical data)

#### 4. **Atomic Database Write**
Uses temporary file + `os.replace()` to ensure no data loss on write failure.

#### 5. **Strict Error Checking**
Adds DEBUG logs and exception throwing at critical points (nutrition calculation, data saving) to avoid silent failures.

---

## 📊 Database Structure

Sample `db/meals.json` structure:

```json
{
  "user_id": "user001",
  "days": [
    {
      "date": "2025-12-08",
      "daily_summary": {
        "total_calories": 1850.0,
        "total_protein": 85.2,
        "total_fat": 62.5,
        "total_carbs": 210.3,
        "total_sodium": 2500.0,
        "daily_score": 78
      },
      "meals": [
        {
          "meal_id": "meal_2025-12-08_1",
          "timestamp": "2025-12-08T12:30:15.123456",
          "image_path": "/path/to/image.png",
          "dishes": [
            {
              "dish_id": "dish_1",
              "name": "Kung Pao Chicken",
              "category": "meat_dish",
              "estimated_weight_g": 300,
              "final_weight_g": 300,
              "portion_level": "large",
              "nutrition_per_100g": {
                "calories": 115.0,
                "protein": 8.5,
                "fat": 6.2,
                "carbs": 7.3,
                "sodium": 320.0
              },
              "nutrition_total": {
                "calories": 345.0,
                "protein": 25.5,
                "fat": 18.6,
                "carbs": 21.9,
                "sodium": 960.0
              }
            }
          ],
          "meal_nutrition_total": {
            "calories": 345.0,
            "protein": 25.5,
            "fat": 18.6,
            "carbs": 21.9,
            "sodium": 960.0
          }
        }
      ]
    }
  ]
}
```

---

## 🧪 Testing

The project includes a complete test suite:

```bash
# Test complete tool chain
python tests/test_complete_chain.py

# Test database save
python tests/test_save.py

# Verify database consistency
python tests/verify_db.py
```

**Sample Test Output**:

```
======================================================================
🧪 Testing Complete Tool Chain
======================================================================

1️⃣  Simulating vision_tools return value...
   ✅ vision_result ready

2️⃣  Calling check_and_refine_portions...
   ✅ portion complete: dish count: 1, has final_weight_g: True

3️⃣  Calling add_nutrition_to_dishes...
   ✅ nutrition complete: has nutrition_per_100g: True

4️⃣  Calling compute_meal_nutrition...
   ✅ compute complete: total meal nutrition: 345 kcal, 25.5g protein

5️⃣  Calling save_meal...
   ✅ save complete: meal_2025-12-08_1

======================================================================
✅ Complete tool chain test passed!
======================================================================
```

---

## 🔧 FAQ

### Q1: Error "DASHSCOPE_API_KEY not configured"

**Solution**:
1. Ensure `.env` file exists in project root directory
2. Check API Key format is correct
3. Restart terminal or reactivate virtual environment

### Q2: Image recognition fails or returns empty results

**Reasons**:
- Unsupported image format (supports jpg, png, webp)
- Image too large (recommend < 5MB)
- Insufficient API quota

**Solutions**:
- Use supported image formats
- Compress image size
- Check DashScope account balance

### Q3: Database file is empty

**Reason**: Program encountered error while writing data, older versions would clear the file.

**Solution**: Fixed in latest version, now uses atomic write (temp file + replace). If empty file is encountered, program will auto-initialize.

### Q4: All nutrition data is 0

**Reason**: Missing `add_nutrition_to_dishes` tool call.

**Solution**: Agent system prompt now explicitly requires calling this tool to ensure complete tool chain.

---

## 🎯 Roadmap

- [ ] Support GUI interface (based on Gradio/Streamlit)
- [ ] Multi-user management
- [ ] Automatic meal photo archiving
- [ ] Export health reports (PDF/Excel)
- [ ] Micronutrient analysis (vitamins, minerals)
- [ ] Exercise consumption tracking & recommendations
- [ ] Data visualization dashboard

---

## 📄 License

This project is for learning and research purposes only.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) - Agent framework
- [Alibaba Cloud Qwen](https://www.aliyun.com/product/bailian) - Multimodal AI models
- [Pydantic](https://github.com/pydantic/pydantic) - Data validation

---

## 📧 Contact

Feel free to submit Issues for questions or suggestions.

---

**Last Updated**: 2025-12-08
