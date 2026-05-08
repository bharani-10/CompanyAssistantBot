# MetaMind OS - Quick Start Guide (Production-Ready)

## Prerequisites

- Python 3.8+
- Node.js 16+
- pip and npm
- Git

## Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key Dependencies**:
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Pydantic 2.5.0
- Pandas 2.1.3
- Scikit-learn 1.3.2
- LangChain (for LLM integration)
- Groq/Google Generative AI (optional)

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Set Environment Variables

Create `.env` file in backend directory:

```bash
# Optional: LLM API Keys (for enhanced architecture generation)
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key

# Upload directory
UPLOAD_DIR=uploads

# Database
DATABASE_URL=sqlite:///./metamind.db
```

## Running the System

### Option 1: Development Mode (Recommended for Testing)

#### Terminal 1: Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

#### Terminal 2: Start Frontend Development Server

```bash
cd frontend
npm run dev
```

**Output**:
```
  VITE v5.0.0  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

#### Terminal 3: Access the Application

Open browser to: `http://localhost:5173`

### Option 2: Production Mode (Docker)

#### Build Docker Image

```bash
docker build -t metamind-os:latest .
```

#### Run Docker Container

```bash
docker run -p 8000:8000 -p 5173:5173 \
  -e GROQ_API_KEY=your_key \
  -v $(pwd)/uploads:/app/uploads \
  metamind-os:latest
```

## Testing the System

### 1. Run Core Recovery Tests

```bash
python test_core_recovery.py
```

**Expected Output**:
```
✅ PASS - JSON Repair
✅ PASS - Missing Fields Repair
✅ PASS - Safe Model Parsing
✅ PASS - Fallback Model Creation
✅ PASS - Safe Fallback Method

Total: 5/5 tests passed
✨ All core recovery tests passed!
```

### 2. Test API Endpoints

#### Health Check

```bash
curl http://localhost:8000/health
```

**Response**:
```json
{
  "status": "healthy",
  "swarm_agents": 8,
  "autonomous_mode": true,
  "projects_generated": 0
}
```

#### Generate Project

```bash
# 1. Upload dataset
curl -X POST -F "file=@your_dataset.csv" http://localhost:8000/upload

# 2. Start autonomous generation
curl -X POST "http://localhost:8000/generate-complete-project?dataset_path=uploads/your_dataset.csv&user_prompt=Build%20a%20classification%20model"

# Response:
# {
#   "mission_id": "mission_20260506_203424",
#   "status": "running",
#   "message": "Real autonomous generation started",
#   "endpoints": {
#     "status": "/mission-status/mission_20260506_203424",
#     "logs": "/mission-logs/mission_20260506_203424"
#   }
# }

# 3. Check mission status
curl http://localhost:8000/mission-status/mission_20260506_203424

# 4. Get mission logs
curl http://localhost:8000/mission-logs/mission_20260506_203424

# 5. List all projects
curl http://localhost:8000/projects
```

### 3. Test with Sample Dataset

#### Create Sample Dataset

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

#### Upload and Generate

```bash
# Upload
curl -X POST -F "file=@sample_dataset.csv" http://localhost:8000/upload

# Generate
curl -X POST "http://localhost:8000/generate-complete-project?dataset_path=uploads/sample_dataset.csv&user_prompt=Build%20a%20binary%20classification%20model%20to%20predict%20the%20target%20column"

# Monitor progress
curl http://localhost:8000/mission-status/mission_20260506_203424
```

## Web Interface

### Dashboard Features

1. **Project Center**
   - View all generated projects
   - Real file counts from filesystem
   - Project health status
   - Download projects as ZIP

2. **Agent Theater**
   - Real-time agent logs
   - Recovery protocol visualization
   - Phase tracking
   - Error recovery display

3. **Mission Timeline**
   - Real-time progress tracking
   - Phase transitions
   - Component status
   - File generation progress

4. **Results Display**
   - Generated project structure
   - File listings
   - Code preview
   - Deployment instructions

