#!/usr/bin/env python3
"""
Debug script for RAG engine with embeddingGemma
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_service import LLMService
from app.services.rag_engine import RAGEngine
import traceback

def debug_rag_engine():
    print("Starting RAG engine debug test...")
    
    try:
        # Test LLM service first
        print("1. Testing LLM Service...")
        llm_service = LLMService("embeddinggemma:300m")
        print("✓ LLM Service created successfully")
        
        # Test embedding generation
        print("2. Testing embedding generation...")
        embeddings = llm_service.embed_documents(["test document"])
        print(f"✓ Embeddings generated successfully, dimension: {len(embeddings[0]) if embeddings else 'N/A'}")
        
        # Test RAG engine
        print("3. Testing RAG Engine initialization...")
        rag_engine = RAGEngine("embeddinggemma:300m")
        print("✓ RAG Engine initialized successfully")
        
        # Test adding documents
        print("4. Testing document addition...")
        rag_engine.add_documents(["test document"])
        print("✓ Document added successfully")
        
        # Test search
        print("5. Testing search functionality...")
        results = rag_engine.search_similar("test")
        print(f"✓ Search completed, found {len(results)} results")
        
        print("\n✓ All tests passed! RAG engine is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_rag_engine()