from pydantic import BaseModel, Field
from .base import BaseAgent
from .analyst import AnalysisResult
from .architect import WorkflowPlan, PipelineStep

class GeneratedCode(BaseModel):
    python_code: str = Field(default="", description="Executable Python code using scikit-learn, pandas, etc.")
    explanation: str = "No explanation provided."

class EngineerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Engineer Agent",
            role="Expert ML Engineer who writes clean, production-ready Python code."
        )

    async def generate_code(self, analysis: AnalysisResult, plan: WorkflowPlan, dataset_path: str) -> GeneratedCode:
        self.log_event("Generating model code...")

        system_prompt = f"""
        Write a complete Python script to execute the designed ML pipeline.
        
        MANDATORY IMPORTS:
        ```python
        import pandas as pd
        import numpy as np
        import json
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.impute import SimpleImputer
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
        from joblib import dump
        import os
        ```

        REQUIREMENTS:
        - Mode: {analysis.problem_type}
        - Load dataset from '{dataset_path}'
        - Create results directory if it doesn't exist
        - Save metrics JSON prefixed with 'METRICS_JSON:' to stdout
        - Save plots to 'results/' directory
        - Save trained model to 'results/trained_model.joblib'
        
        Keep the code simple and focused. Don't use SHAP for now.
        """

        user_content = f"""
        Dataset Info: {analysis.columns_info}
        Target Column: {analysis.target_column}
        Problem Type: {analysis.problem_type}
        Features: {analysis.features}
        
        Generate clean, executable Python code for this ML task.
        """

        try:
            result = await self.chat(system_prompt, user_content, response_model=GeneratedCode)
            if not result.python_code.strip():
                # Fallback: generate without structured output
                raw_result = await self.chat(system_prompt, user_content + "\n\nReturn only the Python code, no explanations.", response_model=None)
                result = GeneratedCode(
                    python_code=raw_result,
                    explanation="Generated via fallback method"
                )
        except Exception as e:
            self.log_event(f"Structured generation failed: {e}")
            # Fallback: generate without structured output
            raw_result = await self.chat(system_prompt, user_content + "\n\nReturn only the Python code, no explanations.", response_model=None)
            result = GeneratedCode(
                python_code=raw_result,
                explanation="Generated via fallback method"
            )
        
        self.log_event("Code generation complete.")
        return result
