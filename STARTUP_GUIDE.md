# 🚀 Dashboard Startup Guide - Automated Launch

## ⚡ **ONE-COMMAND STARTUP**

Choose your preferred method:

### **Method 1: Python Script** (Recommended - All Platforms)
```bash
python start_dashboard.py
```

### **Method 2: Windows Batch File**
```cmd
start_dashboard.bat
```

### **Method 3: Unix Shell Script**
```bash
chmod +x start_dashboard.sh
./start_dashboard.sh
```

### **Method 4: NPM Script**
```bash
npm start
```

---

## 🎯 **What Happens Automatically**

When you run any startup command:

✅ **Pre-flight Checks:**
- Python version (3.9+)
- Node.js installation
- npm availability
- Backend dependencies
- Frontend dependencies
- Dataset file presence

✅ **Backend Startup:**
- Starts FastAPI server on `http://localhost:8000`
- Enables auto-reload for development
- Opens API documentation at `/docs`

✅ **Frontend Startup:**
- Installs npm packages (if needed)
- Starts React dev server on `http://localhost:3000`
- Enables hot module replacement (HMR)

✅ **Success Message:**
```
╔════════════════════════════════════════════════════════════════╗
║              ✅ DASHBOARD STARTED SUCCESSFULLY! ✅              ║
╚════════════════════════════════════════════════════════════════╝

🌐 Access Points:
   📊 Dashboard:     http://localhost:3000
   🔌 Backend API:   http://localhost:8000
   📖 API Docs:      http://localhost:8000/docs
```

---

## 📋 **Startup Scripts Comparison**

| Script | Platform | Features | Best For |
|--------|----------|----------|----------|
| `start_dashboard.py` | All | ✅ Checks<br>✅ Error handling<br>✅ Auto-install | **Recommended** |
| `start_dashboard.bat` | Windows | ✅ Native<br>✅ New windows | Windows users |
| `start_dashboard.sh` | Unix | ✅ Native<br>✅ Color output | Mac/Linux |
| `npm start` | All | ✅ Simple | npm users |

---

## 🔧 **Detailed: Python Script** (`start_dashboard.py`)

### **Features:**
- ✅ Pre-flight system checks
- ✅ Automatic dependency installation
- ✅ Error detection and reporting
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Process monitoring
- ✅ Beautiful terminal output

### **Run:**
```bash
python start_dashboard.py
```

### **Output:**
```
╔════════════════════════════════════════════════════════════════╗
║        🚀 FRAUD DETECTION DASHBOARD - AUTO STARTUP 🚀          ║
╚════════════════════════════════════════════════════════════════╝

🔍 Pre-flight Checks...

✅ Python 3.11.0
✅ Node.js v18.17.0
✅ npm 9.6.7
✅ Backend dependencies installed
✅ Frontend dependencies installed
✅ Dataset found (204.3 MB)

✅ All pre-flight checks passed!

============================================================
🔧 Starting Backend API Server...
============================================================
⏳ Waiting for backend to start...
✅ Backend API started successfully
   📍 API: http://localhost:8000
   📖 Docs: http://localhost:8000/docs

============================================================
🎨 Starting Frontend React App...
============================================================
⏳ Waiting for frontend to start...
✅ Frontend app started successfully
   📍 Dashboard: http://localhost:3000
```

### **Stop:**
Press `Ctrl+C` - Both servers stop automatically

---

## 🪟 **Windows: Batch File** (`start_dashboard.bat`)

### **Features:**
- ✅ Opens 2 separate command windows
- ✅ Native Windows experience
- ✅ Easy to customize

### **Run:**
Double-click `start_dashboard.bat` or:
```cmd
start_dashboard.bat
```

### **What Opens:**
1. **Window 1**: Backend API Server
2. **Window 2**: Frontend React Dev Server

### **Stop:**
Close both command windows

---

## 🐧 **Unix: Shell Script** (`start_dashboard.sh`)

### **Features:**
- ✅ Color-coded output
- ✅ Process management
- ✅ Graceful shutdown
- ✅ Background processes

### **Setup** (one-time):
```bash
chmod +x start_dashboard.sh
```

### **Run:**
```bash
./start_dashboard.sh
```

### **Stop:**
Press `Ctrl+C` - Both servers stop automatically

---

## 📦 **NPM Scripts** (`package.json`)

### **Available Commands:**

