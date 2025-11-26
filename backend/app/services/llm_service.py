from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import os

class LLMService:
    def __init__(self, embedding_model_name: str = "embeddinggemma:300m", generation_model_name: str = "gemma:4b"):
        self.embedding_model_name = embedding_model_name
        self.generation_model_name = generation_model_name
        
        # Initialize embeddings service
        self.embeddings = OllamaEmbeddings(
            model=embedding_model_name,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        
        # Initialize text generation service
        self.generator = Ollama(
            model=generation_model_name,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.2  # Lower temperature for more consistent evaluations
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def get_text_splitter(self, chunk_size: int = 500, chunk_overlap: int = 50):
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text using LangChain's text splitter
        """
        if not text.strip():
            return []
        return self.text_splitter.split_text(text)
    
    def embed_documents(self, texts: List[str]):
        """
        Generate embeddings for a list of documents using embeddingGemma via Ollama
        """
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, query: str):
        """
        Generate embedding for a single query using embeddingGemma via Ollama
        """
        return self.embeddings.embed_query(query)
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the LLM (e.g., Gemma) for evaluation tasks
        """
        return self.generator.invoke(prompt)
    
    def split_cv_sections(self, cv_sections: dict) -> List[dict]:
        """
        Split individual CV sections into chunks with metadata
        """
        chunks_with_metadata = []
        
        for section_name, section_text in cv_sections.items():
            if section_text and section_text.strip():
                section_chunks = self.split_text(section_text)
                
                for i, chunk in enumerate(section_chunks):
                    chunk_with_metadata = {
                        'text': chunk,
                        'metadata': {
                            'section': section_name,
                            'chunk_id': i,
                            'total_chunks': len(section_chunks)
                        }
                    }
                    chunks_with_metadata.append(chunk_with_metadata)
        
        return chunks_with_metadata