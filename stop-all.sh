#!/bin/bash

# NutriFlow AI - 一键终止脚本

echo "======================================================================="
echo "           🍽️  NutriFlow AI - 一键终止                               "
echo "======================================================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$PROJECT_ROOT/.pids"

echo ""
echo -e "${BLUE}🛑 正在停止所有服务...${NC}"
echo ""

STOPPED_COUNT=0
FAILED_COUNT=0

# 停止 Frontend
if [ -f "$PID_DIR/frontend.pid" ]; then
    FRONTEND_PID=$(cat "$PID_DIR/frontend.pid")
    echo -e "${YELLOW}[1/3] 停止 Frontend (PID: $FRONTEND_PID)...${NC}"
    
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID 2>/dev/null
        sleep 2
        
        # 如果进程还在运行，强制终止
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
        
        echo -e "${GREEN}✅ Frontend 已停止${NC}"
        ((STOPPED_COUNT++))
    else
        echo -e "${YELLOW}⚠️  Frontend 进程不存在${NC}"
    fi
    
    rm -f "$PID_DIR/frontend.pid"
else
    echo -e "${YELLOW}[1/3] Frontend 未运行${NC}"
fi

# 停止 API Backend
if [ -f "$PID_DIR/api_backend.pid" ]; then
    API_PID=$(cat "$PID_DIR/api_backend.pid")
    echo -e "${YELLOW}[2/3] 停止 API Backend (PID: $API_PID)...${NC}"
    
    if kill -0 $API_PID 2>/dev/null; then
        kill $API_PID 2>/dev/null
        sleep 2
        
        if kill -0 $API_PID 2>/dev/null; then
            kill -9 $API_PID 2>/dev/null
        fi
        
        echo -e "${GREEN}✅ API Backend 已停止${NC}"
        ((STOPPED_COUNT++))
    else
        echo -e "${YELLOW}⚠️  API Backend 进程不存在${NC}"
    fi
    
    rm -f "$PID_DIR/api_backend.pid"
else
    echo -e "${YELLOW}[2/3] API Backend 未运行${NC}"
fi

# 停止 AI Backend
if [ -f "$PID_DIR/ai_backend.pid" ]; then
    AI_PID=$(cat "$PID_DIR/ai_backend.pid")
    echo -e "${YELLOW}[3/3] 停止 AI Backend (PID: $AI_PID)...${NC}"
    
    if kill -0 $AI_PID 2>/dev/null; then
        kill $AI_PID 2>/dev/null
        sleep 2
        
        if kill -0 $AI_PID 2>/dev/null; then
            kill -9 $AI_PID 2>/dev/null
        fi
        
        echo -e "${GREEN}✅ AI Backend 已停止${NC}"
        ((STOPPED_COUNT++))
    else
        echo -e "${YELLOW}⚠️  AI Backend 进程不存在${NC}"
    fi
    
    rm -f "$PID_DIR/ai_backend.pid"
else
    echo -e "${YELLOW}[3/3] AI Backend 未运行${NC}"
fi

# 额外清理：通过端口查找并终止进程
echo ""
echo -e "${BLUE}🧹 清理残留进程...${NC}"

# 清理端口 3000 (Frontend)
if lsof -ti:3000 > /dev/null 2>&1; then
    echo "  终止端口 3000 上的进程..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
fi

# 清理端口 4000 (API Backend)
if lsof -ti:4000 > /dev/null 2>&1; then
    echo "  终止端口 4000 上的进程..."
    lsof -ti:4000 | xargs kill -9 2>/dev/null
fi

# 清理端口 8000 (AI Backend)
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "  终止端口 8000 上的进程..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

# 清理 next dev 和 node server.js 进程
pkill -f "next dev" 2>/dev/null
pkill -f "node server.js" 2>/dev/null
pkill -f "agent_server.py" 2>/dev/null

echo ""
echo "======================================================================="

if [ $STOPPED_COUNT -gt 0 ]; then
    echo -e "${GREEN}✅ 成功停止 $STOPPED_COUNT 个服务${NC}"
else
    echo -e "${YELLOW}⚠️  没有运行中的服务${NC}"
fi

echo "======================================================================="
echo ""
echo "📝 日志文件保留在: $PID_DIR/"
echo "🗑️  清理日志: rm -rf $PID_DIR/*.log"
echo "🚀 重新启动: ./start-all.sh"
echo ""
