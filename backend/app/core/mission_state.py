"""
Mission State Manager for MetaMind OS
Tracks real-time autonomous generation state
"""
import json
import asyncio
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel
import logging

logger = logging.getLogger("metamind.mission")

class MissionPhase(str, Enum):
    INITIALIZING = "initializing"
    ANALYZING = "analyzing"
    ARCHITECTING = "architecting"
    GENERATING = "generating"
    VALIDATING = "validating"
    EXECUTING = "executing"
    DEBUGGING = "debugging"
    DEPLOYING = "deploying"
    COMPLETE = "complete"
    FAILED = "failed"

class MissionLog(BaseModel):
    timestamp: datetime
    agent: str
    message: str
    phase: MissionPhase
    level: str = "INFO"
    data: Optional[Dict[str, Any]] = None

class MissionState(BaseModel):
    mission_id: str
    created_at: datetime
    updated_at: datetime
    phase: MissionPhase
    progress: int  # 0-100
    dataset_path: str
    user_prompt: str
    
    # Real filesystem counts
    backend_files: int = 0
    frontend_files: int = 0
    ml_files: int = 0
    deployment_files: int = 0
    total_files: int = 0
    
    # Component status
    backend_status: str = "pending"  # pending, generating, validating, complete, failed
    frontend_status: str = "pending"
    ml_status: str = "pending"
    deployment_status: str = "pending"
    
    # Validation results
    backend_builds: bool = False
    frontend_builds: bool = False
    ml_executes: bool = False
    dependencies_installed: bool = False
    
    # Execution tracking
    logs: List[MissionLog] = []
    errors: List[str] = []
    retries: int = 0
    max_retries: int = 3
    
    # Project paths
    project_path: str = ""
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MissionStateManager:
    """Manages mission state with real-time tracking"""
    
    def __init__(self):
        self.missions: Dict[str, MissionState] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.state_file = "mission_states.json"
        self._load_states()
    
    def create_mission(self, dataset_path: str, user_prompt: str) -> str:
        """Create new mission with unique ID"""
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        mission = MissionState(
            mission_id=mission_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            phase=MissionPhase.INITIALIZING,
            progress=0,
            dataset_path=dataset_path,
            user_prompt=user_prompt
        )
        
        self.missions[mission_id] = mission
        self._save_states()
        
        logger.info(f"🚀 Created mission: {mission_id}")
        return mission_id
    
    def update_mission(self, mission_id: str, **updates) -> bool:
        """Update mission state with real data"""
        if mission_id not in self.missions:
            return False
        
        mission = self.missions[mission_id]
        
        for key, value in updates.items():
            if hasattr(mission, key):
                setattr(mission, key, value)
        
        mission.updated_at = datetime.now()
        self._save_states()
        
        logger.info(f"📊 Updated mission {mission_id}: {updates}")
        return True
    
    def add_log(self, mission_id: str, agent: str, message: str, phase: MissionPhase, level: str = "INFO", data: Optional[Dict] = None):
        """Add real-time log entry"""
        if mission_id not in self.missions:
            return False
        
        log_entry = MissionLog(
            timestamp=datetime.now(),
            agent=agent,
            message=message,
            phase=phase,
            level=level,
            data=data
        )
        
        self.missions[mission_id].logs.append(log_entry)
        self.missions[mission_id].updated_at = datetime.now()
        self._save_states()
        
        logger.info(f"📝 [{agent}] {message}")
        return True
    
    def add_error(self, mission_id: str, error: str):
        """Add error to mission"""
        if mission_id not in self.missions:
            return False
        
        self.missions[mission_id].errors.append(error)
        self.missions[mission_id].updated_at = datetime.now()
        self._save_states()
        
        logger.error(f"❌ Mission {mission_id} error: {error}")
        return True
    
    def get_mission(self, mission_id: str) -> Optional[MissionState]:
        """Get mission state"""
        return self.missions.get(mission_id)
    
    def get_all_missions(self) -> List[MissionState]:
        """Get all missions"""
        return list(self.missions.values())
    
    def count_real_files(self, mission_id: str, project_path: str) -> Dict[str, int]:
        """Count actual files on filesystem"""
        try:
            counts = {
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
                    counts["backend"] += len([f for f in files if not f.startswith('.') and not f.endswith('.pyc')])
            
            # Count frontend files
            frontend_path = os.path.join(project_path, "frontend")
            if os.path.exists(frontend_path):
                for root, dirs, files in os.walk(frontend_path):
                    if 'node_modules' in root or '.git' in root:
                        continue
                    counts["frontend"] += len([f for f in files if not f.startswith('.')])
            
            # Count ML files
            ml_path = os.path.join(project_path, "ml")
            if os.path.exists(ml_path):
                for root, dirs, files in os.walk(ml_path):
                    counts["ml"] += len([f for f in files if not f.startswith('.') and not f.endswith('.pyc')])
            
            # Count deployment files
            deployment_files = ["Dockerfile", "docker-compose.yml", ".env.example", "railway.json", "render.yaml", "README.md"]
            for file_name in deployment_files:
                if os.path.exists(os.path.join(project_path, file_name)):
                    counts["deployment"] += 1
            
            counts["total"] = counts["backend"] + counts["frontend"] + counts["ml"] + counts["deployment"]
            
            # Update mission state with real counts
            self.update_mission(mission_id, 
                backend_files=counts["backend"],
                frontend_files=counts["frontend"],
                ml_files=counts["ml"],
                deployment_files=counts["deployment"],
                total_files=counts["total"]
            )
            
            logger.info(f"📊 Real file counts for {mission_id}: {counts}")
            return counts
            
        except Exception as e:
            logger.error(f"File counting error: {e}")
            return {"backend": 0, "frontend": 0, "ml": 0, "deployment": 0, "total": 0}
    
    def mark_complete(self, mission_id: str, success: bool = True):
        """Mark mission as complete only after real validation"""
        if mission_id not in self.missions:
            return False
        
        mission = self.missions[mission_id]
        
        # Only mark complete if all validations pass
        if success and mission.backend_builds and mission.frontend_builds and mission.ml_executes:
            mission.phase = MissionPhase.COMPLETE
            mission.progress = 100
            self.add_log(mission_id, "SYSTEM", "✅ MISSION COMPLETE - All validations passed", MissionPhase.COMPLETE)
        else:
            mission.phase = MissionPhase.FAILED
            self.add_log(mission_id, "SYSTEM", "❌ MISSION FAILED - Validation incomplete", MissionPhase.FAILED)
        
        mission.updated_at = datetime.now()
        self._save_states()
        
        return True
    
    def _save_states(self):
        """Persist mission states to disk"""
        try:
            states_data = {}
            for mission_id, mission in self.missions.items():
                states_data[mission_id] = mission.dict()
            
            with open(self.state_file, 'w') as f:
                json.dump(states_data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save mission states: {e}")
    
    def _load_states(self):
        """Load mission states from disk"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    states_data = json.load(f)
                
                for mission_id, mission_data in states_data.items():
                    # Convert datetime strings back to datetime objects
                    if 'created_at' in mission_data:
                        mission_data['created_at'] = datetime.fromisoformat(mission_data['created_at'])
                    if 'updated_at' in mission_data:
                        mission_data['updated_at'] = datetime.fromisoformat(mission_data['updated_at'])
                    
                    # Convert log timestamps
                    if 'logs' in mission_data:
                        for log in mission_data['logs']:
                            if 'timestamp' in log:
                                log['timestamp'] = datetime.fromisoformat(log['timestamp'])
                    
                    self.missions[mission_id] = MissionState(**mission_data)
                
                logger.info(f"📂 Loaded {len(self.missions)} mission states")
        except Exception as e:
            logger.error(f"Failed to load mission states: {e}")

# Global mission state manager
mission_manager = MissionStateManager()