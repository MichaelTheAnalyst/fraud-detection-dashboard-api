#!/bin/bash
################################################################################
#  Fraud Detection Dashboard - Unix Startup Script
#  
#  Starts both backend API and frontend React app
#  
#  Author: Masood Nazari
#  GitHub: github.com/michaeltheanalyst
################################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║        🚀 FRAUD DETECTION DASHBOARD - AUTO STARTUP 🚀          ║"
echo "║                                                                ║"
echo "║  Starting Backend + Frontend...                                ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found!${NC}"
    echo "   Please install Python 3.9+"
    exit 1
fi
echo -e "${GREEN}✅ Python found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found!${NC}"
    echo "   Please install Node.js from nodejs.org"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm found${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}⏹️  Shutting down dashboard...${NC}"
    echo "   Stopping backend..."
    kill $BACKEND_PID 2>/dev/null
    echo "   Stopping frontend..."
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Dashboard stopped successfully${NC}"
    echo "👋 Goodbye!"
    exit 0
}

# Trap CTRL+C
trap cleanup INT TERM

# Start Backend
echo -e "${BLUE}🔧 Starting Backend API Server...${NC}"
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 3

# Check if backend started
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend failed to start${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Start Frontend
echo -e "${BLUE}🎨 Starting Frontend React App...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..
sleep 5

# Check if frontend started
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Frontend failed to start${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

# Print success message
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║              ✅ DASHBOARD STARTED SUCCESSFULLY! ✅              ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access Points:"
echo ""
echo "   📊 Dashboard:     http://localhost:3000"
echo "   🔌 Backend API:   http://localhost:8000"
echo "   📖 API Docs:      http://localhost:8000/docs"
echo "   💚 Health Check:  http://localhost:8000/health"
echo ""
echo "⌨️  Commands:"
echo ""
echo "   Press Ctrl+C to stop both servers"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Keep script running
wait

