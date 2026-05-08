from fastapi import FastAPI, WebSocket, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import shutil
import json
import asyncio
import logging
from .core.orchestrator import MetaMindOrchestrator
from .agents.autonomous_swarm import AutonomousSwarmOrchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("metamind")

load_dotenv()

app = FastAPI(title="MetaMind Autonomous AI Software Engineering OS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections = []
autonomous_swarm = AutonomousSwarmOrchestrator()

@app.get("/")
async def root():
    """Root endpoint - MetaMind OS status"""
    return {
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "swarm_agents": 8,
        "autonomous_mode": True,
        "projects_generated": len(os.listdir(autonomous_swarm.workspace_root)) if os.path.exists(autonomous_swarm.workspace_root) else 0
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        if websocket in active_connections:
            active_connections.remove(websocket)

async def broadcast_status(data: dict):
    for connection in active_connections:
        try:
            await connection.send_json(data)
        except:
            pass

@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    upload_dir = os.getenv("UPLOAD_DIR", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "path": file_path}

@app.post("/run")
async def run_analysis(dataset_path: str, instruction: str, background_tasks: BackgroundTasks):
    orchestrator = MetaMindOrchestrator(on_status_update=broadcast_status)
    background_tasks.add_task(orchestrator.run, dataset_path, instruction)
    return {"message": "Analysis started in background"}

@app.post("/generate-complete-project")
async def generate_complete_project(dataset_path: str, user_prompt: str, background_tasks: BackgroundTasks):
    """
    🚀 REAL AUTONOMOUS PROJECT GENERATION ENDPOINT
    Creates actual working ML applications with proper async execution
    """
    from .core.mission_state import mission_manager, MissionPhase
    
    logger.info("🚀 AUTONOMOUS SWARM: Real project generation requested")
    
    # Create mission with unique ID
    mission_id = mission_manager.create_mission(dataset_path, user_prompt)
    
    async def real_autonomous_generation_task():
        """Real autonomous generation with proper state tracking"""
        try:
            # Update mission state
            mission_manager.update_mission(mission_id, 
                phase=MissionPhase.INITIALIZING,
                progress=5
            )
            
            mission_manager.add_log(mission_id, "SYSTEM", 
                "🚀 REAL AUTONOMOUS SWARM ENGAGED - Starting actual project generation",
                MissionPhase.INITIALIZING
            )
            
            # Broadcast to WebSocket clients
            await broadcast_status({
                "mission_id": mission_id,
                "agent": "SYSTEM",
                "status": "🚀 REAL AUTONOMOUS SWARM ENGAGED - Starting actual project generation",
                "phase": "initializing",
                "progress": 5
            })
            
            # Generate complete project with real validation
            generated_project = await autonomous_swarm.generate_complete_project(
                dataset_path, 
                user_prompt,
                on_status_update=lambda status: _handle_mission_update(mission_id, status)
            )
            
            # Count real files on filesystem
            real_counts = mission_manager.count_real_files(mission_id, generated_project.project_path)
            
            # Update mission with real project path
            mission_manager.update_mission(mission_id,
                project_path=generated_project.project_path,
                phase=MissionPhase.COMPLETE if generated_project.status == "complete" else MissionPhase.FAILED,
                progress=100 if generated_project.status == "complete" else 75
            )
            
            # Final validation
            if generated_project.status == "complete" and real_counts["total"] > 0:
                mission_manager.add_log(mission_id, "SYSTEM",
                    f"✅ REAL PROJECT GENERATION COMPLETE - {real_counts['total']} files created",
                    MissionPhase.COMPLETE,
                    data=real_counts
                )
                
                await broadcast_status({
                    "mission_id": mission_id,
                    "agent": "SYSTEM", 
                    "status": f"✅ REAL PROJECT GENERATION COMPLETE - {real_counts['total']} files created",
                    "phase": "complete",
                    "progress": 100,
                    "data": {
                        "project_path": generated_project.project_path,
                        "file_counts": real_counts,
                        "status": generated_project.status
                    }
                })
                
                mission_manager.mark_complete(mission_id, True)
            else:
                mission_manager.add_log(mission_id, "SYSTEM",
                    "❌ PROJECT GENERATION INCOMPLETE - Validation failed",
                    MissionPhase.FAILED
                )
                
                await broadcast_status({
                    "mission_id": mission_id,
                    "agent": "SYSTEM",
                    "status": "❌ PROJECT GENERATION INCOMPLETE - Validation failed",
                    "phase": "failed",
                    "progress": 75
                })
                
                mission_manager.mark_complete(mission_id, False)
            
        except Exception as e:
            logger.error(f"Real autonomous generation failed: {e}")
            
            mission_manager.add_error(mission_id, str(e))
            mission_manager.update_mission(mission_id, 
                phase=MissionPhase.FAILED,
                progress=0
            )
            
            await broadcast_status({
                "mission_id": mission_id,
                "agent": "SYSTEM",
                "status": f"❌ REAL GENERATION FAILED: {str(e)}",
                "phase": "failed",
                "progress": 0
            })
    
    async def _handle_mission_update(mission_id: str, status: dict):
        """Handle mission status updates from agents"""
        phase_map = {
            "initialization": MissionPhase.INITIALIZING,
            "analysis": MissionPhase.ANALYZING,
            "architecture": MissionPhase.ARCHITECTING,
            "generation": MissionPhase.GENERATING,
            "validation": MissionPhase.VALIDATING,
            "execution": MissionPhase.EXECUTING,
            "debugging": MissionPhase.DEBUGGING,
            "deployment": MissionPhase.DEPLOYING,
            "complete": MissionPhase.COMPLETE,
            "error": MissionPhase.FAILED
        }
        
        phase = phase_map.get(status.get("phase", ""), MissionPhase.EXECUTING)
        progress = min(95, mission_manager.get_mission(mission_id).progress + 10)  # Increment progress
        
        mission_manager.update_mission(mission_id,
            phase=phase,
            progress=progress
        )
        
        mission_manager.add_log(mission_id, 
            status.get("agent", "UNKNOWN"),
            status.get("status", "Processing..."),
            phase,
            data=status.get("data")
        )
        
        # Broadcast to WebSocket
        await broadcast_status({
            **status,
            "mission_id": mission_id,
            "progress": progress
        })
    
    # Start background task
    background_tasks.add_task(real_autonomous_generation_task)
    
    # Return immediately with mission ID - NOT success
    return {
        "mission_id": mission_id,
        "status": "running", 
        "message": "🚀 Real autonomous generation started - use /mission-status/{mission_id} to track progress",
        "endpoints": {
            "status": f"/mission-status/{mission_id}",
            "logs": f"/mission-logs/{mission_id}"
        }
    }

@app.get("/mission-status/{mission_id}")
async def get_mission_status(mission_id: str):
    """Get real-time mission status with actual file counts"""
    from .core.mission_state import mission_manager
    
    mission = mission_manager.get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Get real-time file counts if project exists
    if mission.project_path and os.path.exists(mission.project_path):
        real_counts = mission_manager.count_real_files(mission_id, mission.project_path)
    else:
        real_counts = {"backend": 0, "frontend": 0, "ml": 0, "deployment": 0, "total": 0}
    
    return {
        "mission_id": mission.mission_id,
        "phase": mission.phase,
        "progress": mission.progress,
        "status": mission.phase.value,
        "created_at": mission.created_at.isoformat(),
        "updated_at": mission.updated_at.isoformat(),
        
        # Real filesystem data
        "file_counts": real_counts,
        "backend_files": real_counts["backend"],
        "frontend_files": real_counts["frontend"], 
        "ml_files": real_counts["ml"],
        "deployment_files": real_counts["deployment"],
        "total_files": real_counts["total"],
        
        # Component status
        "backend_status": mission.backend_status,
        "frontend_status": mission.frontend_status,
        "ml_status": mission.ml_status,
        "deployment_status": mission.deployment_status,
        
        # Validation results
        "backend_builds": mission.backend_builds,
        "frontend_builds": mission.frontend_builds,
        "ml_executes": mission.ml_executes,
        "dependencies_installed": mission.dependencies_installed,
        
        # Execution data
        "errors": mission.errors,
        "retries": mission.retries,
        "project_path": mission.project_path,
        
        # Recent logs (last 10)
        "recent_logs": [
            {
                "timestamp": log.timestamp.isoformat(),
                "agent": log.agent,
                "message": log.message,
                "phase": log.phase,
                "level": log.level
            }
            for log in mission.logs[-10:]
        ]
    }

@app.get("/mission-logs/{mission_id}")
async def get_mission_logs(mission_id: str, limit: int = 50):
    """Get detailed mission logs"""
    from .core.mission_state import mission_manager
    
    mission = mission_manager.get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    logs = mission.logs[-limit:] if limit > 0 else mission.logs
    
    return {
        "mission_id": mission_id,
        "total_logs": len(mission.logs),
        "logs": [
            {
                "timestamp": log.timestamp.isoformat(),
                "agent": log.agent,
                "message": log.message,
                "phase": log.phase,
                "level": log.level,
                "data": log.data
            }
            for log in logs
        ]
    }

@app.get("/projects")
async def list_generated_projects():
    """List all generated projects with REAL file counts from filesystem"""
    from .core.mission_state import mission_manager
    
    projects_dir = autonomous_swarm.workspace_root
    if not os.path.exists(projects_dir):
        return {"projects": []}
    
    projects = []
    for project_dir in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project_dir)
        if os.path.isdir(project_path):
            # Count REAL files on filesystem
            real_counts = {
                "backend": 0,
                "frontend": 0,
                "ml": 0,
                "deployment": 0,
                "total": 0
            }
            
            # Count backend files
            backend_path = os.path.join(project_path, "backend")
            if os.path.exists(backend_path):
                for root, dirs, files in os.walk(backend_path):
                    real_counts["backend"] += len([f for f in files if not f.startswith('.') and not f.endswith('.pyc')])
            
            # Count frontend files
            frontend_path = os.path.join(project_path, "frontend")
            if os.path.exists(frontend_path):
                for root, dirs, files in os.walk(frontend_path):
                    if 'node_modules' in root or '.git' in root:
                        continue
                    real_counts["frontend"] += len([f for f in files if not f.startswith('.')])
            
            # Count ML files
            ml_path = os.path.join(project_path, "ml")
            if os.path.exists(ml_path):
                for root, dirs, files in os.walk(ml_path):
                    real_counts["ml"] += len([f for f in files if not f.startswith('.') and not f.endswith('.pyc')])
            
            # Count deployment files
            deployment_files = ["Dockerfile", "docker-compose.yml", ".env.example", "railway.json", "render.yaml", "README.md"]
            for file_name in deployment_files:
                if os.path.exists(os.path.join(project_path, file_name)):
                    real_counts["deployment"] += 1
            
            real_counts["total"] = real_counts["backend"] + real_counts["frontend"] + real_counts["ml"] + real_counts["deployment"]
            
            # Load metadata if exists
            metadata_file = os.path.join(project_path, "project_metadata.json")
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, "r") as f:
                        metadata = json.load(f)
                    
                    # Override with REAL counts
                    metadata["backend_files"] = real_counts["backend"]
                    metadata["frontend_files"] = real_counts["frontend"]
                    metadata["ml_files"] = real_counts["ml"]
                    metadata["deployment_files"] = real_counts["deployment"]
                    metadata["total_files"] = real_counts["total"]
                    metadata["real_validation"] = True
                    
                except Exception as e:
                    logger.error(f"Error reading metadata for {project_dir}: {e}")
                    metadata = {
                        "status": "unknown",
                        "backend_files": real_counts["backend"],
                        "frontend_files": real_counts["frontend"],
                        "ml_files": real_counts["ml"],
                        "deployment_files": real_counts["deployment"],
                        "total_files": real_counts["total"],
                        "real_validation": True
                    }
            else:
                metadata = {
                    "status": "partial" if real_counts["total"] > 0 else "empty",
                    "backend_files": real_counts["backend"],
                    "frontend_files": real_counts["frontend"],
                    "ml_files": real_counts["ml"],
                    "deployment_files": real_counts["deployment"],
                    "total_files": real_counts["total"],
                    "real_validation": True,
                    "note": "Metadata missing - counts from filesystem scan"
                }
            
            projects.append({
                "id": project_dir,
                "path": project_path,
                "metadata": metadata,
                "real_file_counts": real_counts
            })
    
    # Sort by creation time (newest first)
    projects.sort(key=lambda x: x.get("metadata", {}).get("created_at", ""), reverse=True)
    
    return {
        "projects": projects,
        "total_projects": len(projects),
        "validation": "real_filesystem_counts"
    }

