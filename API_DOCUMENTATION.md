# MetaMind OS - API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. In production, add API key authentication.

## Response Format

All responses are in JSON format.

### Success Response
```json
{
  "status": "success",
  "data": {...},
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "status": "error",
  "error": "Error message",
  "details": {...}
}
```

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the MetaMind OS is operational

**Response**:
```json
{
  "status": "healthy",
  "swarm_agents": 8,
  "autonomous_mode": true,
  "projects_generated": 5
}
```

**Status Codes**:
- `200 OK`: System is healthy

---

### 2. Root Endpoint

**Endpoint**: `GET /`

**Description**: Get MetaMind OS information

**Response**:
```json
{
  "message": "MetaMind Autonomous AI Software Engineering OS",
  "status": "operational",
  "version": "1.0.0",
  "capabilities": [
    "Autonomous project generation",
    "8-agent swarm intelligence",
    "Real filesystem operations",
    "Production-ready code generation"
  ],
  "endpoints": {
    "upload": "/upload",
    "generate": "/generate-complete-project",
    "projects": "/projects",
    "docs": "/docs"
  }
}
```

---

### 3. Upload Dataset

**Endpoint**: `POST /upload`

**Description**: Upload a CSV dataset for analysis

**Request**:
```bash
curl -X POST -F "file=@dataset.csv" http://localhost:8000/upload
```

**Parameters**:
- `file` (required): CSV file to upload

**Response**:
```json
{
  "filename": "dataset.csv",
  "path": "uploads/dataset.csv"
}
```

**Status Codes**:
- `200 OK`: File uploaded successfully
- `400 Bad Request`: No file provided
- `413 Payload Too Large`: File too large

---

### 4. Generate Complete Project

**Endpoint**: `POST /generate-complete-project`

**Description**: Start autonomous project generation

**Request**:
```bash
curl -X POST "http://localhost:8000/generate-complete-project?dataset_path=uploads/dataset.csv&user_prompt=Build%20a%20classification%20model"
```

**Parameters**:
- `dataset_path` (required): Path to uploaded dataset
- `user_prompt` (required): User's project requirements

**Response**:
```json
{
  "mission_id": "mission_20260506_203424",
  "status": "running",
  "message": "Real autonomous generation started - use /mission-status/{mission_id} to track progress",
  "endpoints": {
    "status": "/mission-status/mission_20260506_203424",
    "logs": "/mission-logs/mission_20260506_203424"
  }
}
```

**Status Codes**:
- `200 OK`: Generation started successfully
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Dataset not found

**Important Notes**:
- Returns immediately with `mission_id` (NOT fake success)
- Use `/mission-status/{mission_id}` to track progress
- Generation happens in background
- Real files are created on filesystem

---

### 5. Get Mission Status

**Endpoint**: `GET /mission-status/{mission_id}`

**Description**: Get real-time mission status with actual file counts

**Request**:
```bash
curl http://localhost:8000/mission-status/mission_20260506_203424
```

**Parameters**:
- `mission_id` (required): Mission ID from generation endpoint

**Response**:
```json
{
  "mission_id": "mission_20260506_203424",
  "phase": "generating",
  "progress": 45,
  "status": "generating",
  "created_at": "2026-05-06T20:34:24.123456",
  "updated_at": "2026-05-06T20:35:10.654321",
  
  "file_counts": {
    "backend": 12,
    "frontend": 18,
    "ml": 7,
    "deployment": 3,
    "total": 40
  },
  "backend_files": 12,
  "frontend_files": 18,
  "ml_files": 7,
  "deployment_files": 3,
  "total_files": 40,
  
  "backend_status": "generating",
  "frontend_status": "pending",
  "ml_status": "pending",
  "deployment_status": "pending",
  
  "backend_builds": false,
  "frontend_builds": false,
  "ml_executes": false,
  "dependencies_installed": false,
  
  "errors": [],
  "retries": 0,
  "project_path": "/path/to/generated_projects/mission_20260506_203424",
  
  "recent_logs": [
    {
      "timestamp": "2026-05-06T20:34:25.123456",
      "agent": "Analyst",
      "message": "Dataset analysis complete",
      "phase": "analyzing",
      "level": "INFO"
    },
    {
      "timestamp": "2026-05-06T20:34:30.654321",
      "agent": "Architect",
      "message": "System architecture designed",
      "phase": "architecting",
      "level": "INFO"
    }
  ]
}
```

**Phases**:
- `initializing`: Setting up mission
- `analyzing`: Analyzing dataset
- `architecting`: Designing system architecture
- `generating`: Generating code files
- `validating`: Validating generated files
- `executing`: Running builds and tests
- `debugging`: Fixing errors (if needed)
- `deploying`: Creating deployment configs
- `complete`: Mission completed successfully
- `failed`: Mission failed

