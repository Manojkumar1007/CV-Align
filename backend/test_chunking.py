#!/usr/bin/env python3
"""
Test script for chunking functionality in CV-Align RAG system.
"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.document_processor import DocumentProcessor
from app.services.rag_engine import RAGEngine


def test_chunking():
    """Test the chunking functionality with sample text."""
    print("Testing chunking functionality...")
    
    # Sample CV text
    sample_cv_text = """
    John Doe
    Software Engineer
    john.doe@email.com | (123) 456-7890
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5+ years in web development and cloud technologies.
    Expertise in Python, JavaScript, and modern frameworks.
    
    EXPERIENCE
    Senior Software Engineer | Tech Corp | 2020-Present
    Developed and maintained web applications using Python and JavaScript.
    Implemented CI/CD pipelines that reduced deployment time by 40%.
    Led a team of 4 junior developers and mentored them on best practices.
    
    Software Engineer | Startup Inc | 2018-2020
    Built responsive web applications using React and Node.js.
    Implemented database solutions with PostgreSQL and MongoDB.
    Optimized application performance resulting in 30% faster load times.
    
    EDUCATION
    Bachelor of Science in Computer Science | University of Tech | 2018
    Magna Cum Laude, Dean's List, Computer Science Club President
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Frameworks: React, Node.js, Django, Flask
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, Docker, Kubernetes
    Tools: Git, Jenkins, Jira
    """
    
    processor = DocumentProcessor()
    
    # Test basic text chunking
    print("\n1. Testing basic text chunking...")
    chunks = processor.chunk_text_with_langchain(sample_cv_text, chunk_size=200, chunk_overlap=20)
    print(f"Generated {len(chunks)} chunks from sample text")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1} ({len(chunk)} chars): {chunk[:60]}...")
    
    # Test CV section chunking
    print("\n2. Testing CV section chunking...")
    cv_sections = processor.extract_cv_sections(sample_cv_text)
    print(f"Extracted sections: {list(cv_sections.keys())}")
    
    cv_chunks = processor.chunk_cv_sections_with_langchain(cv_sections)
    print(f"Generated {len(cv_chunks)} section chunks with metadata:")
    for i, chunk in enumerate(cv_chunks):
        print(f"  Chunk {i+1}: section='{chunk['metadata']['section']}', "
              f"chunk_id={chunk['metadata']['chunk_id']}, "
              f"size={len(chunk['text'])} chars")
        print(f"    Content preview: {chunk['text'][:60]}...")
    
    # Test RAG engine with chunks
    print("\n3. Testing RAG engine integration...")
    rag_engine = RAGEngine(embedding_model_name="embeddinggemma:300m", generation_model_name="gemma:4b")
    
    # Add the chunks to the RAG engine
    rag_engine.add_cv_chunks(cv_chunks)
    print(f"Added {len(cv_chunks)} chunks to RAG engine")
    print(f"Vector store now has {rag_engine.index.ntotal} embeddings")
    
    # Test search functionality
    print("\n4. Testing search functionality...")
    search_results = rag_engine.search_cv_chunks("web development", k=3, section_filter='experience')
    print(f"Found {len(search_results)} relevant chunks for 'web development' in experience section")
    for i, result in enumerate(search_results):
        print(f"  Result {i+1} (score: {result['score']:.3f}): {result['text'][:60]}...")
    
    # Test RAG-based evaluation
    print("\n5. Testing RAG-enhanced evaluation...")
    job_description = "We are looking for a senior software engineer with experience in Python, web development, and cloud technologies."
    job_requirements = "5+ years of experience, proficiency in Python, JavaScript, and modern frameworks, experience with cloud platforms"
    
    evaluation_result = rag_engine.evaluate_cv_with_rag_context(
        cv_sections, job_description, job_requirements
    )
    
    print(f"Evaluation completed!")
    print(f"  Overall Score: {evaluation_result.overall_score}")
    print(f"  Skills Score: {evaluation_result.skills_score}")
    print(f"  Experience Score: {evaluation_result.experience_score}")
    print(f"  Education Score: {evaluation_result.education_score}")
    print(f"  Feedback: {evaluation_result.feedback[:100]}...")

    # Test new soft skills evaluation
    print("\n6. Testing soft skills evaluation with LLM...")
    try:
        soft_skills_score = rag_engine.get_soft_skills_score(cv_sections, job_description)
        print(f"✓ Soft skills score: {soft_skills_score}")

        # Test contextual evaluation
        context_score = rag_engine.get_contextual_score(cv_sections, job_description, job_requirements)
        print(f"✓ Contextual understanding score: {context_score}")
    except Exception as e:
        print(f"✗ Error in soft skills evaluation: {e}")

    print("\nChunking functionality test completed successfully!")


if __name__ == "__main__":
    test_chunking()