"""
MetaMind Autonomous AI Software Engineering Swarm
Complete project generation from dataset + prompt
"""
import os
import json
import asyncio
import subprocess
import shutil
import git
from typing import Dict, Any, List, Optional
from pathlib import Path
from pydantic import BaseModel
import logging
from datetime import datetime

logger = logging.getLogger("metamind.autonomous")

class ProjectSpec(BaseModel):
    """Complete project specification"""
    project_name: str
    problem_type: str  # classification, regression, clustering
    target_column: str
    features: List[str]
    dataset_path: str
    user_prompt: str
    ml_algorithm: str
    frontend_type: str = "react"
    backend_type: str = "fastapi"
    deployment_target: str = "huggingface"

class GeneratedProject(BaseModel):
    """Complete generated project structure"""
    project_path: str
    backend_files: List[str]
    frontend_files: List[str]
    ml_files: List[str]
    deployment_files: List[str]
    git_repo: Optional[str] = None
    huggingface_url: Optional[str] = None
    status: str = "generated"
    errors: List[str] = []
    metrics: Dict[str, Any] = {}

class ExecutionResult:
    """Simple execution result class"""
    def __init__(self, success: bool, errors: list = None, health_status: dict = None):
        self.success = success
        self.errors = errors or []
        self.health_status = health_status or {}

