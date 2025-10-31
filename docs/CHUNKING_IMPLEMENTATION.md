# RAG Chunking Implementation in CV-Align

## Overview
This document explains where and how chunking is implemented in the CV-Align RAG system for better contextual retrieval and evaluation of CVs.

## Where Chunking Happens

### 1. Document Processor (`backend/app/services/document_processor.py`)
- **`chunk_text_with_langchain()`**: Core function that splits text using LangChain's RecursiveCharacterTextSplitter
- **`chunk_cv_sections_with_langchain()`**: Specialized function for chunking CV sections while preserving metadata

### 2. LLM Service (`backend/app/services/llm_service.py`)
- **LangChain Integration**: Uses RecursiveCharacterTextSplitter for intelligent text splitting (versions: langchain==0.0.354, langchain-community==0.0.10, langchain-core==0.1.23)
- **Ollama Integration**: Uses embeddinggemma:300m model for embeddings via Ollama (ollama==0.6.0)

### 3. RAG Engine (`backend/app/services/rag_engine.py`)
- **`add_cv_chunks()`**: Function to add chunked content to the vector store with embeddingGemma embeddings
- **`search_cv_chunks()`**: Function to retrieve relevant chunks based on queries
- **`evaluate_cv_with_rag_context()`**: Enhanced evaluation using retrieved context

### 4. Evaluation Route (`backend/app/routes/evaluations.py`)
- The upload and evaluation endpoint now uses LangChain chunking and embeddingGemma embeddings for better RAG-based evaluation

## Prerequisites
- Ollama must be installed and running
- embeddinggemma:300m model must be pulled: `ollama pull embeddinggemma:300m`
- Default Ollama endpoint: `http://localhost:11434`

## How It Works

1. **Text Extraction**: CVs are extracted and sections are identified (skills, experience, education, etc.)

2. **Chunking Process**: 
   - Text is split using LangChain's RecursiveCharacterTextSplitter
   - Recursive splitting on ["\n\n", "\n", " ", ""] until chunks are within size limits
   - Default chunk size: 500 characters with 50 character overlap
   - Each chunk preserves its section context as metadata

3. **Embedding Process**:
   - Text chunks are converted to embeddings using embeddinggemma:300m via Ollama
   - Embeddings are stored in FAISS vector database with metadata

4. **RAG Retrieval**:
   - When evaluating CVs, relevant chunks are retrieved based on job requirements
   - Retrieved context enhances the evaluation accuracy

5. **Evaluation Enhancement**:
   - The system now has access to specific, relevant parts of the CV during evaluation
   - This provides more targeted and accurate scoring

## Configuration
- Chunk size: Default 500 characters, adjustable in function calls
- Overlap: Default 50 characters, helps maintain context
- Model: Default embeddinggemma:300m, configurable in service initialization
- Section filtering: Ability to search specific CV sections (skills, experience, etc.)

## Benefits
- Better semantic retrieval compared to full-document processing
- More accurate CV-to-job matching using embeddingGemma embeddings
- Scalable processing of large documents with LangChain's advanced splitting
- Maintained context through metadata
- Local inference with Ollama for privacy and performance