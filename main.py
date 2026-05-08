"""
FastAPI backend for the RAG chatbot
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Company Assistant Chatbot API",
    description="RAG-based chatbot for company policy questions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy global variables
vector_store = None
rag_system = None


# Pydantic models
class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]


class HealthResponse(BaseModel):
    status: str
    message: str


# SIMPLE STARTUP
@app.on_event("startup")
async def startup_event():
    logger.info("App started successfully")


# ROOT ROUTE
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Company Assistant Chatbot API is running successfully",
        "docs": "/docs"
    }


# HEALTH CHECK
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="healthy",
        message="Backend is running"
    )


# TEMP CHAT ROUTE
@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):

    return ChatResponse(
        answer=f"You asked: {request.question}",
        sources=[]
    )


# DOCUMENTS ROUTE
@app.get("/documents", tags=["Documents"])
async def get_documents_info():

    return {
        "total_chunks": 0,
        "status": "Backend running successfully"
    }


# MAIN
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 10000))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )