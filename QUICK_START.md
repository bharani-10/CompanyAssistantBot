# 🚀 MetaMind OS - Quick Start Guide

**Autonomous AI Software Engineering System - Fast Setup**

## ⚡ Super Fast Start (30 seconds)

### Option 1: Windows
```bash
# Double-click or run:
start_fast.bat
```

### Option 2: Python (Cross-platform)
```bash
python quick_start.py
```

### Option 3: Manual (if above fails)
```bash
cd backend
pip install fastapi uvicorn pandas numpy scikit-learn python-multipart
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🧪 Test the System (Optional)
```bash
python test_fast.py
```

## 🎯 Quick Demo

1. **Open your browser**: http://localhost:8000/docs
2. **Upload a CSV file** using the `/upload` endpoint
3. **Generate a complete ML app** using `/generate-complete-project`
   - dataset_path: `uploads/your_file.csv`
   - user_prompt: `"Build a prediction system for my data"`

## ⚡ What You Get (in seconds!)

- ✅ **Complete FastAPI Backend** with ML endpoints
- ✅ **React Frontend** with prediction interface  
- ✅ **ML Training Pipeline** with auto-model selection
- ✅ **Docker Deployment** configs
- ✅ **GitHub Repository** structure
- ✅ **Production-ready** code

## 🔧 System URLs

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend** (if available): http://localhost:3000

## 📊 Example Test

Try with the included student performance dataset:

```json
{
  "dataset_path": "data/students_performance.csv",
  "user_prompt": "Build a complete student performance prediction system with modern web interface and deployment configuration"
}
```

## 🚀 Features

- **⚡ FAST MODE**: Generates complete apps in seconds
- **🤖 8-Agent Swarm**: Autonomous software engineering
- **📁 Real Files**: Creates actual project structure
- **🐳 Deploy Ready**: Docker, Hugging Face, Railway configs
- **📚 Full Documentation**: README, API docs, guides

## 🛠️ Troubleshooting

**Backend won't start?**
```bash
pip install --upgrade pip
pip install fastapi uvicorn pandas numpy scikit-learn
```

**Port 8000 busy?**
- Change port in `backend/app/main.py` line: `uvicorn.run(app, port=8001)`

**Need help?**
- Check the generated project's README.md
- Look at API docs: http://localhost:8000/docs

---

**🤖 This is an autonomous AI software engineering system. No manual coding required!**