@app.get("/projects/{project_id}/download")
async def download_project(project_id: str):
    """Download generated project as ZIP"""
    project_path = os.path.join(autonomous_swarm.workspace_root, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create ZIP file
    zip_path = f"{project_path}.zip"
    shutil.make_archive(project_path, 'zip', project_path)
    
    return FileResponse(
        zip_path,
        media_type='application/zip',
        filename=f"{project_id}.zip"
    )

@app.get("/projects/{project_id}/files")
async def get_project_files(project_id: str):
    """Get project file structure"""
    project_path = os.path.join(autonomous_swarm.workspace_root, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    
    def get_file_tree(path, prefix=""):
        items = []
        try:
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append({
                        "name": item,
                        "type": "directory",
                        "path": f"{prefix}/{item}",
                        "children": get_file_tree(item_path, f"{prefix}/{item}")
                    })
                else:
                    items.append({
                        "name": item,
                        "type": "file", 
                        "path": f"{prefix}/{item}",
                        "size": os.path.getsize(item_path)
                    })
        except PermissionError:
            pass
        return items
    
    return {"file_tree": get_file_tree(project_path)}

@app.get("/projects/{project_id}/file/{file_path:path}")
async def get_project_file_content(project_id: str, file_path: str):
    """Get content of a specific file"""
    project_path = os.path.join(autonomous_swarm.workspace_root, project_id)
    full_file_path = os.path.join(project_path, file_path)
    
    if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(full_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content, "file_path": file_path}
    except UnicodeDecodeError:
        return {"error": "Binary file cannot be displayed", "file_path": file_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
