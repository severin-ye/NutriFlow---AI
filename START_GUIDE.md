# 🚀 NutriFlow AI - Quick Start Guide

## 快速启动指南

根据你的需求选择启动方式：

---

## 方式 1️⃣: AI Backend CLI (最简单，推荐新手)

适合：快速测试 AI 功能，无需前端界面

```bash
# 1. 进入 AI 后端目录
cd /home/severin/Codelib/HCI/nutrition_tracker_AI

# 2. 激活虚拟环境
source .venv/bin/activate

# 3. 确认已配置 API Key
cat .env  # 应该看到 DASHSCOPE_API_KEY=sk-xxx...

# 4. 运行主程序
python main.py
```

**使用说明**:
- 选择功能 1: 分析餐盘图片
- 输入图片路径 (可以拖拽图片到终端)
- 系统自动完成识别、营养分析、健康评分、推荐等
- 数据自动保存到 `ai_nutrition_agent/db/meals.json`

---

## 方式 2️⃣: 完整全栈系统 (需要三个终端)

适合：完整体验前端界面 + API + AI

### 终端 1: 启动 AI Backend API Server

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
source .venv/bin/activate
python agent_server.py
```

**预期输出**:
```
* Running on http://127.0.0.1:8000
AI Agent Server started successfully!
```

### 终端 2: 启动 API Backend (Node.js)

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_backend
npm start
```

**预期输出**:
```
Server running on port 5000
```

### 终端 3: 启动 Frontend (React)

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_frontend
npm run dev
```

**预期输出**:
```
- Local:   http://localhost:3000
```

### 访问应用

打开浏览器访问: `http://localhost:3000`

---

## 方式 3️⃣: 只测试 AI Backend (适合开发调试)

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
source .venv/bin/activate

# 运行完整工具链测试
python tests/test_complete_chain.py

# 验证数据库
python tests/verify_db.py
```

---

## ⚙️ 首次启动前的准备

### 1. 检查 Python 虚拟环境

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI

# 如果 .venv 不存在，创建它
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI

# 检查 .env 文件是否存在
ls -la .env

# 如果不存在，创建它
echo "DASHSCOPE_API_KEY=sk-your_api_key_here" > .env

# 编辑填入真实的 API Key
nano .env  # 或使用 vim/code 等编辑器
```

### 3. 检查 Node.js 依赖 (如果要运行全栈)

```bash
# API Backend
cd /home/severin/Codelib/HCI/nutrition_tracker_backend
npm install

# Frontend
cd /home/severin/Codelib/HCI/nutrition_tracker_frontend
npm install
```

---

## 🧪 快速测试

使用示例图片测试系统：

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
source .venv/bin/activate

# 如果你有图片 image.png 在项目根目录
python -c "
from ai_nutrition_agent.agent import NutritionAgent
agent = NutritionAgent()
result = agent.analyze_meal('/home/severin/Codelib/HCI/image.png', '午餐')
print('分析完成！')
"
```

---

## 📊 检查系统状态

### 查看数据库

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI

# 查看数据库内容
cat ai_nutrition_agent/db/meals.json | python -m json.tool

# 或使用验证脚本
python tests/verify_db.py
```

### 查看日志

```bash
# 如果有日志文件
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
tail -f log.txt  # 实时查看日志
```

---

## ❌ 常见启动问题

### 问题 1: "DASHSCOPE_API_KEY未配置"

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
echo "DASHSCOPE_API_KEY=sk-your_key" > .env
```

### 问题 2: "ModuleNotFoundError"

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
source .venv/bin/activate
pip install -r requirements.txt
```

### 问题 3: 端口被占用

```bash
# 查看端口占用
lsof -i :8000  # AI Backend
lsof -i :5000  # API Backend
lsof -i :3000  # Frontend

# 杀死进程
kill -9 <PID>
```

### 问题 4: 数据库文件不存在

```bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
mkdir -p ai_nutrition_agent/db
echo '{"user_id": "user001", "days": []}' > ai_nutrition_agent/db/meals.json
```

---

## 💡 推荐的启动流程 (新用户)

1. **第一次使用** - 使用方式 1️⃣ (CLI)
   ```bash
   cd nutrition_tracker_AI
   source .venv/bin/activate
   python main.py
   ```

2. **测试成功后** - 尝试方式 2️⃣ (全栈)
   ```bash
   # 三个终端分别启动三个服务
   # 然后访问 http://localhost:3000
   ```

3. **开发调试** - 使用方式 3️⃣ (测试)
   ```bash
   python tests/test_complete_chain.py
   ```

---

## 📝 快捷启动脚本

你可以创建一个启动脚本：

```bash
# 创建 start.sh
cat > /home/severin/Codelib/HCI/start_ai.sh << 'SCRIPT'
#!/bin/bash
cd /home/severin/Codelib/HCI/nutrition_tracker_AI
source .venv/bin/activate
python main.py
SCRIPT

# 添加执行权限
chmod +x /home/severin/Codelib/HCI/start_ai.sh

# 使用
./start_ai.sh
```

---

## 🎯 下一步

启动成功后：

1. ✅ 拍一张餐食照片或使用测试图片
2. ✅ 通过 CLI 或网页上传分析
3. ✅ 查看营养数据和健康评分
4. ✅ 获取下一餐推荐
5. ✅ 查看历史记录和趋势

---

**有问题？** 查看 `README.md` 的故障排除部分或提交 Issue

**最后更新**: 2025-12-09
