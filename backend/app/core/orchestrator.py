import asyncio
import pandas as pd
from typing import Dict, Any, Callable, Awaitable
from ..agents.analyst import AnalystAgent
from ..agents.architect import ArchitectAgent
from ..agents.engineer import EngineerAgent
from ..agents.executor import ExecutorAgent
from ..agents.report_agents import EvaluatorAgent, CriticAgent, ExplainerAgent

class MetaMindOrchestrator:
    def __init__(self, on_status_update: Callable[[Dict[str, Any]], Awaitable[None]]):
        self.on_status_update = on_status_update
        self.analyst = AnalystAgent()
        self.architect = ArchitectAgent()
        self.engineer = EngineerAgent()
        self.executor = ExecutorAgent()
        self.evaluator = EvaluatorAgent()
        self.critic = CriticAgent()
        self.explainer = ExplainerAgent()

    async def _emit_status(self, agent: str, status: str, data: Any = None):
        await self.on_status_update({
            "agent": agent,
            "status": status,
            "data": data
        })

    async def run(self, dataset_path: str, instruction: str, retry_count: int = 0):
        try:
            await self._emit_status("SYSTEM", f"Swarm engaged. Initialization sequence: {'Standard' if retry_count == 0 else 'RECOVERY_MODE'}")
            
            # 1. Analyst
            await self._emit_status("Analyst Agent", "Scanning dataset structures...")
            df = pd.read_csv(dataset_path)
            analysis = await self.analyst.analyze_dataset(df, instruction)
            await self._emit_status("Analyst Agent", "Analysis complete", analysis.dict())

            # 2. Architect + Critic (Consensus Loop)
            await self._emit_status("Architect Agent", "Designing optimized architecture...")
            plan = await self.architect.design_pipeline(analysis)
            
            # CONSENSUS ENGINE: Critic validates the plan
            await self._emit_status("Critic Agent", "Critiquing architecture design...")
            critique = await self.critic.critique(analysis, plan)
            
            if not critique.is_valid and retry_count < 2:
                await self._emit_status("SYSTEM", "Consensus failed. Re-architecting...", {"critique": critique.dict()})
                return await self.run(dataset_path, f"{instruction} (Correction: {critique.reason})", retry_count + 1)

            await self._emit_status("Architect Agent", "Consensus reached. Architecture locked.", plan.dict())

            # 3. Engineer
            await self._emit_status("Engineer Agent", "Synthesizing production-grade code...")
            code_obj = await self.engineer.generate_code(analysis, plan, dataset_path)
            await self._emit_status("Engineer Agent", "Synthesis complete", code_obj.dict())

            # 4. Executor (Self-Healing)
            await self._emit_status("Executor Agent", "Deploying to secure runtime...")
            exec_result = await self.executor.execute(code_obj.python_code)
            
            if not exec_result.success:
                if retry_count < 2:
                    await self._emit_status("SYSTEM", f"Execution failed. Triggering Self-Healing (Attempt {retry_count + 1})...")
                    return await self.run(dataset_path, f"{instruction} (Note: Avoid error {exec_result.error})", retry_count + 1)
                
                await self._emit_status("Executor Agent", f"Fatal Error: {exec_result.error}", {"error": exec_result.error})
                return

            await self._emit_status("Executor Agent", "Model training successful", {
                "metrics": exec_result.metrics,
                "artifacts": exec_result.artifacts
            })

            # 5. Evaluator
            await self._emit_status("Evaluator Agent", "Evaluating performance...")
            evaluation = await self.evaluator.evaluate(exec_result.metrics or {})
            await self._emit_status("Evaluator Agent", "Evaluation complete", evaluation.dict())

            # 6. Explainer
            await self._emit_status("Explainer Agent", "Generating summary...")
            final_context = {
                "analysis": analysis.dict(),
                "plan": plan.dict(),
                "metrics": exec_result.metrics,
                "evaluation": evaluation.dict()
            }
            explanation = await self.explainer.explain(final_context)
            await self._emit_status("Explainer Agent", "All tasks complete", {"explanation": explanation})

            return {
                "status": "success",
                "analysis": analysis,
                "plan": plan,
                "metrics": exec_result.metrics,
                "explanation": explanation
            }
        except Exception as e:
            await self._emit_status("SYSTEM ERROR", str(e))
            print(f"CRITICAL ERROR in orchestrator: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # We want to make sure the UI knows we're done even on error
            await self._emit_status("SYSTEM", "PROCESS_FINISHED")
