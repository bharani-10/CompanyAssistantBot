"""
RAG system for question answering using LangChain
"""
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from typing import Dict, List, Tuple
import os
from knowledge_base import KNOWLEDGE_BASE, get_answer


class RAGSystem:
    """RAG system for answering questions based on company documents"""
    
    def __init__(
        self,
        vector_store: Chroma,
        llm_model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.7,
        api_key: str = None,
        llm_provider: str = "groq"
    ):
        self.vector_store = vector_store
        
        # Initialize LLM based on provider
        if llm_provider == "groq":
            self.llm = ChatGroq(
                model=llm_model,
                temperature=temperature,
                groq_api_key=api_key or os.getenv("GROQ_API_KEY")
            )
        elif llm_provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model=llm_model,
                temperature=temperature,
                google_api_key=api_key or os.getenv("GEMINI_API_KEY")
            )
        else:
            self.llm = ChatOpenAI(
                model_name=llm_model,
                temperature=temperature,
                openai_api_key=api_key or os.getenv("OPENAI_API_KEY"),
                streaming=True
            )
        
        # Create the prompt template
        self.prompt_template = """Use the following pieces of context to answer the user question. 
If you don't know the answer from the context provided, say "I don't have that information in the company documents."

Always cite which documents you used to answer the question.

Context:
{context}

Question: {question}

Answer:"""
    
    def answer_question(self, question: str) -> Tuple[str, List[Dict]]:
        """Answer a question and return the answer with source documents"""
        
        try:
            # First, try to get answer from knowledge base
            kb_result = get_answer(question)
            if kb_result["answer"] != "I don't have that information in the knowledge base.":
                # Found in knowledge base
                source_docs = [{
                    "source": kb_result.get("source", "Knowledge Base"),
                    "content": kb_result["answer"][:200] + "..." if len(kb_result["answer"]) > 200 else kb_result["answer"],
                    "page": "KB"
                }]
                return kb_result["answer"], source_docs
            
            # If not in knowledge base, search vector store
            docs = self.vector_store.similarity_search(question, k=3)
            
            # Prepare context from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Create prompt
            prompt = PromptTemplate(
                template=self.prompt_template,
                input_variables=["context", "question"]
            )
            
            # Format the prompt
            formatted_prompt = prompt.format(context=context, question=question)
            
            # Get answer from LLM
            answer = self.llm.invoke(formatted_prompt).content
            
            # Extract source documents
            source_docs = []
            for doc in docs:
                source_docs.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "page": str(doc.metadata.get("page", "0"))
                })
            
            return answer, source_docs
        
        except Exception as e:
            return f"Error processing question: {str(e)}", []
    
    def get_retriever(self):
        """Get the retriever for advanced usage"""
        return self.vector_store.as_retriever(search_kwargs={"k": 3})


def create_rag_system(
    vector_store: Chroma,
    llm_model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.7,
    api_key: str = None,
    llm_provider: str = "groq"
) -> RAGSystem:
    """Factory function to create a RAG system"""
    return RAGSystem(
        vector_store=vector_store,
        llm_model=llm_model,
        temperature=temperature,
        api_key=api_key,
        llm_provider=llm_provider
    )
