以下为**原文内容的完整、忠实中文翻译**，在不增删、不改写含义的前提下，保留原有结构、符号与技术细节。

---

# 🍽️ NutriFlow · AI —— 智能营养分析系统

一个基于 **LangChain 1.0 + LangGraph** 构建的智能营养分析助手，利用阿里云通义千问（Qwen）多模态模型，实现餐食图片识别、营养分析、健康评分以及智能推荐。

---

## ✨ 核心功能

* 🔍 **智能图像识别** —— 使用 Qwen-VL-Plus 多模态模型识别餐盘中的所有菜品
* ⚖️ **分量估计与校验** —— 基于 AI 的菜品重量智能估计与校验（小 / 中 / 大份）
* 🌐 **在线营养查询** —— 实时在线查询最新营养数据，无需维护本地数据库
* 📊 **营养计算** —— 精准计算五大核心营养素（热量、蛋白质、脂肪、碳水化合物、钠）
* 🎯 **健康评分** —— 基于营养均衡情况给出健康评分与个性化建议
* 📈 **饮食趋势分析** —— 基于最近 7 天数据分析饮食模式与趋势
* 🕐 **智能餐次推断** —— 根据时间戳与历史记录自动推断餐次（早餐 / 午餐 / 晚餐 / 加餐）
* 💡 **下一餐推荐** —— 根据饮食历史与营养缺口推荐下一餐食物
* 💾 **数据持久化** —— 使用 JSON 数据库存储所有餐食记录

---

## 🏗️ 项目结构

```
HCI/
├── main.py                          # 主程序入口
├── requirements.txt                 # Python 依赖
├── .env                            # 环境变量（需自行创建）
├── image.png                       # 示例图片
├── README.md                       # 本文件
│
├── ai_nutrition_agent/             # 核心业务逻辑
│   ├── __init__.py
│   ├── agent.py                    # LangGraph Agent 主文件
│   │
│   ├── config/                     # 配置模块
│   │   ├── __init__.py
│   │   └── settings.py             # API、模型、路径配置
│   │
│   ├── tools/                      # 工具模块（共 12 个工具）
│   │   ├── __init__.py
│   │   ├── vision_tools.py         # 图像识别（Qwen-VL）
│   │   ├── portion_tools.py        # 分量校验与修正
│   │   ├── nutrition_tools.py      # 在线营养查询 + 批量添加
│   │   ├── compute_tools.py        # 营养计算与汇总
│   │   ├── db_tools.py             # 数据库读写
│   │   ├── meal_type_tools.py      # 餐次推断
│   │   └── recommendation_tools.py # 健康评分与推荐
│   │
│   ├── schemas/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── meal_schema.py          # 餐食数据结构（Pydantic）
│   │   └── tool_schema.py          # 工具输入 / 输出结构
│   │
│   ├── prompts/                    # Prompt 模板
│   │   ├── vision_prompt.txt       # 图像识别 Prompt
│   │   ├── portion_prompt.txt      # 分量校验 Prompt
│   │   ├── score_prompt.txt        # 健康评分 Prompt
│   │   ├── trend_prompt.txt        # 趋势分析 Prompt
│   │   ├── nextmeal_prompt.txt     # 下一餐推荐 Prompt
│   │   └── summary_prompt.txt      # 汇总报告 Prompt
│   │
│   └── db/                         # 数据库（自动创建）
│       └── meals.json              # 餐食记录数据库
│
├── db/                             # 数据库备份目录
│   └── meals.json
│
├── tests/                          # 测试文件
│   ├── __init__.py
│   ├── test_tools.py               # 工具单元测试
│   ├── test_complete_chain.py      # 完整工具链测试
│   ├── test_save.py                # 数据库存储测试
│   └── verify_db.py                # 数据库校验脚本
│
└── doc/                            # 设计文档
    ├── Design_Online_Version.md
    ├── Online_Query_Guide.md
    ├── Implementation_Order.md
    └── LangChain_1.0_Tutorial.md
```

