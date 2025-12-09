# NutriFlow AI - Directory Tree

```
NutriFlow-AI/
│
├── 📄 README.md                          # Main project documentation
├── 📄 PROJECT_STRUCTURE.md               # This file - detailed structure guide
├── 📄 requirements.txt                   # Root Python dependencies
│
├── 📁 nutrition_tracker_AI/              # 🐍 AI Backend (Python + LangChain)
│   ├── 📄 README.md
│   ├── �� main.py                       # CLI entry point
│   ├── 📄 agent_server.py               # Flask/FastAPI API server
│   ├── 📄 requirements.txt
│   │
│   ├── 📁 ai_nutrition_agent/           # Core agent package
│   │   ├── 📄 __init__.py
│   │   ├── 📄 agent.py                 # ⭐ Main LangGraph agent (12 tools)
│   │   ├── 📄 gui_agent.py
│   │   │
│   │   ├── 📁 config/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 settings.py          # API keys, paths, prompts
│   │   │
│   │   ├── 📁 tools/                   # 🛠️ 12 Agent Tools
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 vision_tools.py      # 1. Image recognition (Qwen-VL)
│   │   │   ├── 📄 portion_tools.py     # 2. Portion verification
│   │   │   ├── 📄 nutrition_tools.py   # 3-4. Nutrition query (online)
│   │   │   ├── 📄 compute_tools.py     # 5. Nutrition calculation
│   │   │   ├── 📄 meal_type_tools.py   # Meal type inference
│   │   │   ├── 📄 db_tools.py          # 6-8. Database operations
│   │   │   └── 📄 recommendation_tools.py # 9-12. Scoring & recommendations
│   │   │
│   │   ├── 📁 schemas/                 # 📊 Data Models (Pydantic)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 meal_schema.py       # Meal, Dish, Nutrition structures
│   │   │   └── 📄 tool_schema.py       # Tool I/O schemas
│   │   │
│   │   ├── 📁 prompts/                 # 📝 LLM Prompt Templates
│   │   │   ├── 📄 vision_prompt.txt
│   │   │   ├── 📄 portion_prompt.txt
│   │   │   ├── 📄 score_prompt.txt
│   │   │   ├── 📄 trend_prompt.txt
│   │   │   ├── 📄 nextmeal_prompt.txt
│   │   │   └── 📄 summary_prompt.txt
│   │   │
│   │   └── 📁 db/
│   │       └── 📄 meals.json           # Main database file
│   │
│   ├── 📁 db/                          # Database backup
│   │   └── 📄 meals.json
│   │
│   ├── �� tests/                       # 🧪 Test Suite
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_tools.py            # Unit tests
│   │   ├── 📄 test_complete_chain.py   # Integration tests
│   │   ├── �� test_save.py             # Database tests
│   │   └── 📄 verify_db.py             # DB validation script
│   │
│   ├── 📁 doc/                         # 📚 Design Documents
│   │   ├── 📄 设计思路 联网版.md
│   │   ├── 📄 联网查询说明.md
│   │   ├── 📄 实现顺序.md
│   │   └── 📄 langchain 1.0教程.md
│   │
│   └── 📁 [temp files]                 # Temporary analysis files
│       ├── 📄 ai_response.json
│       ├── 📄 data.json
│       ├── 📄 output.json
│       ├── 📄 log.txt
│       └── 📄 my_file.txt
│
├── 📁 nutrition_tracker_backend/       # 🟢 API Backend (Node.js + Express)
│   ├── 📄 README.md
│   ├── �� package.json
│   ├── 📄 package-lock.json
│   └── 📄 analyze_response_log.json
│
└── 📁 nutrition_tracker_frontend/      # ⚛️ Frontend (React + TypeScript)
    ├── 📄 README.md
    ├── 📄 package.json
    ├── 📄 package-lock.json
    ├── 📄 tsconfig.json
    ├── 📄 components.json              # shadcn/ui config
    └── 📁 data/
        └── 📄 users.json               # User data
```

---

## 🔑 Key Components Explained

### AI Backend Core (`nutrition_tracker_AI/ai_nutrition_agent/`)

#### **agent.py** - Main Agent Implementation
- Creates LangGraph ReAct agent using `create_react_agent()`
- Registers 12 tools
- Handles tool orchestration and execution flow
- Main methods: `analyze_meal()`, `query_history()`, `recommend_meal()`

