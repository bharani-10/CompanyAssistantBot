# MetaMind OS - Localhost Access Guide

## 🚀 System Status: RUNNING ✅

Both backend and frontend servers are now running on your local machine!

---

## 📍 Access Points

### Frontend (Web Interface)
```
🌐 http://localhost:3000
```

**Features**:
- Project Center (view generated projects)
- Agent Theater (real-time agent logs)
- Mission Timeline (track progress)
- Results Display (view generated code)

### Backend API
```
🔌 http://localhost:8000
```

**Features**:
- RESTful API endpoints
- WebSocket support
- Real-time mission tracking
- File management

### API Documentation
```
📚 http://localhost:8000/docs
```

Interactive API documentation (Swagger UI)

---

## 🧪 Quick Test Commands

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "swarm_agents": 8,
  "autonomous_mode": true,
  "projects_generated": 0
}
```

### 2. Root Endpoint
```bash
curl http://localhost:8000/
```

**Expected Response**:
```json
{
  "message": "MetaMind Autonomous AI Software Engineering OS",
  "status": "operational",
  "version": "1.0.0",
  "capabilities": [...]
}
```

### 3. List Projects
```bash
curl http://localhost:8000/projects
```

**Expected Response**:
```json
{
  "projects": [],
  "total_projects": 0,
  "validation": "real_filesystem_counts"
}
```

---

## 📊 System Information

### Backend Server
- **Status**: ✅ Running
- **URL**: http://localhost:8000
- **Port**: 8000
- **Framework**: FastAPI
- **Agents**: 8 (Analyst, Architect, Engineer, Executor, Debugger, Evaluator, DevOps, GitHub, Recovery)
- **LLM**: Groq (llama-3.1-8b-instant)

### Frontend Server
- **Status**: ✅ Running
- **URL**: http://localhost:3000
- **Port**: 3000
- **Framework**: React + TypeScript + Vite
- **Features**: Real-time updates, WebSocket support

---

## 🎯 Next Steps

### 1. Open Web Interface
Click here or open in browser:
```
http://localhost:3000
```

### 2. Create Sample Dataset
```python
import pandas as pd
import numpy as np

# Create sample classification dataset
data = {
    'feature_1': np.random.randn(100),
    'feature_2': np.random.randn(100),
    'feature_3': np.random.choice(['A', 'B', 'C'], 100),
    'target': np.random.randint(0, 2, 100)
}

df = pd.DataFrame(data)
df.to_csv('sample_dataset.csv', index=False)
print("Sample dataset created: sample_dataset.csv")
```

### 3. Upload Dataset
Use the web interface to upload your dataset

### 4. Start Generation
Click "Generate Project" and watch the autonomous swarm work!

### 5. Monitor Progress
- Watch real-time logs in Agent Theater
- Track progress in Mission Timeline
- View file counts in Project Center

### 6. Download Project
Once complete, download the generated project as ZIP

---

## 🔗 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/health` | GET | Health check |
| `/upload` | POST | Upload dataset |
| `/generate-complete-project` | POST | Start generation |
| `/mission-status/{mission_id}` | GET | Get mission status |
| `/mission-logs/{mission_id}` | GET | Get mission logs |
| `/projects` | GET | List projects |
| `/projects/{project_id}/files` | GET | Get file structure |
| `/projects/{project_id}/file/{file_path}` | GET | Get file content |
| `/projects/{project_id}/download` | GET | Download project |
| `/ws` | WS | WebSocket updates |

---

## 📝 Example Workflow

### Step 1: Upload Dataset
```bash
curl -X POST -F "file=@sample_dataset.csv" http://localhost:8000/upload
```

### Step 2: Start Generation
```bash
curl -X POST "http://localhost:8000/generate-complete-project?dataset_path=uploads/sample_dataset.csv&user_prompt=Build%20a%20binary%20classification%20model"
```

**Response**:
```json
{
  "mission_id": "mission_20260506_223631",
  "status": "running",
  "message": "Real autonomous generation started",
  "endpoints": {
    "status": "/mission-status/mission_20260506_223631",
    "logs": "/mission-logs/mission_20260506_223631"
  }
}
```