---

## 🚀 快速开始

### 1. 环境配置

**系统要求**：

* Python 3.12+
* 阿里云 DashScope API Key（Qwen）

**安装依赖**：

```bash
# 克隆项目
cd /path/to/HCI

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux / Mac
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

---

### 2. 配置 API Key

创建 `.env` 文件并添加你的阿里云 API Key：

```bash
# .env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

**获取 API Key**：

1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 开通 Qwen 服务
3. 获取 API Key

---

### 3. 运行程序

```bash
python main.py

或

通过以下方式启动本地服务：

uvicorn agent_server:app --host 0.0.0.0 --port 8000 --reload
```

**主菜单**：

```
======================================================================
              🍽️  智能营养分析系统                             
              基于 LangChain 1.0 + 阿里云 Qwen                       
======================================================================

请选择功能：

  1. 📸 分析餐食图片（一步完成全流程）
  2. 📈 查询历史记录
  3. 💡 获取下一餐推荐
  4. 🚪 退出

请输入数字（1-4）：
```

---

### 4. 分析餐食图片

选择选项 `1`，输入图片路径：

```bash
Image path: /path/to/your/meal_image.png
```

系统将自动执行以下步骤：

1. ✅ 根据时间自动推断餐次（早餐 / 午餐 / 晚餐 / 加餐）
2. ✅ Qwen-VL 识别所有菜品并估计分量
3. ✅ AI 校验分量合理性
4. ✅ 在线查询每道菜的营养数据
5. ✅ 计算整餐营养总量
6. ✅ 健康评分与建议
7. ✅ 结合历史数据进行趋势分析
8. ✅ 推荐下一餐食物
9. ✅ 自动保存至数据库

**示例输出**：

```
📋 分析报告：
----------------------------------------------------------------------
# 餐食分析报告

## 1. 菜品识别与分量估计
- **宫保鸡丁**：300g（大份），菜品在盘中堆叠较高，可见丰富的鸡肉、花生、胡萝卜等食材

## 2. 营养计算
- **总热量**：345 kcal
- **蛋白质**：25.5 g
- **脂肪**：18.6 g
- **碳水化合物**：21.9 g
- **钠**：960 mg

## 3. 健康评分与建议
- **评分**：75 分
- **建议**：
  - 热量适中
  - 蛋白质充足
  - 钠含量略高，建议下一餐选择低钠食物

## 4. 趋势分析
- **近期营养趋势**：最近 7 天平均 1850 kcal / 天，蛋白质摄入充足

## 5. 下一餐推荐
### 方案一：高蛋白低钠均衡餐
- **推荐菜品**：清蒸鸡胸肉、焯西兰花、糙米饭（小份）
- **原因**：补充膳食纤维，降低钠摄入

## 6. 数据保存
- **已成功保存餐食记录至 2025-12-08，餐次 ID：meal_2025-12-08_1**
----------------------------------------------------------------------
```

---

## 🛠️ 技术架构

### 核心技术栈

* **LangChain 1.0** —— Agent 框架
* **LangGraph** —— 工作流编排（`create_react_agent`）
* **Pydantic 2.12** —— 数据校验
* **Qwen-VL-Plus** —— 多模态视觉模型（图像识别）
* **Qwen-Plus** —— 文本推理模型（分量校验、营养查询）
* **OpenAI SDK** —— 与 DashScope API 兼容

---

### Agent 工作流

系统使用 **12 个工具** 协同工作，严格遵循以下顺序：

```
1. detect_dishes_and_portions(image_path)
   ↓ 返回 vision_result（JSON）
   
2. check_and_refine_portions(vision_result)
   ↓ 返回 portion_result（JSON）
   
3. add_nutrition_to_dishes(portion_result)  ← 🔴 关键步骤
   ↓ 返回 nutrition_result（JSON）
   
4. compute_meal_nutrition(nutrition_result)
   ↓ 返回 compute_result（JSON）
   
5. save_meal(compute_result)
   ↓ 保存至数据库
```

