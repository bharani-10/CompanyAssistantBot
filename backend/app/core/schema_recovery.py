"""
Schema Recovery and JSON Repair System for MetaMind OS
Ensures fault-tolerant Pydantic validation with self-healing capabilities
"""
import json
import logging
from typing import Dict, Any, Optional, Type, Union
from pydantic import BaseModel, ValidationError

logger = logging.getLogger("metamind.recovery")

class SchemaRecoveryEngine:
    """Self-healing schema validation and repair system"""
    
    @staticmethod
    def repair_missing_fields(data: Dict[str, Any], model_class: Type[BaseModel]) -> Dict[str, Any]:
        """Repair missing fields in data to match Pydantic model requirements"""
        try:
            # Get model field defaults
            model_fields = model_class.__fields__
            repaired_data = data.copy()
            
            for field_name, field_info in model_fields.items():
                if field_name not in repaired_data:
                    # Inject default value
                    if hasattr(field_info, 'default') and field_info.default is not None:
                        repaired_data[field_name] = field_info.default
                    elif hasattr(field_info, 'default_factory') and field_info.default_factory is not None:
                        repaired_data[field_name] = field_info.default_factory()
                    else:
                        # Inject safe defaults based on field type
                        repaired_data[field_name] = SchemaRecoveryEngine._get_safe_default(field_name)
            
            logger.info(f"🔧 Repaired {len(repaired_data) - len(data)} missing fields for {model_class.__name__}")
            return repaired_data
            
        except Exception as e:
            logger.error(f"Field repair failed: {e}")
            return data
    
    @staticmethod
    def _get_safe_default(field_name: str) -> Any:
        """Get safe default values for common field types"""
        defaults = {
            "ml_pipeline": {
                "preprocessing": {"steps": ["StandardScaling"]},
                "model_selection": {"algorithms": ["RandomForest"]},
                "evaluation": {"metrics": ["accuracy"]}
            },
            "backend_architecture": {
                "framework": "FastAPI",
                "structure": {"routers": ["prediction"], "services": ["ml_service"]},
                "endpoints": {"prediction": "/predict", "health": "/health"}
            },
            "frontend_architecture": {
                "framework": "React",
                "styling": "TailwindCSS",
                "components": {"pages": ["Dashboard"], "ui": ["PredictionForm"]}
            },
            "api_endpoints": [
                {"path": "/predict", "method": "POST", "description": "Single prediction"},
                {"path": "/health", "method": "GET", "description": "Health check"}
            ],
            "database_schema": {
                "tables": [],
                "storage": "filesystem",
                "type": "SQLite"
            },
            "deployment_strategy": {
                "containerization": "Docker",
                "cloud_platforms": ["Hugging Face Spaces"],
                "monitoring": "Built-in health checks"
            },
            "technology_stack": {
                "backend": ["FastAPI", "Uvicorn", "Pydantic"],
                "ml": ["scikit-learn", "pandas", "numpy"],
                "frontend": ["React", "TypeScript", "TailwindCSS"],
                "deployment": ["Docker"]
            },
            "scalability_plan": {
                "auto_scaling": True,
                "load_balancing": False
            }
        }
        
        return defaults.get(field_name, {})
    
    @staticmethod
    def safe_parse_json(json_str: str) -> Dict[str, Any]:
        """Safely parse JSON with error recovery"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            
            # Try to repair common JSON issues
            repaired_json = SchemaRecoveryEngine._repair_malformed_json(json_str)
            try:
                return json.loads(repaired_json)
            except:
                logger.error("JSON repair failed, returning minimal structure")
                return {"status": "partial", "error": "malformed_json"}
    
    @staticmethod
    def _repair_malformed_json(json_str: str) -> str:
        """Attempt to repair common JSON formatting issues"""
        try:
            # Remove trailing commas
            repaired = json_str.replace(',}', '}').replace(',]', ']')
            
            # Fix missing quotes around keys
            import re
            repaired = re.sub(r'(\w+):', r'"\1":', repaired)
            
            # Ensure proper closing braces
            open_braces = repaired.count('{')
            close_braces = repaired.count('}')
            if open_braces > close_braces:
                repaired += '}' * (open_braces - close_braces)
            
            return repaired
        except:
            return '{"status": "repair_failed"}'
    
    @staticmethod
    def safe_parse_model(data: Union[str, Dict[str, Any]], model_class: Type[BaseModel], max_retries: int = 3) -> BaseModel:
        """Safely parse data into Pydantic model with automatic recovery"""
        
        # Convert string to dict if needed
        if isinstance(data, str):
            data = SchemaRecoveryEngine.safe_parse_json(data)
        
        for attempt in range(max_retries):
            try:
                # Attempt direct parsing
                return model_class(**data)
                
            except ValidationError as e:
                logger.warning(f"Validation attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    # Repair missing fields and retry
                    data = SchemaRecoveryEngine.repair_missing_fields(data, model_class)
                    logger.info(f"🔧 Attempting repair and retry {attempt + 2}/{max_retries}")
                else:
                    # Final attempt with fallback defaults
                    logger.error(f"All validation attempts failed, using fallback defaults")
                    return SchemaRecoveryEngine._create_fallback_model(model_class)
            
            except Exception as e:
                logger.error(f"Unexpected error during parsing: {e}")
                return SchemaRecoveryEngine._create_fallback_model(model_class)
        
        # Should never reach here, but safety fallback
        return SchemaRecoveryEngine._create_fallback_model(model_class)
    
    @staticmethod
    def _create_fallback_model(model_class: Type[BaseModel]) -> BaseModel:
        """Create a fallback model instance with safe defaults"""
        try:
            # Try to create with empty dict (will use model defaults)
            return model_class()
        except:
            # If that fails, create with minimal required fields
            if model_class.__name__ == "SystemArchitecture":
                return model_class(
                    ml_pipeline={
                        "algorithm": "RandomForest",
                        "preprocessing": {"steps": ["StandardScaling"]},
                        "evaluation": {"metrics": ["accuracy"]}
                    },
                    backend_architecture={
                        "framework": "FastAPI",
                        "endpoints": {"prediction": "/predict", "health": "/health"}
                    },
                    frontend_architecture={
                        "framework": "React",
                        "styling": "TailwindCSS"
                    },
                    api_endpoints=[
                        {"path": "/predict", "method": "POST", "description": "Single prediction"}
                    ],
                    database_schema={
                        "tables": [],
                        "storage": "filesystem",
                        "type": "SQLite"
                    },
                    deployment_strategy={
                        "containerization": "Docker",
                        "cloud_platforms": ["Hugging Face Spaces"]
                    },
                    technology_stack={
                        "backend": ["FastAPI", "Uvicorn"],
                        "ml": ["scikit-learn", "pandas"],
                        "frontend": ["React", "TypeScript"]
                    },
                    scalability_plan={
                        "auto_scaling": True,
                        "load_balancing": False
                    }
                )
            else:
                # Generic fallback for other models
                try:
                    # Try with empty kwargs
                    return model_class(**{})
                except:
                    # Last resort - create with None values for all fields
                    field_defaults = {}
                    for field_name, field_info in model_class.__fields__.items():
                        field_defaults[field_name] = None
                    return model_class(**field_defaults)

# Global recovery engine instance
recovery_engine = SchemaRecoveryEngine()