class AutonomousSwarmOrchestrator:
    """Master orchestrator for the 8-agent autonomous swarm"""
    
    def __init__(self, workspace_root: str = "generated_projects"):
        self.workspace_root = workspace_root
        self.current_project = None
        self.agents = {}
        self.project_counter = 0
        
        # Initialize workspace
        os.makedirs(workspace_root, exist_ok=True)
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agents including recovery agent"""
        from .swarm_agents import (
            AnalystAgent, ArchitectAgent, EngineerAgent, ExecutorAgent,
            DebuggerAgent, EvaluatorAgent, DevOpsAgent, GitHubAgent, RecoveryAgent
        )
        
        self.agents = {
            "analyst": AnalystAgent(),
            "architect": ArchitectAgent(), 
            "engineer": EngineerAgent(),
            "executor": ExecutorAgent(),
            "debugger": DebuggerAgent(),
            "evaluator": EvaluatorAgent(),
            "devops": DevOpsAgent(),
            "github": GitHubAgent(),
            "recovery": RecoveryAgent()
        }
    
    async def generate_complete_project(self, dataset_path: str, user_prompt: str, on_status_update=None) -> GeneratedProject:
        """
        REAL AUTONOMOUS ENGINEERING INTELLIGENCE
        Generate ACTUAL working full-stack ML applications with REAL filesystem operations
        """
        try:
            project_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            project_path = os.path.join(self.workspace_root, project_id)
            
            if on_status_update:
                await on_status_update({
                    "agent": "SYSTEM",
                    "status": "🚀 REAL AUTONOMOUS SWARM ENGAGED - Creating actual working project",
                    "phase": "initialization"
                })
            
            # STEP 1: CREATE REAL PROJECT STRUCTURE
            self._create_complete_project_structure(project_path)
            
            # STEP 2: REAL DATASET ANALYSIS
            if on_status_update:
                await on_status_update({
                    "agent": "Analyst Agent", 
                    "status": "📊 Analyzing dataset structure and detecting ML problem type",
                    "phase": "analysis"
                })
            
            analysis = await self.agents["analyst"].analyze_dataset_intelligence(dataset_path, user_prompt)
            
            # STEP 3: REAL ARCHITECTURE DESIGN WITH RECOVERY
            if on_status_update:
                await on_status_update({
                    "agent": "Architect Agent",
                    "status": "🏗️ Designing complete system architecture with fault-tolerance", 
                    "phase": "architecture"
                })
            
            architecture = None
            architecture_attempts = 0
            max_architecture_attempts = 3
            
            while architecture is None and architecture_attempts < max_architecture_attempts:
                try:
                    architecture_attempts += 1
                    logger.info(f"🏗️ Architecture attempt {architecture_attempts}/{max_architecture_attempts}")
                    
                    architecture = await self.agents["architect"].design_complete_system(analysis)
                    
                    # Validate architecture has critical fields
                    if not architecture.database_schema:
                        raise ValueError("Architecture missing database_schema")
                    
                    logger.info("✅ Architecture generation successful")
                    break
                    
                except Exception as arch_error:
                    logger.warning(f"Architecture attempt {architecture_attempts} failed: {arch_error}")
                    
                    if architecture_attempts < max_architecture_attempts:
                        if on_status_update:
                            await on_status_update({
                                "agent": "Recovery Agent",
                                "status": f"🔧 Architecture attempt {architecture_attempts} failed, retrying...",
                                "phase": "architecture"
                            })
                        
                        # Wait before retry
                        await asyncio.sleep(1)
                    else:
                        # Final attempt - use recovery agent
                        if on_status_update:
                            await on_status_update({
                                "agent": "Recovery Agent",
                                "status": "🔧 All architecture attempts failed, initiating recovery protocol",
                                "phase": "architecture"
                            })
                        
                        # Use recovery agent to fix architecture
                        architecture = await self.agents["recovery"].recover_failed_architecture(str(arch_error), analysis)
                        
                        if on_status_update:
                            await on_status_update({
                                "agent": "Recovery Agent",
                                "status": "✅ Architecture recovered successfully via recovery agent",
                                "phase": "architecture"
                            })
            
            # Final safety check
            if architecture is None:
                logger.error("❌ All architecture generation attempts failed")
                # Emergency fallback
                from .swarm_agents import SystemArchitecture
                architecture = SystemArchitecture.create_safe_fallback()
                
                if on_status_update:
                    await on_status_update({
                        "agent": "SYSTEM",
                        "status": "🆘 Using emergency fallback architecture",
                        "phase": "architecture"
                    })
            
            # STEP 4: REAL FILE GENERATION
            if on_status_update:
                await on_status_update({
                    "agent": "Engineer Agent",
                    "status": "⚙️ Writing REAL production files to filesystem",
                    "phase": "generation"
                })
            
            generated_files = await self.agents["engineer"].generate_real_application_files(
                analysis, architecture, project_path
            )
            
            # STEP 5: REAL FILE VALIDATION
            if on_status_update:
                await on_status_update({
                    "agent": "Executor Agent",
                    "status": "🔍 Validating real file existence and structure",
                    "phase": "validation"
                })
            
            file_validation = await self._validate_real_files(project_path, generated_files)
            
            # STEP 6: REAL DEPENDENCY INSTALLATION
            if on_status_update:
                await on_status_update({
                    "agent": "Executor Agent",
                    "status": "📦 Installing real dependencies and building project",
                    "phase": "execution"
                })
            
            execution_result = await self.agents["executor"].execute_and_validate_project(
                project_path, generated_files, on_status_update
            )
            
            # STEP 7: SELF-HEALING IF NEEDED
            retry_count = 0
            while not execution_result.success and retry_count < 3:
                if on_status_update:
                    await on_status_update({
                        "agent": "Debugger Agent",
                        "status": f"🔧 Auto-fixing real errors (attempt {retry_count + 1}/3)",
                        "phase": "debugging"
                    })
                
                execution_result = await self.agents["debugger"].auto_fix_and_retry(
                    project_path, execution_result.errors, on_status_update
                )
                retry_count += 1
            
            # STEP 8: REAL DEPLOYMENT CONFIGS
            if on_status_update:
                await on_status_update({
                    "agent": "DevOps Agent",
                    "status": "🐳 Generating real deployment configurations",
                    "phase": "deployment"
                })
            
            deployment_files = await self.agents["devops"].generate_deployment_configs(
                project_path, architecture
            )
            
            # STEP 9: REAL GITHUB REPOSITORY
            if on_status_update:
                await on_status_update({
                    "agent": "GitHub Agent", 
                    "status": "📦 Creating real GitHub repository structure",
                    "phase": "repository"
                })
            
            github_result = await self.agents["github"].create_real_repository(
                project_path, analysis, architecture
            )
            
            # STEP 10: FINAL VALIDATION - COUNT REAL FILES
            real_file_counts = self._count_real_files(project_path)
            
            # SAVE REAL PROJECT METADATA
            metadata = {
                "project_id": project_id,
                "created_at": datetime.now().isoformat(),
                "dataset_path": dataset_path,
                "user_prompt": user_prompt,
                "problem_type": analysis.problem_type,
                "target_column": analysis.target_column,
                "backend_files": real_file_counts["backend"],
                "frontend_files": real_file_counts["frontend"], 
                "ml_files": real_file_counts["ml"],
                "deployment_files": real_file_counts["deployment"],
                "total_files": real_file_counts["total"],
                "status": "complete" if execution_result.success else "partial",
                "git_initialized": github_result.success if github_result else False,
                "build_success": execution_result.success,
                "validation_passed": file_validation,
                "real_generation": True
            }
            
            with open(os.path.join(project_path, "project_metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)
            
            if on_status_update:
                await on_status_update({
                    "agent": "SYSTEM",
                    "status": f"✅ REAL PROJECT GENERATION COMPLETE - {real_file_counts['total']} files created",
                    "phase": "complete",
                    "data": metadata
                })
            
            return GeneratedProject(
                project_path=project_path,
                backend_files=generated_files.backend_files,
                frontend_files=generated_files.frontend_files,
                ml_files=generated_files.ml_files,
                deployment_files=deployment_files,
                status="complete" if execution_result.success else "partial",
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"❌ REAL GENERATION FAILED: {e}")
            if on_status_update:
                await on_status_update({
                    "agent": "SYSTEM",
                    "status": f"❌ Generation failed: {str(e)} - Attempting recovery",
                    "phase": "error"
                })
            return await self._emergency_recovery(dataset_path, user_prompt, str(e))
    
    def _create_real_project_structure(self, project_path: str):
        """Create complete real project structure with all necessary directories"""
        directories = [
            "backend/app/routes",
            "backend/app/services", 
            "backend/app/models",
            "backend/app/utils",
            "backend/tests",
            "frontend/src/components/pages",
            "frontend/src/components/ui",
            "frontend/src/services",
            "frontend/src/hooks",
            "frontend/src/utils",
            "frontend/public",
            "ml/models",
            "ml/data", 
            "ml/notebooks",
            "ml/utils",
            "deployment",
            "docs",
            "logs",
            "uploads"
        ]
        
        for directory in directories:
            full_path = os.path.join(project_path, directory)
            os.makedirs(full_path, exist_ok=True)
            
    def _create_complete_project_structure(self, project_path: str):
        """Create complete real project structure with all necessary directories"""
        directories = [
            "backend/app/routes",
            "backend/app/services", 
            "backend/app/models",
            "backend/app/utils",
            "backend/tests",
            "frontend/src/components/pages",
            "frontend/src/components/ui",
            "frontend/src/services",
            "frontend/src/hooks",
            "frontend/src/utils",
            "frontend/public",
            "ml/models",
            "ml/data", 
            "ml/notebooks",
            "ml/utils",
            "deployment",
            "docs",
            "logs",
            "uploads"
        ]
        
        for directory in directories:
            full_path = os.path.join(project_path, directory)
            os.makedirs(full_path, exist_ok=True)
            
        logger.info(f"✅ Created complete real project structure at {project_path}")
        
        # Verify directories were created
        created_dirs = []
        for directory in directories:
            full_path = os.path.join(project_path, directory)
            if os.path.exists(full_path):
                created_dirs.append(directory)
        
        logger.info(f"📁 Verified {len(created_dirs)}/{len(directories)} directories created")
        return len(created_dirs) == len(directories)
    
    async def _validate_real_files(self, project_path: str, generated_files) -> bool:
        """Validate that all generated files actually exist on filesystem"""
        try:
            logger.info("🔍 VALIDATING: Real file existence on filesystem")
            
            all_files = []
            if hasattr(generated_files, 'backend_files'):
                all_files.extend(generated_files.backend_files)
            if hasattr(generated_files, 'frontend_files'):
                all_files.extend(generated_files.frontend_files)
            if hasattr(generated_files, 'ml_files'):
                all_files.extend(generated_files.ml_files)
            if hasattr(generated_files, 'config_files'):
                all_files.extend(generated_files.config_files)
            
            missing_files = []
            for file_path in all_files:
                full_path = os.path.join(project_path, file_path)
                if not os.path.exists(full_path):
                    missing_files.append(file_path)
            
            if missing_files:
                logger.error(f"❌ Missing files: {missing_files}")
                return False
            
            logger.info(f"✅ All {len(all_files)} files validated on filesystem")
            return True
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return False
    
    def _count_real_files(self, project_path: str) -> Dict[str, int]:
        """Count actual files that exist on the filesystem"""
        try:
            counts = {
                "backend": 0,
                "frontend": 0, 
                "ml": 0,
                "deployment": 0,
                "docs": 0,
                "total": 0
            }
            
            # Count backend files
            backend_path = os.path.join(project_path, "backend")
            if os.path.exists(backend_path):
                for root, dirs, files in os.walk(backend_path):
                    counts["backend"] += len([f for f in files if not f.startswith('.')])
            
            # Count frontend files
            frontend_path = os.path.join(project_path, "frontend")
            if os.path.exists(frontend_path):
                for root, dirs, files in os.walk(frontend_path):
                    # Skip node_modules
                    if 'node_modules' in root:
                        continue
                    counts["frontend"] += len([f for f in files if not f.startswith('.')])
            
            # Count ML files
            ml_path = os.path.join(project_path, "ml")
            if os.path.exists(ml_path):
                for root, dirs, files in os.walk(ml_path):
                    counts["ml"] += len([f for f in files if not f.startswith('.')])
            
            # Count deployment files
            deployment_files = ["Dockerfile", "docker-compose.yml", ".env.example", "railway.json", "render.yaml"]
            for file_name in deployment_files:
                if os.path.exists(os.path.join(project_path, file_name)):
                    counts["deployment"] += 1
            
            # Count docs
            docs_files = ["README.md", "CONTRIBUTING.md", "LICENSE", "CHANGELOG.md"]
            for file_name in docs_files:
                if os.path.exists(os.path.join(project_path, file_name)):
                    counts["docs"] += 1
            
            counts["total"] = sum(counts.values()) - counts["total"]  # Exclude total from total
            
            logger.info(f"📊 Real file counts: Backend({counts['backend']}), Frontend({counts['frontend']}), ML({counts['ml']}), Deployment({counts['deployment']}), Total({counts['total']})")
            return counts
            
        except Exception as e:
            logger.error(f"File counting error: {e}")
            return {"backend": 0, "frontend": 0, "ml": 0, "deployment": 0, "docs": 0, "total": 0}
            
    async def _fast_validation_only(self, project_path: str, generated_files) -> ExecutionResult:
        """Fast validation without heavy dependency installation - for speed"""
        try:
            logger.info("⚡ FAST VALIDATION: Structure check only")
            
            # Quick file existence check
            required_files = [
                "backend/app/main.py",
                "backend/requirements.txt",
                "frontend/package.json",
                "frontend/src/App.tsx"
            ]
            
            missing_files = []
            for file_path in required_files:
                full_path = os.path.join(project_path, file_path)
                if not os.path.exists(full_path):
                    missing_files.append(file_path)
            
            if missing_files:
                logger.warning(f"⚠️ Missing files: {missing_files}")
                return ExecutionResult(
                    success=False,
                    errors=[f"Missing files: {', '.join(missing_files)}"],
                    health_status={"structure": False}
                )
            
            logger.info("✅ Fast validation passed - all essential files present")
            return ExecutionResult(
                success=True,
                health_status={
                    "structure": True,
                    "fast_mode": True,
                    "note": "Dependencies not installed for speed"
                }
            )
            
        except Exception as e:
            logger.error(f"Fast validation error: {e}")
            return ExecutionResult(success=False, errors=[str(e)])
    
    async def _emergency_recovery(self, dataset_path: str, user_prompt: str, error: str) -> GeneratedProject:
        """Emergency recovery with simplified generation"""
        logger.info("🆘 EMERGENCY RECOVERY MODE")
        
        # Create minimal working project
        project_id = f"recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_path = os.path.join(self.workspace_root, project_id)
        os.makedirs(project_path, exist_ok=True)
        
        # Generate minimal but working application
        minimal_project = await self.agents["engineer"].generate_minimal_working_app(
            dataset_path, user_prompt, project_path
        )
        
        return GeneratedProject(
            project_path=project_path,
            backend_files=minimal_project.get("backend_files", []),
            frontend_files=minimal_project.get("frontend_files", []),
            ml_files=minimal_project.get("ml_files", []),
            deployment_files=[],
            status="recovery_mode",
            errors=[error]
        )