#!/bin/bash

# NutriFlow AI - 一键启动脚本

echo "======================================================================="
echo "           🍽️  NutriFlow AI - 一键启动                               "
echo "======================================================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# PID 文件路径
PID_DIR="$PROJECT_ROOT/.pids"
mkdir -p "$PID_DIR"

AI_PID_FILE="$PID_DIR/ai_backend.pid"
API_PID_FILE="$PID_DIR/api_backend.pid"
FRONTEND_PID_FILE="$PID_DIR/frontend.pid"

echo ""
echo -e "${BLUE}📋 检查现有进程...${NC}"

# 检查是否有服务正在运行
if [ -f "$AI_PID_FILE" ] || [ -f "$API_PID_FILE" ] || [ -f "$FRONTEND_PID_FILE" ]; then
    echo -e "${YELLOW}⚠️  检测到服务可能正在运行${NC}"
    echo "请先运行 ./stop-all.sh 停止现有服务"
    exit 1
fi

# 检查端口占用
check_port() {
    lsof -i:$1 > /dev/null 2>&1
    return $?
}

if check_port 8000 || check_port 4000 || check_port 3000; then
    echo -e "${YELLOW}⚠️  检测到端口占用${NC}"
    if check_port 8000; then
        echo "  - 端口 8000 (AI Backend) 已被占用"
    fi
    if check_port 4000; then
        echo "  - 端口 4000 (API Backend) 已被占用"
    fi
    if check_port 3000; then
        echo "  - 端口 3000 (Frontend) 已被占用"
    fi
    echo ""
    read -p "是否终止这些进程并继续？(y/n): " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        lsof -ti:8000,4000,3000 | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✅ 已清理端口${NC}"
        sleep 2
    else
        echo "已取消启动"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}🚀 启动服务...${NC}"
echo ""

# 1. 启动 AI Backend (Python FastAPI)
echo -e "${BLUE}[1/3] 启动 AI Backend (端口 8000)...${NC}"
cd "$PROJECT_ROOT/nutrition_tracker_AI"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "  创建 Python 虚拟环境..."
    python3 -m venv .venv
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ 缺少 .env 文件！${NC}"
    echo "请在 nutrition_tracker_AI/.env 中配置 DASHSCOPE_API_KEY"
    exit 1
fi

# 使用绝对路径启动
PYTHON_BIN="$PROJECT_ROOT/nutrition_tracker_AI/.venv/bin/python"
UVICORN_BIN="$PROJECT_ROOT/nutrition_tracker_AI/.venv/bin/uvicorn"

# 如果 uvicorn 不存在，使用 python -m uvicorn
if [ ! -f "$UVICORN_BIN" ]; then
    nohup $PYTHON_BIN agent_server.py > "$PID_DIR/ai_backend.log" 2>&1 &
else
    nohup $UVICORN_BIN agent_server:app --host 0.0.0.0 --port 8000 > "$PID_DIR/ai_backend.log" 2>&1 &
fi

AI_PID=$!
echo $AI_PID > "$AI_PID_FILE"
echo -e "${GREEN}✅ AI Backend 已启动 (PID: $AI_PID)${NC}"

# 等待 AI Backend 启动并验证
sleep 6
if kill -0 $AI_PID 2>/dev/null && curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ AI Backend 运行正常${NC}"
else
    if ! kill -0 $AI_PID 2>/dev/null; then
        echo -e "${RED}❌ AI Backend 进程已退出！${NC}"
        echo "最后20行日志:"
        tail -20 "$PID_DIR/ai_backend.log"
        exit 1
    else
        echo -e "${YELLOW}⚠️  AI Backend 进程运行中，但端口 8000 未响应（可能仍在启动中）${NC}"
    fi
fi

# 2. 启动 API Backend (Node.js Express)
echo ""
echo -e "${BLUE}[2/3] 启动 API Backend (端口 4000)...${NC}"
cd "$PROJECT_ROOT/nutrition_tracker_backend"

if [ ! -d "node_modules" ]; then
    echo "  安装 npm 依赖..."
    npm install --silent
fi

nohup npm start > "$PID_DIR/api_backend.log" 2>&1 &
API_PID=$!
echo $API_PID > "$API_PID_FILE"
echo -e "${GREEN}✅ API Backend 已启动 (PID: $API_PID)${NC}"

# 等待 API Backend 启动
sleep 3
if ! kill -0 $API_PID 2>/dev/null; then
    echo -e "${RED}❌ API Backend 启动失败！${NC}"
    echo "查看日志: cat $PID_DIR/api_backend.log"
    kill $AI_PID 2>/dev/null
    rm -f "$AI_PID_FILE"
    exit 1
fi

# 3. 启动 Frontend (Next.js)
echo ""
echo -e "${BLUE}[3/3] 启动 Frontend (端口 3000)...${NC}"
cd "$PROJECT_ROOT/nutrition_tracker_frontend"

if [ ! -d "node_modules" ]; then
    echo "  安装 npm 依赖..."
    npm install --silent
fi

# 检查 .env.local 文件
if [ ! -f ".env.local" ]; then
    echo "  创建 .env.local 配置..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:4000" > .env.local
fi

nohup npm run dev > "$PID_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$FRONTEND_PID_FILE"
echo -e "${GREEN}✅ Frontend 已启动 (PID: $FRONTEND_PID)${NC}"

# 等待 Frontend 启动
sleep 5

echo ""
echo "======================================================================="
echo -e "${GREEN}✅ 所有服务启动完成！${NC}"
echo "======================================================================="
echo ""
echo "📊 服务状态:"
echo "  ┌─────────────────────────────────────────────────────────────┐"
echo "  │ 🤖 AI Backend    : http://localhost:8000  (PID: $AI_PID)    │"
echo "  │ 🔧 API Backend   : http://localhost:4000  (PID: $API_PID)   │"
echo "  │ 🌐 Frontend      : http://localhost:3000  (PID: $FRONTEND_PID) │"
echo "  └─────────────────────────────────────────────────────────────┘"
echo ""
echo "📝 日志文件:"
echo "  - AI Backend  : $PID_DIR/ai_backend.log"
echo "  - API Backend : $PID_DIR/api_backend.log"
echo "  - Frontend    : $PID_DIR/frontend.log"
echo ""
echo "🔍 查看日志: tail -f $PID_DIR/*.log"
echo "🛑 停止服务: ./stop-all.sh"
echo ""
echo "======================================================================="
echo -e "${BLUE}🎉 请在浏览器中访问: http://localhost:3000${NC}"
echo "======================================================================="
