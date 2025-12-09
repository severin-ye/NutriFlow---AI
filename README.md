# 🍽️ NutriFlow AI - Intelligent Nutrition Analysis System

<div align="center">

**A Full-Stack AI-Powered Nutrition Tracking Platform**

Built with LangChain 1.0 + LangGraph | Alibaba Qwen Models | React + TypeScript

English | [简体中文](./README.zh-CN.md)

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API](#-api-documentation)

</div>

---

## 📖 Overview

NutriFlow AI is a comprehensive nutrition analysis platform that uses cutting-edge AI technology to help users track their dietary intake, analyze nutritional balance, and receive personalized meal recommendations.

### What Makes It Special?

- 🤖 **AI-Powered Analysis**: Leverages Alibaba's Qwen multimodal models for accurate dish recognition
- 🔍 **Computer Vision**: Automatically identifies multiple dishes from a single meal photo
- 📊 **Real-Time Nutrition Data**: Online nutrition queries with latest dietary information
- 🎯 **Personalized Insights**: AI-driven health scoring and meal recommendations
- 📈 **Trend Analysis**: 7-day dietary pattern tracking and insights
- 🌐 **Full-Stack Solution**: Complete system from AI backend to React frontend

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Image Recognition** | Qwen-VL-Plus identifies all dishes on a plate with high accuracy |
| ⚖️ **Portion Estimation** | AI estimates portion sizes (small/medium/large) and verifies reasonability |
| 🌐 **Online Nutrition Query** | Real-time web search for up-to-date nutrition data |
| 📊 **Nutrition Calculation** | Calculates 5 key nutrients: calories, protein, fat, carbs, sodium |
| 🎯 **Health Scoring** | Provides scores (0-100) based on nutritional balance |
| 📈 **Dietary Trends** | Analyzes eating patterns over the last 7 days |
| 🕐 **Meal Type Inference** | Auto-detects breakfast/lunch/dinner/snack from timestamp |
| 💡 **Smart Recommendations** | Suggests next meals based on nutritional gaps |
| 💾 **Data Persistence** | Stores complete meal history in structured JSON database |

### User Experience

- ✅ **One-Click Analysis**: Upload photo → Get complete analysis automatically
- ✅ **No Manual Input**: No need to type dish names or portion sizes
- ✅ **Historical Tracking**: Query and visualize past meal records
- ✅ **Trend Insights**: Understand your eating habits over time
- ✅ **Actionable Advice**: Get specific food recommendations for next meals

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     NutriFlow AI Platform                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Frontend  │────▶│  API Backend │────▶│ AI Backend  │ │
│  │  (React/TS) │◀────│  (Node.js)   │◀────│  (Python)   │ │
│  └─────────────┘     └──────────────┘     └─────────────┘ │
│         │                    │                     │        │
│         │                    │                     │        │
│    User Upload          Auth & API           LangChain     │
│    Display UI           Routing              12 Tools      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Frontend (`nutrition_tracker_frontend/`)
- **Framework**: Next.js 14 + React 18
- **Language**: TypeScript
- **UI Library**: shadcn/ui (Tailwind CSS)
- **Key Features**: 
  - Responsive camera interface for meal capture
  - Real-time nutrition display
  - Historical data visualization
  - User authentication

#### API Backend (`nutrition_tracker_backend/`)
- **Runtime**: Node.js
- **Framework**: Express.js
- **Authentication**: JWT-based auth
- **Key Features**:
  - RESTful API endpoints
  - Image upload handling
  - User session management
  - Request routing to AI backend

#### AI Backend (`nutrition_tracker_AI/`)
- **Framework**: LangChain 1.0 + LangGraph
- **Models**: 
  - Qwen-VL-Plus (vision)
  - Qwen-Plus (text reasoning)
- **Tools**: 12 specialized agent tools
- **Database**: JSON-based structured storage
- **Key Features**:
  - Multimodal image analysis
  - Online nutrition queries
  - Health scoring algorithms
  - Meal recommendations

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.12 or higher
- **Node.js**: 18.x or higher
- **Alibaba Cloud API Key**: DashScope (Qwen models)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/severin-ye/NutriFlow-AI.git
cd NutriFlow-AI
```

#### 2. Setup AI Backend

```bash
cd nutrition_tracker_AI

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DASHSCOPE_API_KEY=your_api_key_here" > .env
```

**Get API Key**: Visit [Alibaba Cloud Bailian Platform](https://bailian.console.aliyun.com/)

#### 3. Setup API Backend

```bash
cd ../nutrition_tracker_backend

# Install dependencies
npm install

# Start server
npm start
```

#### 4. Setup Frontend

```bash
cd ../nutrition_tracker_frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running the System

**Option A: Full Stack (Recommended)**

```bash
# Terminal 1 - AI Backend
cd nutrition_tracker_AI
source .venv/bin/activate
python agent_server.py

# Terminal 2 - API Backend
cd nutrition_tracker_backend
npm start

# Terminal 3 - Frontend
cd nutrition_tracker_frontend
npm run dev
```

Visit: `http://localhost:3000`

**Option B: AI Backend CLI Only**

```bash
cd nutrition_tracker_AI
source .venv/bin/activate
python main.py
```

---

## 📚 Documentation

### Project Structure

```
NutriFlow-AI/
├── 📁 nutrition_tracker_AI/          # AI Backend (Python)
│   ├── main.py                       # CLI entry point
│   ├── agent_server.py               # Flask/FastAPI server
│   ├── ai_nutrition_agent/           # Core agent package
│   │   ├── agent.py                  # LangGraph agent (12 tools)
│   │   ├── config/settings.py        # Configuration
│   │   ├── tools/                    # 12 specialized tools
│   │   ├── schemas/                  # Pydantic data models
│   │   ├── prompts/                  # LLM prompt templates
│   │   └── db/meals.json            # Database
│   └── tests/                        # Test suite
│
├── 📁 nutrition_tracker_backend/      # API Backend (Node.js)
│   ├── server.js                     # Express server
│   ├── src/
│   │   ├── controllers/              # Route handlers
│   │   ├── middleware/auth.js        # JWT authentication
│   │   └── routes/                   # API routes
│   └── uploads/                      # Temporary image storage
│
└── 📁 nutrition_tracker_frontend/     # Frontend (React)
    ├── app/                          # Next.js app directory
    │   ├── page.tsx                  # Main tracker page
    │   ├── auth/page.tsx             # Login/signup
    │   └── summary/page.tsx          # Daily summary
    ├── components/
    │   ├── nutrition-tracker.tsx     # Main component
    │   └── daily-summary.tsx         # Summary view
    └── types/                        # TypeScript definitions
```

### AI Backend: 12 Agent Tools

| # | Tool Name | Purpose | Input | Output |
|---|-----------|---------|-------|--------|
| 1 | `detect_dishes_and_portions` | Image recognition via Qwen-VL | image_path | JSON: dishes array |
| 2 | `check_and_refine_portions` | Portion verification | vision_result | JSON: verified portions |
| 3 | `add_nutrition_to_dishes` | Batch nutrition query | portion_result | JSON: with nutrition_per_100g |
| 4 | `query_nutrition_per_100g` | Single dish query | dish_name | JSON: nutrition data |
| 5 | `compute_meal_nutrition` | Calculate totals | nutrition_result | JSON: meal_nutrition_total |
| 6 | `save_meal` | Database persistence | compute_result | Status message |
| 7 | `load_recent_meals` | Load history | days (int) | JSON: recent meals |
| 8 | `get_daily_summary` | Daily report | date (optional) | JSON: daily summary |
| 9 | `score_current_meal` | Basic health scoring | meal_nutrition | Score + advice |
| 10 | `score_current_meal_llm` | LLM-based scoring | meal_data | Detailed score |
| 11 | `score_weekly_adjusted` | Weekly trend scoring | weekly_data | Adjusted score |
| 12 | `recommend_next_meal` | Next meal suggestion | history + current | Recommendations |

### Workflow

```
User uploads image
    ↓
Frontend → API Backend → AI Agent
                            ↓
                    1. Qwen-VL: Image → Dishes
                    2. Verify portions
                    3. Query nutrition (online)
                    4. Calculate totals
                    5. Health scoring
                    6. Generate recommendations
                    7. Save to database
                            ↓
Frontend ← API Backend ← JSON response
    ↓
Display analysis report
```

---

## 🔌 API Documentation

### AI Backend Endpoints

#### `POST /analyze`
Analyze meal image and return complete nutrition analysis.

**Request:**
```json
{
  "image_path": "/path/to/meal.jpg",
  "user_id": "user001"
}
```

**Response:**
```json
{
  "dishes": [
    {
      "name": "Kung Pao Chicken",
      "category": "meat_dish",
      "final_weight_g": 300,
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
  },
  "health_score": 75,
  "recommendations": ["Next meal: low sodium, high fiber..."]
}
```

### API Backend Endpoints

#### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login (returns JWT)

#### Meal Analysis

- `POST /api/analyze` - Upload and analyze meal image
- `GET /api/meals` - Get user's meal history
- `GET /api/meals/:date` - Get meals for specific date

---

## 🧪 Testing

### AI Backend Tests

```bash
cd nutrition_tracker_AI
source .venv/bin/activate

# Run all tests
python -m pytest tests/

# Specific tests
python tests/test_complete_chain.py  # Integration test
python tests/verify_db.py            # Database validation
```

**Test Coverage:**
- ✅ Vision tool (Qwen-VL integration)
- ✅ Portion verification
- ✅ Nutrition query (online)
- ✅ Nutrition calculation
- ✅ Database operations
- ✅ Complete tool chain (end-to-end)

### Sample Test Output

```
======================================================================
🧪 Testing Complete Tool Chain
======================================================================

1️⃣  Vision: ✅ Identified 1 dish
2️⃣  Portion: ✅ Verified 300g (large)
3️⃣  Nutrition: ✅ Queried online (115 kcal/100g)
4️⃣  Calculate: ✅ Total 345 kcal, 25.5g protein
5️⃣  Save: ✅ Saved to database (meal_2025-12-08_1)

======================================================================
✅ All tests passed!
======================================================================
```

---

## 🔧 Configuration

### Environment Variables

**AI Backend** (`.env` in `nutrition_tracker_AI/`):
```bash
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxx
QWEN_VL_MODEL=qwen-vl-plus
QWEN_TEXT_MODEL=qwen-plus
```

**API Backend** (`.env` in `nutrition_tracker_backend/`):
```bash
PORT=5000
JWT_SECRET=your_secret_key
AI_BACKEND_URL=http://localhost:8000
```

**Frontend** (`.env.local` in `nutrition_tracker_frontend/`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Key Settings

**AI Agent Configuration** (`nutrition_tracker_AI/ai_nutrition_agent/config/settings.py`):
```python
DASHSCOPE_API_KEY        # API key
QWEN_VL_MODEL           # Vision model name
QWEN_TEXT_MODEL         # Text model name
DB_PATH                 # Database file path
RECENT_DAYS = 7         # Days for trend analysis
```

---

## 📊 Database Schema

### meals.json Structure

```json
{
  "user_id": "user001",
  "days": [
    {
      "date": "2025-12-09",
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
          "meal_id": "meal_2025-12-09_1",
          "timestamp": "2025-12-09T08:30:00",
          "image_path": "/uploads/breakfast.jpg",
          "dishes": [
            {
              "dish_id": "dish_1",
              "name": "Scrambled Eggs",
              "category": "protein",
              "estimated_weight_g": 150,
              "final_weight_g": 150,
              "portion_level": "medium",
              "nutrition_per_100g": {
                "calories": 140.0,
                "protein": 12.5,
                "fat": 9.5,
                "carbs": 1.5,
                "sodium": 150.0
              },
              "nutrition_total": {
                "calories": 210.0,
                "protein": 18.8,
                "fat": 14.3,
                "carbs": 2.3,
                "sodium": 225.0
              }
            }
          ],
          "meal_nutrition_total": {
            "calories": 210.0,
            "protein": 18.8,
            "fat": 14.3,
            "carbs": 2.3,
            "sodium": 225.0
          }
        }
      ]
    }
  ]
}
```

---

## 🔐 Security

- **Authentication**: JWT-based authentication for API endpoints
- **API Key**: Alibaba Cloud API key stored in environment variables
- **Data Privacy**: User data stored locally, not sent to third parties
- **Image Storage**: Temporary upload files cleaned after processing

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "DASHSCOPE_API_KEY not configured"

**Solution:**
- Ensure `.env` file exists in `nutrition_tracker_AI/`
- Check API key format (should start with `sk-`)
- Restart the application after adding `.env`

#### 2. Image Recognition Returns Empty

**Possible Causes:**
- Unsupported image format (use JPG, PNG, or WebP)
- Image too large (keep under 5MB)
- Poor image quality or lighting
- API quota exceeded

**Solution:**
- Use supported formats and compress images
- Ensure good lighting when taking photos
- Check DashScope account balance

#### 3. Database File Empty/Corrupted

**Solution:**
- The system auto-initializes empty databases
- Check file permissions on `db/meals.json`
- If corrupted, delete file and restart (will create new)

#### 4. Nutrition Values All Zero

**Cause:** Missing `add_nutrition_to_dishes` tool call

**Solution:** 
- Already fixed in current version
- Agent system prompt ensures this tool is called
- Run `python tests/test_complete_chain.py` to verify

#### 5. Frontend Can't Connect to Backend

**Solution:**
- Verify all three services are running
- Check `.env` files have correct URLs
- Ensure no port conflicts (3000, 5000, 8000)

---

## 🎯 Roadmap

### Phase 1: Core Features (✅ Completed)
- [x] AI image recognition
- [x] Nutrition calculation
- [x] Health scoring
- [x] Database persistence
- [x] CLI interface
- [x] Complete test suite

### Phase 2: Full Stack (🚧 In Progress)
- [x] API backend
- [x] React frontend
- [x] User authentication
- [ ] Multi-user support
- [ ] Data visualization dashboard

### Phase 3: Advanced Features (📋 Planned)
- [ ] Mobile app (React Native)
- [ ] Barcode scanning for packaged foods
- [ ] Recipe recommendations
- [ ] Meal planning calendar
- [ ] Export reports (PDF/Excel)
- [ ] Social features (share meals)
- [ ] Integration with fitness apps

### Phase 4: Intelligence Upgrade (🔮 Future)
- [ ] Custom dietary goals
- [ ] Allergy/dietary restriction support
- [ ] Micronutrient tracking
- [ ] Exercise calorie integration
- [ ] Predictive meal suggestions
- [ ] Voice interface

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed description
2. **Suggest Features**: Share your ideas in discussions
3. **Submit PRs**: 
   - Fork the repository
   - Create feature branch (`git checkout -b feature/AmazingFeature`)
   - Commit changes (`git commit -m 'Add AmazingFeature'`)
   - Push to branch (`git push origin feature/AmazingFeature`)
   - Open Pull Request

### Development Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **LangChain**: MIT License
- **Alibaba Qwen Models**: Commercial use requires Alibaba Cloud agreement
- **React**: MIT License
- **Next.js**: MIT License
- **shadcn/ui**: MIT License

---

## 🙏 Acknowledgements

### Core Technologies
- [LangChain](https://github.com/langchain-ai/langchain) - Agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [Alibaba Cloud Qwen](https://www.aliyun.com/product/bailian) - Multimodal AI models
- [Pydantic](https://github.com/pydantic/pydantic) - Data validation
- [Next.js](https://nextjs.org/) - React framework
- [shadcn/ui](https://ui.shadcn.com/) - UI components

### Inspiration
- YOLO for object detection concepts
- MyFitnessPal for nutrition tracking UX
- Calorie Mama for AI-powered food recognition

---

## 📧 Contact & Support

- **Author**: Severin Ye
- **GitHub**: [@severin-ye](https://github.com/severin-ye)
- **Repository**: [NutriFlow-AI](https://github.com/severin-ye/NutriFlow-AI)
- **Issues**: [Report a bug](https://github.com/severin-ye/NutriFlow-AI/issues)

For questions or suggestions, please open an issue or start a discussion.

---

## 📈 Statistics

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Project Stats:**
- 🐍 Python Lines: ~2,000
- 🟢 JavaScript/TypeScript Lines: ~1,500
- 🧪 Test Coverage: 80%+
- 🛠️ AI Tools: 12
- 📊 Data Models: 8
- 📝 Prompt Templates: 6

---

<div align="center">

**Built with ❤️ by Severin Ye**

⭐ Star this repo if you find it helpful!

[Back to Top](#-nutriflow-ai---intelligent-nutrition-analysis-system)

</div>

---

**Last Updated**: December 9, 2025
**Version**: 1.0.0
