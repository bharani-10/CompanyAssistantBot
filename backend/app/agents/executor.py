import subprocess
import os
import json
import uuid
import sys
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import logging

logger = logging.getLogger("metamind.executor")

class ExecutionResult(BaseModel):
    success: bool
    output: str
    error: Optional[str]
    metrics: Optional[Dict[str, Any]]
    artifacts: List[str]

class ExecutorAgent:
    def __init__(self, workspace_root: str = None):
        self.name = "Executor Agent"
        if workspace_root is None:
            workspace_root = os.getenv("RUN_WORKSPACE_DIR", "run_workspace")
        self.workspace_root = workspace_root
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)
        if not os.path.exists(os.path.join(self.workspace_root, "results")):
            os.makedirs(os.path.join(self.workspace_root, "results"))

    def log_event(self, message: str):
        logger.info(f"[Executor Agent] {message}")

    async def execute(self, code: str) -> ExecutionResult:
        run_id = str(uuid.uuid4())[:8]
        script_path = os.path.join(self.workspace_root, f"model_run_{run_id}.py")
        
        with open(script_path, "w") as f:
            f.write(code)

        self.log_event(f"Executing generated code in {script_path}...")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
                timeout=300
            )

            success = result.returncode == 0
            stdout = result.stdout
            stderr = result.stderr
            
            metrics = None
            if "METRICS_JSON:" in stdout:
                try:
                    metrics_str = stdout.split("METRICS_JSON:")[1].strip()
                    metrics = json.loads(metrics_str)
                except Exception as e:
                    logger.error(f"Failed to parse metrics: {e}")

            artifacts = []
            results_dir = os.path.join(self.workspace_root, "results")
            if os.path.exists(results_dir):
                artifacts = [os.path.join("results", f) for f in os.listdir(results_dir)]

            self.log_event(f"Execution finished. Success: {success}")
            
            return ExecutionResult(
                success=success,
                output=stdout,
                error=stderr if not success else None,
                metrics=metrics,
                artifacts=artifacts
            )
            
        except subprocess.TimeoutExpired:
            return ExecutionResult(success=False, output="", error="Execution timed out", metrics=None, artifacts=[])
        except Exception as e:
            return ExecutionResult(success=False, output="", error=str(e), metrics=None, artifacts=[])