#### **tools/** - 12 Agent Tools
| Tool | File | Purpose |
|------|------|---------|
| 1️⃣ detect_dishes_and_portions | vision_tools.py | Qwen-VL image recognition |
| 2️⃣ check_and_refine_portions | portion_tools.py | Portion verification |
| 3️⃣ add_nutrition_to_dishes | nutrition_tools.py | Batch nutrition query |
| 4️⃣ query_nutrition_per_100g | nutrition_tools.py | Single dish query |
| 5️⃣ compute_meal_nutrition | compute_tools.py | Calculate totals |
| 6️⃣ save_meal | db_tools.py | Save to database |
| 7️⃣ load_recent_meals | db_tools.py | Load history |
| 8️⃣ get_daily_summary | db_tools.py | Daily report |
| 9️⃣ score_current_meal | recommendation_tools.py | Basic scoring |
| 🔟 score_current_meal_llm | recommendation_tools.py | LLM scoring |
| 1️⃣1️⃣ score_weekly_adjusted | recommendation_tools.py | Weekly trend |
| 1️⃣2️⃣ recommend_next_meal | recommendation_tools.py | Next meal recommendation |

#### **schemas/** - Data Models
- `meal_schema.py`: Meal, Dish, DailyRecord, Nutrition
- `tool_schema.py`: Tool input/output validation

#### **prompts/** - Prompt Engineering
Contains carefully crafted prompts for each agent task:
- Vision analysis
- Portion estimation
- Health scoring
- Trend analysis
- Meal recommendations

#### **config/settings.py** - Configuration Hub
```python
DASHSCOPE_API_KEY        # Alibaba Cloud API key
QWEN_VL_MODEL           # qwen-vl-plus
QWEN_TEXT_MODEL         # qwen-plus
DB_PATH                 # Database file path
AGENT_SYSTEM_PROMPT     # Main agent instructions
```

---

## 📊 Data Flow Through Components

```
┌─────────────────────────────────────────────────────────────┐
│                        User Action                          │
│              (Upload meal image via Frontend)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Frontend (React + TypeScript)                  │
│  - Image upload component                                   │
│  - Display analysis results                                 │
│  - Nutrition charts & trends                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP POST /analyze
                       ▼
┌─────────────────────────────────────────────────────────────┐
│             API Backend (Node.js + Express)                 │
│  - RESTful API endpoints                                    │
│  - User authentication                                      │
│  - Request routing                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ Call Python agent
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          AI Backend (LangChain Agent Server)                │
│                  agent_server.py                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │   LangGraph Agent (agent.py)     │
        │   Orchestrates 12 tools:         │
        └──────────────┬───────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   [Vision]      [Nutrition]    [Scoring]
   Qwen-VL       Qwen-Plus      Algorithm
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  meals.json    │
              │   Database     │
              └────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │      Analysis Results (JSON)     │
        │  - Dishes identified             │
        │  - Nutrition calculated          │
        │  - Health score                  │
        │  - Recommendations               │
        └──────────────┬───────────────────┘
                       │
                       ▼
              Return to Frontend
                       │
                       ▼
              Display to User
```

---

## 🧪 Testing Structure

```
tests/
├── test_tools.py              # Unit tests for individual tools
├── test_complete_chain.py     # Integration test (vision → save)
├── test_save.py               # Database operation tests
└── verify_db.py               # Database integrity validation
```

**Run tests:**
```bash
cd nutrition_tracker_AI
python tests/test_complete_chain.py
```

---

## 🔐 Environment Setup

### Required Files

**`.env`** (create in `nutrition_tracker_AI/`):
```bash
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxx
```

### API Key Sources
- Alibaba Cloud DashScope: https://bailian.console.aliyun.com/

---

## 📦 Dependencies Overview

### Python (AI Backend)
```
langchain >= 1.0.0          # Agent framework
langgraph                   # Workflow engine
langchain-community         # Community integrations
pydantic == 2.12.5         # Data validation
openai                      # API client (DashScope compatible)
pillow                      # Image processing
python-dotenv              # Environment variables
```

### Node.js (API Backend)
```json
{
  "express": "^4.x",
  "cors": "^2.x",
  "body-parser": "^1.x"
}
```

### React (Frontend)
```json
{
  "react": "^18.x",
  "typescript": "^5.x",
  "@shadcn/ui": "latest"
}
```

---

## 🎯 Entry Points

| Component | Entry Point | Command |
|-----------|-------------|---------|
| AI Backend (CLI) | `nutrition_tracker_AI/main.py` | `python main.py` |
| AI Backend (API) | `nutrition_tracker_AI/agent_server.py` | `python agent_server.py` |
| API Backend | `nutrition_tracker_backend/[server].js` | `npm start` |
| Frontend | `nutrition_tracker_frontend/` | `npm run dev` |

---

## 📈 Development Status

✅ **Completed:**
- AI agent with 12 tools
- Image recognition (Qwen-VL)
- Online nutrition query
- Database persistence
- CLI interface
- Complete test suite

🚧 **In Progress:**
- API server integration
- Frontend development
- User authentication

🔮 **Planned:**
- Multi-user support
- Data visualization dashboard
- Export reports (PDF)
- Mobile app

---

**Generated**: 2025-12-09