---

### 关键设计决策

#### 1. **JSON 字符串通信**

所有工具返回 JSON 字符串（而非 Python dict），因为 LangChain 会自动序列化复杂类型，可避免 `'str' object has no attribute 'get'` 错误。

#### 2. **在线营养查询**

不依赖本地营养数据库，而是使用 Qwen-Plus + Web Search 进行实时查询，确保数据最新、最全面。

#### 3. **智能餐次推断**

根据时间与历史数据自动判断餐次：

* 06:00–09:30 → 早餐
* 11:00–13:30 → 午餐
* 17:00–20:00 → 晚餐
* 其他时间 → 加餐（结合历史智能判断）

#### 4. **原子化数据库写入**

使用临时文件 + `os.replace()`，确保写入失败时不会造成数据丢失。

#### 5. **严格错误检查**

在关键步骤（营养计算、数据保存）加入 DEBUG 日志与异常抛出，避免静默失败。

---

## 📊 数据库结构

示例 `db/meals.json` 结构：

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

## 🧪 测试

项目包含完整测试套件：

```bash
# 测试完整工具链
python tests/test_complete_chain.py

# 测试数据库保存
python tests/test_save.py

# 校验数据库一致性
python tests/verify_db.py
```

**示例测试输出**：

```
======================================================================
🧪 测试完整工具链
======================================================================

1️⃣  模拟 vision_tools 返回值...
   ✅ vision_result 已就绪

2️⃣  调用 check_and_refine_portions...
   ✅ 分量校验完成：菜品数量 1，包含 final_weight_g

3️⃣  调用 add_nutrition_to_dishes...
   ✅ 营养补全完成：包含 nutrition_per_100g

4️⃣  调用 compute_meal_nutrition...
   ✅ 计算完成：总热量 345 kcal，蛋白质 25.5g

5️⃣  调用 save_meal...
   ✅ 保存完成：meal_2025-12-08_1

======================================================================
✅ 完整工具链测试通过！
======================================================================
```

---

## 🔧 常见问题（FAQ）

### Q1：错误提示 “DASHSCOPE_API_KEY not configured”

**解决方案**：

1. 确认项目根目录存在 `.env` 文件
2. 检查 API Key 格式是否正确
3. 重启终端或重新激活虚拟环境

---

### Q2：图像识别失败或返回空结果

**可能原因**：

* 不支持的图片格式（仅支持 jpg、png、webp）
* 图片过大（建议 < 5MB）
* API 配额不足

**解决方案**：

* 使用支持的图片格式
* 压缩图片大小
* 检查 DashScope 账户余额

---

### Q3：数据库文件为空

**原因**：程序在写入数据时发生错误，旧版本可能会清空文件。

**解决方案**：最新版本已修复，采用原子写入方式（临时文件 + replace）。若发现空文件，程序会自动初始化。

---

### Q4：所有营养数据为 0

**原因**：未调用 `add_nutrition_to_dishes` 工具。

**解决方案**：Agent 系统 Prompt 已明确要求调用该工具，以确保工具链完整。

---

## 🎯 路线图（Roadmap）

* [ ] 支持 GUI 界面（基于 Gradio / Streamlit）
* [ ] 多用户管理
* [ ] 自动餐食照片归档
* [ ] 导出健康报告（PDF / Excel）
* [ ] 微量营养素分析（维生素、矿物质）
* [ ] 运动消耗记录与推荐
* [ ] 数据可视化仪表盘

---

## 📄 许可证

本项目仅用于学习与研究目的。

---

## 🙏 致谢

* LangChain —— Agent 框架
* 阿里云通义千问（Qwen） —— 多模态 AI 模型
* Pydantic —— 数据校验

---

## 📧 联系方式

欢迎通过 Issues 提交问题或建议。

---

**最后更新时间**：2025-12-08
