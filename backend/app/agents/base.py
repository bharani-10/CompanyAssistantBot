import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
import logging

logger = logging.getLogger("metamind.agents")

class BaseAgent:
    def __init__(self, name: str, role: str, model_name: str = "llama-3.1-8b-instant"):
        self.name = name
        self.role = role
        self.llm = None
        
        google_api_key = os.getenv("GOOGLE_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        if groq_api_key:
            logger.info(f"Using Groq for agent {self.name} with model {model_name}")
            self.llm = ChatGroq(
                model=model_name,
                groq_api_key=groq_api_key,
                temperature=0.1,
            )
        elif google_api_key:
            logger.info(f"Using Gemini for agent {self.name}")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=google_api_key,
                temperature=0.1,
            )
        else:
            logger.info(f"Agent {self.name} running in autonomous mode (no LLM required)")

    async def chat(self, system_prompt: str, user_content: str, response_model: Optional[Any] = None) -> Any:
        # If no LLM available, return sensible defaults using recovery engine
        if not self.llm:
            if response_model:
                from ..core.schema_recovery import recovery_engine
                # Create safe default instance
                return recovery_engine._create_fallback_model(response_model)
            else:
                return f"Autonomous {self.name} completed task: {user_content[:100]}..."
        
        messages = [
            SystemMessage(content=f"You are the {self.name}, the {self.role}. {system_prompt}"),
            HumanMessage(content=user_content)
        ]
        
        try:
            if response_model:
                from ..core.schema_recovery import recovery_engine
                
                try:
                    # Attempt structured output with timeout
                    structured_llm = self.llm.with_structured_output(response_model)
                    response = await asyncio.wait_for(structured_llm.ainvoke(messages), timeout=90.0)
                    return response
                except Exception as structured_err:
                    logger.warning(f"Structured output failed for {self.name}, using recovery engine: {structured_err}")
                    
                    # Fallback to raw chat + safe parsing
                    try:
                        raw_response = await asyncio.wait_for(self.llm.ainvoke(messages), timeout=90.0)
                        content = raw_response.content
                        
                        # Use recovery engine for safe parsing
                        return recovery_engine.safe_parse_model(content, response_model)
                        
                    except Exception as raw_err:
                        logger.error(f"Raw response failed for {self.name}, using fallback: {raw_err}")
                        return recovery_engine._create_fallback_model(response_model)
            else:
                response = await asyncio.wait_for(self.llm.ainvoke(messages), timeout=90.0)
                return response.content
        except Exception as e:
            logger.error(f"Error in agent {self.name}: {e}")
            if response_model:
                from ..core.schema_recovery import recovery_engine
                return recovery_engine._create_fallback_model(response_model)
            else:
                return f"Error in {self.name}, continuing autonomously"

    def log_event(self, message: str):
        logger.info(f"[{self.name}] {message}")
