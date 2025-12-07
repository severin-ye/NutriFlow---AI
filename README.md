# 🍽️ NutriFlow · AI - 智能营养分析系统

基于 **LangChain 1.0 + LangGraph** 构建的智能营养分析助手，使用阿里云通义千问 (Qwen) 多模态模型，实现餐盘图像识别、营养分析、健康评分和智能推荐。

---

## ✨ 功能特性

- 🔍 **智能图像识别** - 使用 Qwen-VL-Plus 多模态模型识别餐盘中的所有菜品
- ⚖️ **分量估算与验证** - AI 智能估算并验证每道菜的重量（小份/中份/大份）
- 🌐 **在线营养查询** - 实时联网查询最新营养数据，无需维护本地数据库
- 📊 **营养成分计算** - 精确计算五大营养素（热量、蛋白质、脂肪、碳水化合物、钠）
- 🎯 **健康评分** - 基于营养均衡度给出健康评分和个性化建议
- 📈 **饮食趋势分析** - 结合最近 7 天数据进行饮食模式和趋势评估
- 🕐 **智能餐型推断** - 根据时间戳和历史记录自动推断餐型（早餐/午餐/晚餐/夜宵）
- 💡 **下一餐推荐** - 基于饮食历史和营养缺口推荐下一餐食物
- 💾 **数据持久化** - 使用 JSON 数据库存储所有餐食记录

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
│   ├── tools/                      # 工具模块（12 个工具）
│   │   ├── __init__.py
│   │   ├── vision_tools.py         # 图像识别（Qwen-VL）
│   │   ├── portion_tools.py        # 分量验证与细化
│   │   ├── nutrition_tools.py      # 在线营养查询 + 批量添加
│   │   ├── compute_tools.py        # 营养计算与汇总
│   │   ├── db_tools.py             # 数据库读写
│   │   ├── meal_type_tools.py      # 餐型推断
│   │   └── recommendation_tools.py # 健康评分与推荐
│   │
│   ├── schemas/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── meal_schema.py          # 餐食数据结构（Pydantic）
│   │   └── tool_schema.py          # 工具输入输出结构
│   │
│   ├── prompts/                    # 提示词模板
│   │   ├── vision_prompt.txt       # 图像识别提示词
│   │   ├── portion_prompt.txt      # 分量验证提示词
│   │   ├── score_prompt.txt        # 健康评分提示词
│   │   ├── trend_prompt.txt        # 趋势分析提示词
│   │   ├── nextmeal_prompt.txt     # 下一餐推荐提示词
│   │   └── summary_prompt.txt      # 总结报告提示词
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
│   ├── test_save.py                # 数据库保存测试
│   └── verify_db.py                # 数据库验证脚本
│
└── doc/                            # 设计文档
    ├── 设计思路 联网版.md
    ├── 联网查询说明.md
    ├── 实现顺序.md
    └── langchain 1.0教程.md
```

---

## 🚀 快速开始

### 1. 环境准备

**系统要求**：
- Python 3.12+
- 阿里云 DashScope API Key（通义千问）

**安装依赖**：

```bash
# 克隆项目
cd /path/to/HCI

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

创建 `.env` 文件并添加你的阿里云 API Key：

```bash
# .env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

**获取 API Key**：
1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 开通通义千问服务
3. 获取 API Key

### 3. 运行程序

```bash
python main.py
```

**主菜单**：

```
======================================================================
                      🍽️  智能营养分析系统                             
               基于 LangChain 1.0 + 阿里通义千问                       
======================================================================

请选择功能:

  1. 📸 分析餐盘图片 (一键完成所有步骤)
  2. 📈 查询历史记录
  3. 💡 获取下一餐推荐
  4. 🚪 退出

请输入数字 (1-4):
```

### 4. 分析餐盘图片

选择功能 `1`，输入图片路径：

```bash
图片路径: /path/to/your/meal_image.png
```

系统将自动执行：
1. ✅ 根据时间自动推断餐型（早餐/午餐/晚餐/夜宵）
2. ✅ Qwen-VL 识别所有菜品并估算分量
3. ✅ AI 验证分量合理性
4. ✅ 在线查询每道菜的营养数据
5. ✅ 计算整餐营养总和
6. ✅ 健康评分与建议
7. ✅ 结合历史数据分析趋势
8. ✅ 推荐下一餐食物
9. ✅ 自动保存到数据库

**示例输出**：

```
📋 分析报告:
----------------------------------------------------------------------
# 餐食分析报告

## 1. 菜品识别与分量估算
- **宫保鸡丁**：300克（大份），菜品在盘中堆叠较高，可见鸡肉丁、花生、胡萝卜等配料丰富

## 2. 营养成分计算
- **总热量**: 345 千卡
- **蛋白质**: 25.5 克
- **脂肪**: 18.6 克
- **碳水化合物**: 21.9 克
- **钠**: 960 毫克

## 3. 健康评分与建议
- **评分**: 75 分
- **建议**:
  - 热量适中
  - 蛋白质充足
  - 钠含量略高，建议下一餐选择低钠食物

## 4. 趋势分析
- **近期营养趋势**: 最近7天平均热量 1850 kcal/天，蛋白质摄入充足

