from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseAgent
from .analyst import AnalysisResult

class ModelDossier(BaseModel):
    name: str = "Standard Model"
    rank: int = 1
    accuracy_forecast: float = 0.8
    explainability_score: float = 0.7
    complexity: str = "Medium"
    latency: str = "Low"
    risk_level: str = "Minimal"
    strengths: List[str] = []
    weaknesses: List[str] = []
    why_chosen: str = "Reliable baseline model."
    why_rejected: Optional[str] = None

class PipelineStep(BaseModel):
    step_name: str = "preprocessing"
    description: str = "Standard preprocessing step"

class WorkflowPlan(BaseModel):
    models: List[ModelDossier] = []
    pipeline_steps: List[PipelineStep] = []
    feature_engineering_plan: str = "Standard scaling and imputation."
    evaluation_metric: str = "accuracy"
    strategic_reasoning: str = "Optimizing for stability and explainability."

class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Architect Agent",
            role="System Architect who designs optimized machine learning pipelines."
        )

    async def design_pipeline(self, analysis: AnalysisResult) -> WorkflowPlan:
        self.log_event("Designing ML pipeline architecture...")
        
        system_prompt = """
        Based on the Analyst's findings, design a comprehensive ML strategy.
        Select at least 2 candidate algorithms to compare.
        For each, create a ModelDossier containing:
        - rank (1 for best, 2 for alt)
        - accuracy_forecast (0.0 - 1.0)
        - explainability_score (0.0 - 1.0)
        - complexity, latency, risk_level
        - strengths, weaknesses
        - why_chosen / why_rejected
        
        Also define pipeline_steps as a list of PipelineStep objects with step_name and description.
        """

        user_content = f"""
        Analysis Summary: {analysis.summary}
        Problem Type: {analysis.problem_type}
        Target Column: {analysis.target_column}
        Features: {", ".join(analysis.features)}
        
        Provide a structured WorkflowPlan with the Best Model ranked as 1.
        """

        result = await self.chat(system_prompt, user_content, response_model=WorkflowPlan)
        self.log_event(f"Architecture designed with {len(result.models)} candidate models.")
        return result
