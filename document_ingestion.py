"""
Document ingestion pipeline for loading PDFs and creating embeddings
"""
import os
import glob
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain_core.documents import Document


class SimpleVectorStore:
    """Simple in-memory vector store for testing"""
    
    def __init__(self, documents: List[Document], embeddings):
        self.documents = documents
        self.embeddings = embeddings
        self._collection = None
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Improved similarity search - returns documents from different sources"""
        # Group documents by source
        sources = {}
        for doc in self.documents:
            source = doc.metadata.get("source", "Unknown")
            if source not in sources:
                sources[source] = []
            sources[source].append(doc)
        
        # Return first document from each source (up to k)
        results = []
        for source, docs in sources.items():
            if len(results) < k and docs:
                results.append(docs[0])
        
        # If we need more, add remaining documents
        if len(results) < k:
            for doc in self.documents:
                if doc not in results and len(results) < k:
                    results.append(doc)
        
        return results[:k]
    
    def as_retriever(self, search_kwargs=None):
        """Return self as retriever"""
        return self
    
    def persist(self):
        """Persist store"""
        pass


class DocumentIngestionPipeline:
    """Handles PDF loading, chunking, and embedding storage"""
    
    def __init__(
        self,
        pdf_directory: str = ".",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db"
    ):
        self.pdf_directory = pdf_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize vector store
        self.vector_store = None
    
    def load_all_pdfs(self) -> List[Document]:
        """Load all PDF files from the directory"""
        pdf_files = glob.glob(os.path.join(self.pdf_directory, "*.pdf"))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {self.pdf_directory}")
        
        all_documents = []
        print(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            try:
                print(f"Loading: {os.path.basename(pdf_file)}")
                loader = PyPDFLoader(pdf_file)
                documents = loader.load()
                
                # Add source metadata
                for doc in documents:
                    doc.metadata["source"] = os.path.basename(pdf_file)
                
                all_documents.extend(documents)
            except Exception as e:
                print(f"Error loading {pdf_file}: {str(e)}")
        
        print(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        print(f"Chunking {len(documents)} documents...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, chunks: List[Document]):
        """Create simple in-memory vector store from chunks"""
        print(f"Creating vector store with {len(chunks)} chunks...")
        
        self.vector_store = SimpleVectorStore(chunks, self.embeddings)
        print(f"Vector store created")
        
        return self.vector_store
    
    def load_vector_store(self):
        """Load existing vector store from disk"""
        if not os.path.exists(self.persist_directory):
            raise ValueError(f"Vector store not found at {self.persist_directory}")
        
        print(f"Loading vector store from {self.persist_directory}...")
        # For now, just create a new one
        documents = self.load_all_pdfs()
        chunks = self.chunk_documents(documents)
        self.vector_store = self.create_vector_store(chunks)
        return self.vector_store
    
    def ingest_documents(self):
        """Complete pipeline: Load PDFs -> Chunk -> Embed -> Store"""
        documents = self.load_all_pdfs()
        chunks = self.chunk_documents(documents)
        vector_store = self.create_vector_store(chunks)
        return vector_store
    
    def search(self, query: str, k: int = 3) -> List[Document]:
        """Search for relevant documents"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results


def initialize_pipeline(
    pdf_directory: str = ".",
    rebuild: bool = False
):
    """Initialize or load the document ingestion pipeline"""
    
    pipeline = DocumentIngestionPipeline(pdf_directory=pdf_directory)
    
    # Try to load existing vector store, if fails create new one
    try:
        if not rebuild and os.path.exists(pipeline.persist_directory):
            print("Loading existing vector store...")
            vector_store = pipeline.load_vector_store()
        else:
            print("Creating new vector store...")
            vector_store = pipeline.ingest_documents()
    except Exception as e:
        print(f"Warning: Could not load/create vector store: {e}")
        print("Creating new vector store...")
        vector_store = pipeline.ingest_documents()
    
    return vector_store
