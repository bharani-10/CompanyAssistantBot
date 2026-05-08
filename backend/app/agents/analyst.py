import pandas as pd
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .base import BaseAgent

class ColumnInfo(BaseModel):
    name: str = "Unknown"
    dtype: str = "Object"
    missing_values_pct: float = 0.0
    unique_values: int = 0
    quality_score: float = 1.0
    recommendation: str = "No issues detected."

class AnalysisResult(BaseModel):
    problem_type: str = "regression"
    target_column: str = "target"
    target_recommendation: str = "MetaMind has identified this target as the optimal predictive objective."
    features: List[str] = []
    summary: str = "Initial scan complete."
    columns_info: List[ColumnInfo] = []
    rows: int = 0
    data_quality_score: float = 1.0
    correlation_map: Dict[str, Dict[str, float]] = {}

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Analyst Agent",
            role="Expert Data Scientist focused on exploratory data analysis and feature identification."
        )

    async def analyze_dataset(self, df: pd.DataFrame, user_instruction: str) -> AnalysisResult:
        self.log_event("Starting dataset analysis...")
        
        schema_info = []
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        corr_map = {}
        
        # Calculate a subset correlation for the UI heatmap
        if len(numeric_cols) > 1:
            corr_map = df[numeric_cols].corr().to_dict()

        for col in df.columns:
            null_pct = float(df[col].isna().mean())
            schema_info.append({
                "name": col,
                "dtype": str(df[col].dtype),
                "null_pct": null_pct,
                "unique": int(df.nunique()[col]),
                "sample": df[col].dropna().head(2).tolist()
            })

        system_prompt = """
        Your task is to analyze the provided dataset schema and a user instruction to identify:
        1. The type of ML problem (classification/regression/clustering).
        2. The target column (if applicable).
        3. The most relevant features.
        4. Cleaning recommendations for each column.
        """

        user_content = f"""
        User Instruction: "{user_instruction}"
        
        Dataset Preview (First 5 rows):
        {df.head().to_markdown()}
        
        Column Statistics:
        {json.dumps(schema_info, indent=2)}
        
        Based on this, return a structured AnalysisResult.
        """

        result = await self.chat(system_prompt, user_content, response_model=AnalysisResult)
        result.rows = len(df)
        result.correlation_map = corr_map
        result.data_quality_score = max(0.0, 1.0 - df.isna().mean().mean())
        self.log_event(f"Analysis complete. Data Quality: {result.data_quality_score:.2f}")
        return result