## Troubleshooting

### Issue: "database_schema Field required" Error

**Status**: ✅ FIXED in Production Release

The system now uses fault-tolerant Pydantic models with automatic recovery.

**What happens**:
1. LLM generates incomplete JSON
2. Schema recovery engine detects missing fields
3. Automatically injects default values
4. Continues generation without crash

### Issue: Backend Dependencies Installation Fails

**Solution**:
```bash
# Clear pip cache
pip cache purge

# Reinstall with verbose output
pip install -r requirements.txt -v

# Or use specific Python version
python3.11 -m pip install -r requirements.txt
```

### Issue: Frontend Build Fails

**Solution**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Or use specific Node version
nvm use 18
npm install
```

### Issue: Port Already in Use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
```

## Performance Optimization

### For Speed

1. **Use Fast Mode** (no LLM):
   - Set `GROQ_API_KEY` and `GOOGLE_API_KEY` to empty
   - System uses fast architecture generation
   - ~30-60 seconds for complete project

2. **Parallel Processing**:
   - Multiple agents run concurrently
   - File generation parallelized
   - Dependency installation in background

3. **Caching**:
   - Mission states cached in memory
   - File counts cached per project
   - Recovery patterns cached

### For Reliability

1. **Enable Recovery Logging**:
   - Set `LOG_LEVEL=DEBUG` for detailed logs
   - Monitor recovery agent activity
   - Track retry attempts

2. **Persistent State**:
   - Mission states saved to `mission_states.json`
   - Survives server restarts
   - Full audit trail available

3. **Real Validation**:
   - All files verified on filesystem
   - Dependencies actually installed
   - Models actually trained
   - Builds actually executed

## Monitoring

### Real-Time Monitoring

```bash
# Watch mission progress
watch -n 1 'curl -s http://localhost:8000/mission-status/mission_20260506_203424 | jq .progress'

# Monitor file generation
watch -n 1 'curl -s http://localhost:8000/mission-status/mission_20260506_203424 | jq .file_counts'

# Check agent logs
curl -s http://localhost:8000/mission-logs/mission_20260506_203424 | jq '.logs[-10:]'
```

### Log Files

- **Backend Logs**: `backend/logs/metamind.log`
- **Mission States**: `mission_states.json`
- **Project Metadata**: `generated_projects/mission_*/project_metadata.json`

## Next Steps

1. **Explore Generated Projects**:
   - Download from Project Center
   - Review generated code
   - Deploy to Hugging Face Spaces

2. **Customize Architecture**:
   - Modify `ArchitectAgent` for custom designs
   - Add new agents to swarm
   - Extend recovery mechanisms

3. **Integrate with CI/CD**:
   - Use API endpoints in pipelines
   - Automate project generation
   - Deploy generated projects

4. **Scale to Production**:
   - Use Docker Compose for multi-container setup
   - Add load balancing
   - Implement distributed recovery
   - Add monitoring and alerting

## Support

For issues or questions:

1. Check `PRODUCTION_RELIABILITY_GUIDE.md` for detailed documentation
2. Review test results: `python test_core_recovery.py`
3. Check mission logs: `/mission-logs/{mission_id}`
4. Review agent theater for recovery details

## Success Indicators

✅ **System is working correctly when**:
- Health check returns `{"status": "healthy"}`
- Projects generate with real file counts > 0
- Mission status shows actual file counts from filesystem
- Recovery logs show successful schema repairs
- All tests pass: `python test_core_recovery.py`

## Performance Benchmarks

- **Dataset Analysis**: ~2-5 seconds
- **Architecture Generation**: ~5-10 seconds (with LLM) or ~1-2 seconds (fast mode)
- **File Generation**: ~10-20 seconds
- **Dependency Installation**: ~30-60 seconds
- **Total Project Generation**: ~60-120 seconds

**Total Time**: ~2-3 minutes for complete production-ready project

---

**MetaMind OS is now production-ready with enterprise-grade reliability!** 🚀