**Status Codes**:
- `200 OK`: Mission status retrieved
- `404 Not Found`: Mission not found

---

### 6. Get Mission Logs

**Endpoint**: `GET /mission-logs/{mission_id}`

**Description**: Get detailed mission logs

**Request**:
```bash
curl "http://localhost:8000/mission-logs/mission_20260506_203424?limit=50"
```

**Parameters**:
- `mission_id` (required): Mission ID
- `limit` (optional): Number of logs to return (default: 50)

**Response**:
```json
{
  "mission_id": "mission_20260506_203424",
  "total_logs": 127,
  "logs": [
    {
      "timestamp": "2026-05-06T20:34:24.123456",
      "agent": "SYSTEM",
      "message": "🚀 REAL AUTONOMOUS SWARM ENGAGED - Starting actual project generation",
      "phase": "initializing",
      "level": "INFO",
      "data": null
    },
    {
      "timestamp": "2026-05-06T20:34:25.234567",
      "agent": "Analyst",
      "message": "📊 Analyzing dataset structure and detecting ML problem type",
      "phase": "analyzing",
      "level": "INFO",
      "data": {
        "problem_type": "classification",
        "target_column": "target",
        "features": 10,
        "dataset_size": [100, 11]
      }
    },
    {
      "timestamp": "2026-05-06T20:34:30.345678",
      "agent": "Architect",
      "message": "🏗️ Designing complete system architecture with fault-tolerance",
      "phase": "architecting",
      "level": "INFO",
      "data": null
    },
    {
      "timestamp": "2026-05-06T20:34:35.456789",
      "agent": "Recovery Agent",
      "message": "🔧 Architecture attempt 1 failed, retrying...",
      "phase": "architecting",
      "level": "WARNING",
      "data": {
        "attempt": 1,
        "error": "Incomplete structured output"
      }
    },
    {
      "timestamp": "2026-05-06T20:34:36.567890",
      "agent": "Recovery Agent",
      "message": "✅ Architecture recovered successfully via recovery agent",
      "phase": "architecting",
      "level": "INFO",
      "data": {
        "recovery_method": "schema_recovery_engine",
        "fields_repaired": 6
      }
    }
  ]
}
```

**Log Levels**:
- `INFO`: Informational message
- `WARNING`: Warning message
- `ERROR`: Error message
- `DEBUG`: Debug message

**Status Codes**:
- `200 OK`: Logs retrieved
- `404 Not Found`: Mission not found

---

### 7. List Generated Projects

**Endpoint**: `GET /projects`

**Description**: List all generated projects with real file counts

**Request**:
```bash
curl http://localhost:8000/projects
```

**Response**:
```json
{
  "projects": [
    {
      "id": "mission_20260506_203424",
      "path": "/path/to/generated_projects/mission_20260506_203424",
      "metadata": {
        "project_id": "mission_20260506_203424",
        "created_at": "2026-05-06T20:34:24.123456",
        "dataset_path": "uploads/dataset.csv",
        "user_prompt": "Build a classification model",
        "problem_type": "classification",
        "target_column": "target",
        "backend_files": 12,
        "frontend_files": 18,
        "ml_files": 7,
        "deployment_files": 3,
        "total_files": 40,
        "status": "complete",
        "git_initialized": true,
        "build_success": true,
        "validation_passed": true,
        "real_generation": true
      },
      "real_file_counts": {
        "backend": 12,
        "frontend": 18,
        "ml": 7,
        "deployment": 3,
        "total": 40
      }
    }
  ],
  "total_projects": 1,
  "validation": "real_filesystem_counts"
}
```

**Status Codes**:
- `200 OK`: Projects listed successfully

---

### 8. Get Project File Structure

**Endpoint**: `GET /projects/{project_id}/files`

**Description**: Get project file structure

**Request**:
```bash
curl http://localhost:8000/projects/mission_20260506_203424/files
```

**Response**:
```json
{
  "file_tree": [
    {
      "name": "backend",
      "type": "directory",
      "path": "/backend",
      "children": [
        {
          "name": "app",
          "type": "directory",
          "path": "/backend/app",
          "children": [
            {
              "name": "main.py",
              "type": "file",
              "path": "/backend/app/main.py",
              "size": 2048
            }
          ]
        }
      ]
    },
    {
      "name": "frontend",
      "type": "directory",
      "path": "/frontend",
      "children": [...]
    }
  ]
}
```

