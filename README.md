# 🍽️ AI Nutrition Agent - 智能营养分析系统

基于 LangChain 1.0 + LangGraph 构建的智能营养分析助手，使用阿里云通义千问(Qwen)模型。

## 📋 功能特性

- 🔍 **图像识别**: 使用 Qwen-VL 识别餐盘中的多道菜品
- ⚖️ **分量估算**: 智能估算并验证每道菜的重量
- 📊 **营养分析**: 计算完整的营养成分(热量、蛋白质、脂肪、碳水、钠)
- 🎯 **健康评分**: 基于营养均衡度给出健康评分和建议
- 📈 **趋势分析**: 结合最近7天数据进行趋势评估
- 💡 **智能推荐**: 根据饮食历史推荐下一餐食物
- 💾 **数据持久化**: 使用JSON数据库存储所有记录

## 🏗️ 项目结构

```
ai-nutrition-agent/
├── agent.py                      # 主Agent文件
├── tools/                        # 工具层
│   ├── vision_tools.py          # Qwen-VL 图像识别
│   ├── portion_tools.py         # 分量验证
│   ├── nutrition_tools.py       # 营养查询
│   ├── compute_tools.py         # 营养计算
│   ├── db_tools.py              # 数据库操作
│   └── recommendation_tools.py  # 推荐生成
├── schemas/                      # 数据模型
│   ├── meal_schema.py           # 餐食数据结构
│   └── tool_schema.py           # 工具输入输出结构
├── prompts/                      # 提示词文件
│   ├── vision_prompt.txt
│   ├── portion_prompt.txt
│   ├── score_prompt.txt
│   ├── trend_prompt.txt
│   ├── nextmeal_prompt.txt
│   └── summary_prompt.txt
├── db/                           # 数据库
│   ├── meals.json               # 主数据库
│   └── nutrition_db.csv         # 营养数据库
├── config/
│   └── settings.py              # 配置文件
├── .env                         # 环境变量
└── requirements.txt             # 依赖包
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install pandas Pillow
```

### 2. 配置API Key

在 `.env` 文件中配置阿里云API Key:

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 运行Agent

```bash
python agent.py
```

## 📖 使用说明

### CLI界面

运行 `agent.py` 后会进入交互式界面:

1. **分析餐盘图片**: 上传图片进行完整营养分析
2. **查询历史记录**: 查看最近N天的饮食数据
3. **获取下一餐推荐**: 基于历史数据获取推荐

### 编程接口

```python
from agent import NutritionAgent

# 创建Agent实例
agent = NutritionAgent()

# 分析餐盘图片
result = agent.analyze_meal("meal.jpg", meal_type="午餐")

# 查询历史
history = agent.query_history(days=7)

# 获取推荐
recommendation = agent.get_recommendation()
```

## 🔧 核心工具

| 工具 | 功能 | 模型 |
|-----|------|------|
| `detect_dishes_and_portions` | 识别菜品和估算分量 | Qwen-VL-Plus |
| `check_and_refine_portions` | 验证分量合理性 | Qwen-Plus |
| `query_nutrition_per_100g` | 查询营养数据 | 本地CSV |
| `compute_meal_nutrition` | 计算整餐营养 | 规则 |
| `score_current_meal_llm` | 本餐评分 | Qwen-Plus |
| `score_weekly_adjusted` | 趋势评分 | Qwen-Plus |
| `recommend_next_meal` | 生成推荐 | Qwen-Plus |
| `load_recent_meals` | 加载历史 | JSON |
| `save_meal` | 保存数据 | JSON |

## 📊 数据库结构

### JSON数据库 (`db/meals.json`)

```json
{
  "user_id": "user001",
  "days": [
    {
      "date": "2025-12-07",
      "daily_summary": {
        "total_calories": 0,
        "total_protein": 0,
        "total_fat": 0,
        "total_carbs": 0,
        "total_sodium": 0,
        "daily_score": 0
      },
      "meals": []
    }
  ]
}
```

### 营养数据库 (`db/nutrition_db.csv`)

包含常见食物的每100g营养成分数据，支持模糊匹配。

## 🎯 执行流程

当分析一张餐盘图片时，Agent会自动执行以下步骤:

1. **图像识别** → 识别所有菜品并粗估分量
2. **分量验证** → 检查重量是否合理，不合理则修正
3. **营养查询** → 对每道菜查询每100g营养成分
4. **营养计算** → 计算每道菜和整餐的总营养
5. **加载历史** → 读取最近7天的饮食记录
6. **本餐评分** → 根据营养均衡度评分
7. **趋势评分** → 结合历史趋势调整评分
8. **生成推荐** → 推荐下一餐食物
9. **保存数据** → 写入JSON数据库

## 🔑 技术特点

- ✅ **LangChain 1.0架构**: 使用最新的Agent框架
- ✅ **工具驱动**: 所有逻辑封装为可复用的工具
- ✅ **Pydantic验证**: 确保数据结构的一致性
- ✅ **JSON持久化**: 简单可靠的数据存储
- ✅ **模糊匹配**: 智能查找相似菜品
- ✅ **趋势分析**: 长期营养监控

## 📝 开发说明

### 添加新菜品

编辑 `db/nutrition_db.csv`，添加新的菜品营养数据。

### 修改提示词

编辑 `prompts/` 目录下的相应文件。

### 扩展工具

在 `tools/` 目录创建新文件，使用 `@tool` 装饰器定义新工具，然后在 `agent.py` 中注册。

## ⚠️ 注意事项

- 确保阿里云API Key已正确配置
- 图像文件需要是常见格式(jpg/png)
- 营养数据库需要定期维护更新
- JSON数据库会持续增长，建议定期备份

## 📄 许可证

MIT License

## 👨‍💻 作者

Severin (叶博韬)

---

**祝你使用愉快！🎉**