```bash
# Start full dashboard (runs Python script)
npm start

# Start backend only
npm run start:backend

# Start frontend only
npm run start:frontend

# Install frontend dependencies
npm run install:frontend

# Build frontend for production
npm run build:frontend

# Test backend API
npm run test:backend

# Setup everything
npm run setup
```

### **Example:**
```bash
# Complete setup from scratch
npm run setup

# Start dashboard
npm start
```

---

## 🛠️ **First-Time Setup**

### **Option 1: Automated Setup**
```bash
# Install everything automatically
npm run setup

# Start dashboard
python start_dashboard.py
```

### **Option 2: Manual Setup**
```bash
# 1. Install backend dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies
cd frontend
npm install
cd ..

# 3. Start dashboard
python start_dashboard.py
```

---

## ⚙️ **Configuration**

### **Change Ports**

**Backend** (edit `backend/config.py`):
```python
# Change API port
API_PORT = 8000
```

**Frontend** (edit `frontend/vite.config.js`):
```javascript
server: {
  port: 3000,  // Change frontend port
}
```

### **Environment Variables**

Create `frontend/.env`:
```bash
VITE_API_URL=http://localhost:8000
```

---

## 🐛 **Troubleshooting**

### **Problem: "Port already in use"**

**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Unix
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000):**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Unix
lsof -ti:3000 | xargs kill -9
```

### **Problem: "Module not found"**

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### **Problem: "Dataset not found"**
- Ensure `financial_fraud_detection_dataset.csv` is in project root
- Check file name spelling

### **Problem: Script won't run**

**Unix:**
```bash
chmod +x start_dashboard.sh
```

**Windows:**
- Right-click → "Run as Administrator"

---

## 🎯 **Development Workflow**

### **Daily Development:**
```bash
# Morning: Start dashboard
python start_dashboard.py

# Develop...
# Backend auto-reloads on code changes
# Frontend has HMR (instant updates)

# Evening: Stop dashboard
# Press Ctrl+C
```

### **Testing:**
```bash
# Test backend API
python test_api.py

# Or
npm run test:backend
```

### **Production Build:**
```bash
# Build frontend
npm run build:frontend

# Deploy dist/ folder
```

---

## 📊 **What You'll See**

### **Backend Console:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **Frontend Console:**
```
  VITE v5.0.8  ready in 523 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### **Browser:**
Open `http://localhost:3000` to see:
- ✅ Executive Overview (5 KPIs)
- ✅ High-Risk Transactions
- ✅ Fraud Velocity Heatmap
- ✅ Fraud Type Breakdown
- ✅ Financial Impact
- ✅ Model Health

---

## 🚀 **Quick Reference**

| Task | Command |
|------|---------|
| **Start Everything** | `python start_dashboard.py` |
| **Start Backend Only** | `npm run start:backend` |
| **Start Frontend Only** | `npm run start:frontend` |
| **Stop Everything** | `Ctrl+C` |
| **Setup from Scratch** | `npm run setup` |
| **Test API** | `python test_api.py` |
| **Build Production** | `npm run build:frontend` |

---

## 💡 **Pro Tips**

1. **Use Python script** - Most reliable, cross-platform
2. **Check health** - Visit `http://localhost:8000/health`
3. **API docs** - Explore `http://localhost:8000/docs`
4. **Auto-reload** - Both servers reload on code changes
5. **Git ignore** - Dataset is ignored (too large for git)

---

## 📞 **Need Help?**

- **Backend Issues**: Check `backend/` console
- **Frontend Issues**: Check `frontend/` console
- **API Errors**: Visit `/docs` for testing
- **Port Conflicts**: Change ports in configs

---

## 🎉 **Success Checklist**

After running startup script, verify:

- [ ] ✅ No errors in terminal
- [ ] ✅ Backend at `http://localhost:8000`
- [ ] ✅ Frontend at `http://localhost:3000`
- [ ] ✅ Health check returns "healthy"
- [ ] ✅ Dashboard loads in browser
- [ ] ✅ Data displays correctly

---

## 👨‍💻 **Author**

**Masood Nazari**  
Business Intelligence Analyst | Data Science | AI | Clinical Research

📧 M.Nazari@soton.ac.uk  
🌐 https://michaeltheanalyst.github.io/  
💼 linkedin.com/in/masood-nazari  
🔗 github.com/michaeltheanalyst

---

**Now start your dashboard with ONE command!** 🚀

```bash
python start_dashboard.py
```