**Status Codes**:
- `200 OK`: File structure retrieved
- `404 Not Found`: Project not found

---

### 9. Get Project File Content

**Endpoint**: `GET /projects/{project_id}/file/{file_path}`

**Description**: Get content of a specific file

**Request**:
```bash
curl http://localhost:8000/projects/mission_20260506_203424/file/backend/app/main.py
```

**Response**:
```json
{
  "content": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/\")\nasync def root():\n    return {\"message\": \"Hello World\"}",
  "file_path": "backend/app/main.py"
}
```

**Status Codes**:
- `200 OK`: File content retrieved
- `404 Not Found`: File not found
- `400 Bad Request`: Binary file (cannot display)

---

### 10. Download Project

**Endpoint**: `GET /projects/{project_id}/download`

**Description**: Download project as ZIP file

**Request**:
```bash
curl -O http://localhost:8000/projects/mission_20260506_203424/download
```

**Response**: ZIP file download

**Status Codes**:
- `200 OK`: ZIP file downloaded
- `404 Not Found`: Project not found

---

## WebSocket Endpoint

### Real-Time Status Updates

**Endpoint**: `WS /ws`

**Description**: WebSocket connection for real-time status updates

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Status update:', data);
};
```

**Message Format**:
```json
{
  "mission_id": "mission_20260506_203424",
  "agent": "Architect",
  "status": "🏗️ Designing complete system architecture",
  "phase": "architecting",
  "progress": 35,
  "data": {...}
}
```

---

## Error Handling

### Common Errors

#### 404 Not Found
```json
{
  "detail": "Mission not found"
}
```

#### 400 Bad Request
```json
{
  "detail": "Invalid parameters"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

### Error Recovery

The system automatically recovers from errors:
- Schema validation errors → Automatic repair
- Missing files → Regeneration
- Failed builds → Auto-fix and retry
- Network errors → Automatic retry

---

## Rate Limiting

Currently, no rate limiting is implemented. In production, add:
- 100 requests per minute per IP
- 10 concurrent project generations
- 5 MB file upload limit

---

## Pagination

Not currently implemented. For large result sets, use `limit` parameter where available.

---

## Versioning

Current API version: `1.0.0`

Future versions will maintain backward compatibility.

---

## Examples

### Example 1: Complete Project Generation Workflow

```bash
# 1. Upload dataset
UPLOAD_RESPONSE=$(curl -s -X POST -F "file=@dataset.csv" http://localhost:8000/upload)
DATASET_PATH=$(echo $UPLOAD_RESPONSE | jq -r '.path')

# 2. Start generation
GEN_RESPONSE=$(curl -s -X POST "http://localhost:8000/generate-complete-project?dataset_path=$DATASET_PATH&user_prompt=Build%20a%20classification%20model")
MISSION_ID=$(echo $GEN_RESPONSE | jq -r '.mission_id')

# 3. Poll status
while true; do
  STATUS=$(curl -s http://localhost:8000/mission-status/$MISSION_ID)
  PROGRESS=$(echo $STATUS | jq -r '.progress')
  PHASE=$(echo $STATUS | jq -r '.phase')
  
  echo "Progress: $PROGRESS% - Phase: $PHASE"
  
  if [ "$PHASE" = "complete" ] || [ "$PHASE" = "failed" ]; then
    break
  fi
  
  sleep 5
done

# 4. Download project
curl -O http://localhost:8000/projects/$MISSION_ID/download
```

### Example 2: Monitor Real-Time Logs

```bash
# Get mission logs continuously
MISSION_ID="mission_20260506_203424"

while true; do
  curl -s "http://localhost:8000/mission-logs/$MISSION_ID?limit=10" | jq '.logs[-5:]'
  sleep 2
done
```

### Example 3: Check Project Files

```bash
MISSION_ID="mission_20260506_203424"

# Get file structure
curl -s http://localhost:8000/projects/$MISSION_ID/files | jq '.file_tree'

# Get specific file content
curl -s http://localhost:8000/projects/$MISSION_ID/file/backend/app/main.py | jq '.content'
```

---

## Best Practices

1. **Always check mission status** before assuming generation is complete
2. **Use WebSocket** for real-time updates instead of polling
3. **Handle errors gracefully** - the system auto-recovers
4. **Download projects** after generation completes
5. **Monitor logs** for recovery activities and debugging info

---

## Support

For API issues:
1. Check `/health` endpoint
2. Review mission logs: `/mission-logs/{mission_id}`
3. Check recent projects: `/projects`
4. Review documentation: `PRODUCTION_RELIABILITY_GUIDE.md`

---

**MetaMind OS API - Production Ready** ✅