## 5. 推荐下一餐食物
### 推荐选项 1: 高蛋白低钠均衡餐
- **推荐菜品**: 清蒸鸡胸肉、水煮西兰花、糙米饭（小份）
- **理由**: 补充纤维素，降低钠摄入

## 6. 数据保存
- **成功保存餐食记录到 2025-12-08，餐食ID: meal_2025-12-08_1**
----------------------------------------------------------------------
```

---

## 🛠️ 技术架构

### 核心技术栈

- **LangChain 1.0** - Agent 框架
- **LangGraph** - 工作流编排（`create_react_agent`）
- **Pydantic 2.12** - 数据验证
- **Qwen-VL-Plus** - 多模态视觉模型（图像识别）
- **Qwen-Plus** - 文本推理模型（分量验证、营养查询）
- **OpenAI SDK** - 兼容 DashScope API

### Agent 工作流

系统使用 **12 个工具** 协同工作，严格按照以下顺序执行：

```
1. detect_dishes_and_portions(image_path)
   ↓ 返回 vision_result (JSON)
   
2. check_and_refine_portions(vision_result)
   ↓ 返回 portion_result (JSON)
   
3. add_nutrition_to_dishes(portion_result)  ← 🔴 关键步骤
   ↓ 返回 nutrition_result (JSON)
   
4. compute_meal_nutrition(nutrition_result)
   ↓ 返回 compute_result (JSON)
   
5. save_meal(compute_result)
   ↓ 保存到数据库
```

### 关键设计决策

#### 1. **JSON 字符串通信**
所有工具返回 JSON 字符串（而非 Python dict），因为 LangChain 会自动序列化复杂类型。这避免了 `'str' object has no attribute 'get'` 错误。

#### 2. **在线营养查询**
不依赖本地营养数据库，而是通过 Qwen-Plus + Web Search 实时查询，确保数据最新且覆盖面广。

#### 3. **智能餐型推断**
基于时间和历史记录自动推断餐型：
- 06:00-09:30 → 早餐
- 11:00-13:30 → 午餐
- 17:00-20:00 → 晚餐
- 其他时间 → 夜宵（结合历史数据智能判断）

#### 4. **原子性数据库写入**
使用临时文件 + `os.replace()` 确保写入失败时不会丢失原有数据。

#### 5. **严格错误检查**
在关键环节（营养计算、数据保存）添加 DEBUG 日志和异常抛出，避免静默失败。

---

## 📊 数据库结构

`db/meals.json` 结构示例：

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
              "name": "宫保鸡丁",
              "category": "荤菜",
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

项目包含完整的测试套件：

```bash
# 测试完整工具链
python tests/test_complete_chain.py

# 测试数据库保存
python tests/test_save.py

# 验证数据库一致性
python tests/verify_db.py
```

**测试输出示例**：

```
======================================================================
🧪 测试完整工具链
======================================================================

1️⃣  模拟 vision_tools 返回值...
   ✅ vision_result准备完成

2️⃣  调用 check_and_refine_portions...
   ✅ portion完成: 菜品数: 1, 有final_weight_g: True

3️⃣  调用 add_nutrition_to_dishes...
   ✅ nutrition完成: 有nutrition_per_100g: True

4️⃣  调用 compute_meal_nutrition...
   ✅ compute完成: 整餐总营养: 345 kcal, 25.5g protein

5️⃣  调用 save_meal...
   ✅ save完成: meal_2025-12-08_1

======================================================================
✅ 完整工具链测试通过！
======================================================================
```

---

## 🔧 常见问题

### Q1: 提示 "DASHSCOPE_API_KEY未配置"

**解决方案**：
1. 确保 `.env` 文件存在于项目根目录
2. 检查 API Key 格式是否正确
3. 重启终端或重新激活虚拟环境

### Q2: 图像识别失败或返回空结果

**原因**：
- 图片格式不支持（支持 jpg, png, webp）
- 图片过大（建议 < 5MB）
- API 配额不足

**解决方案**：
- 使用支持的图片格式
- 压缩图片大小
- 检查 DashScope 账户余额

### Q3: 数据库文件为空

**原因**：程序在写入数据时出错，但旧版本会清空文件。

**解决方案**：已在最新版本中修复，现在使用原子性写入（临时文件 + 替换）。如果遇到空文件，程序会自动重新初始化。

### Q4: 营养数据全是 0

**原因**：缺少 `add_nutrition_to_dishes` 工具调用。

**解决方案**：已在 Agent 系统提示词中明确要求调用此工具，确保工具链完整。

---

## 🎯 Roadmap

- [ ] 支持 GUI 界面（基于 Gradio/Streamlit）
- [ ] 多用户管理
- [ ] 餐食照片自动归档
- [ ] 导出健康报告（PDF/Excel）
- [ ] 微量元素分析（维生素、矿物质）
- [ ] 运动消耗记录与建议
- [ ] 数据可视化仪表板

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - Agent 框架
- [阿里云通义千问](https://www.aliyun.com/product/bailian) - 多模态 AI 模型
- [Pydantic](https://github.com/pydantic/pydantic) - 数据验证

---

## 📧 联系方式

如有问题或建议，欢迎提交 Issue。

---

**最后更新**: 2025-12-08