### Step 3: Check Status
```bash
curl http://localhost:8000/mission-status/mission_20260506_223631
```

### Step 4: Get Logs
```bash
curl http://localhost:8000/mission-logs/mission_20260506_223631
```

### Step 5: Download Project
```bash
curl -O http://localhost:8000/projects/mission_20260506_223631/download
```

---

## 🛠️ Troubleshooting

### Issue: Cannot connect to localhost:3000

**Solution**:
1. Check if frontend is running: `npm run dev` in frontend directory
2. Try accessing http://localhost:5173 (Vite default port)
3. Check browser console for errors

### Issue: Cannot connect to localhost:8000

**Solution**:
1. Check if backend is running: `python -m uvicorn app.main:app --reload`
2. Check if port 8000 is in use: `netstat -ano | findstr :8000`
3. Try different port: `python -m uvicorn app.main:app --port 8001`

### Issue: API returns 404

**Solution**:
1. Verify backend is running
2. Check endpoint URL spelling
3. Ensure dataset path is correct
4. Check mission ID is valid

### Issue: Generation fails

**Solution**:
1. Check mission logs: `/mission-logs/{mission_id}`
2. Verify dataset format (CSV)
3. Check dataset has target column
4. Review error messages in logs

---

## 📊 Real-Time Monitoring

### Watch Mission Progress
```bash
# In a loop, check mission status
while true; do
  curl -s http://localhost:8000/mission-status/mission_20260506_223631 | jq '.progress'
  sleep 2
done
```

### Monitor Agent Logs
```bash
# Get latest logs
curl -s http://localhost:8000/mission-logs/mission_20260506_223631 | jq '.logs[-5:]'
```

### Track File Generation
```bash
# Check real file counts
curl -s http://localhost:8000/mission-status/mission_20260506_223631 | jq '.file_counts'
```

---

## 🎓 Learning Resources

### Documentation
- `README_PRODUCTION.md` - Project overview
- `QUICK_START_PRODUCTION.md` - Quick start guide
- `API_DOCUMENTATION.md` - Complete API reference
- `PRODUCTION_RELIABILITY_GUIDE.md` - Reliability guide

### Testing
- `test_core_recovery.py` - Core recovery tests
- `test_production_system.py` - Full production tests

### Examples
- See API_DOCUMENTATION.md for complete examples
- Check QUICK_START_PRODUCTION.md for workflows

---

## 🚀 Performance Tips

### For Faster Generation
1. Use fast mode (no LLM): Set `GROQ_API_KEY` to empty
2. Smaller datasets: <1000 rows for quick testing
3. Simple problem types: Classification is faster than regression

### For Better Results
1. Use LLM: Set `GROQ_API_KEY` for better architecture
2. Larger datasets: >1000 rows for better model training
3. Clear prompts: Specific user requirements

---

## 📞 Support

### Quick Help
1. Check health: `curl http://localhost:8000/health`
2. View logs: `curl http://localhost:8000/mission-logs/{mission_id}`
3. List projects: `curl http://localhost:8000/projects`

### Documentation
- See `PRODUCTION_RELIABILITY_GUIDE.md` for detailed guide
- See `API_DOCUMENTATION.md` for API reference
- See `QUICK_START_PRODUCTION.md` for troubleshooting

---

## ✅ Verification Checklist

- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Health check responding
- ✅ API endpoints accessible
- ✅ WebSocket support enabled
- ✅ Real-time updates working
- ✅ Mission tracking operational
- ✅ File operations functional

---

## 🎉 You're All Set!

MetaMind OS is now running on your local machine!

**Next**: Open http://localhost:3000 in your browser and start generating projects! 🚀

---

**MetaMind OS v1.0.0 - Running on Localhost**  
**Backend**: http://localhost:8000 ✅  
**Frontend**: http://localhost:3000 ✅  
**Status**: OPERATIONAL 🟢
