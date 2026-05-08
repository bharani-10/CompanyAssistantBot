import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .base import BaseAgent

class EvaluationResult(BaseModel):
    best_model: str = "Candidate Algorithm"
    performance_summary: str = "Evaluation pending."
    is_satisfactory: bool = Field(default=True, description="True if performance meets common standards")
    improvement_areas: List[str] = []
    confidence_score: float = Field(default=85.0, description="Score from 0-100 on how confident the swarm is in this result")

class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Evaluator Agent", "Quality Assurance Lead for Model Selection")

    async def evaluate(self, metrics: Dict[str, Any]) -> EvaluationResult:
        system_prompt = """
        Analyze the training metrics and select the best model. 
        Determine a 'Confidence Score' (0-100) based on the robustness of the data and the final metrics.
        """
        user_content = f"Training Results: {json.dumps(metrics, indent=2)}"
        return await self.chat(system_prompt, user_content, response_model=EvaluationResult)

class Criticism(BaseModel):
    weaknesses: List[str] = []
    actionable_suggestions: List[str] = []
    retry_recommended: bool = False

class CritiqueResult(BaseModel):
    is_valid: bool = True
    reason: str = "Plan satisfies architectural constraints."
    suggested_changes: List[str] = []

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("Critic Agent", "Lead Quality Control and Security Auditor")

    async def critique(self, analysis: Any, plan: Any) -> CritiqueResult:
        system_prompt = """
        Audit the proposed ML architecture and plan.
        You MUST return a JSON object with exactly these keys:
        - is_valid: (boolean) true if the plan is sound, false if it has errors.
        - reason: (string) explanation of your decision.
        - suggested_changes: (list of strings) specific fixes if is_valid is false.
        
        CRITICAL: Do NOT return the Plan itself. Return ONLY the CritiqueResult JSON.
        """
        user_content = f"Analysis Context: {analysis.json()}\nProposed Architecture to Audit: {plan.json()}"
        return await self.chat(system_prompt, user_content, response_model=CritiqueResult)

    async def criticize(self, evaluation: EvaluationResult, code: str, error: Optional[str] = None) -> Criticism:
        system_prompt = "Identify potential flaws in the model logic, feature engineering, or code structure. Suggest improvements."
        user_content = f"Evaluation: {evaluation.performance_summary}\nCode: {code}\nError (if any): {error}"
        return await self.chat(system_prompt, user_content, response_model=Criticism)

class ExplainerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Explainer Agent", "Technical Educator and Data Communicator")

    async def explain(self, all_data: Dict[str, Any]) -> str:
        system_prompt = """
        Generate a legendary executive-grade summary of the AI discovery mission.
        Your report must include TWO distinct sections.
        
        Section 1: # EXECUTIVE TL;DR (BEGINNER MODE)
        - Focus on "What this means for the business"
        - Explain why we chose this model in clear analogies.
        
        Section 2: # ARCHITECTURAL DEEP-DIVE (EXPERT MODE)
        - Detail the metrics (Accuracy, RMSE, etc.)
        - Discuss why this specific candidate model outperformed the others.
        - Discuss feature interactions.
        
        Use cinematic markdown with icons and bold headers.
        """
        user_content = f"Mission Lifecycle Data: {json.dumps(all_data, indent=2)}"
        return await self.chat(system_prompt, user_content)
