import os
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from dataclasses import dataclass
import json

@dataclass
class EvaluationResult:
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    feedback: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]

class RAGEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./database/vector_store")
        self.index = None
        self.documents = []
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        os.makedirs(self.vector_db_path, exist_ok=True)
        
        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        docs_path = os.path.join(self.vector_db_path, "documents.pkl")
        
        if os.path.exists(index_path) and os.path.exists(docs_path):
            self.index = faiss.read_index(index_path)
            with open(docs_path, 'rb') as f:
                self.documents = pickle.load(f)
        else:
            dimension = 384  # all-MiniLM-L6-v2 embedding dimension
            self.index = faiss.IndexFlatIP(dimension)
            self.documents = []
    
    def add_documents(self, texts: List[str], metadata: List[Dict] = None):
        if metadata is None:
            metadata = [{}] * len(texts)
        
        embeddings = self.model.encode(texts)
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        self.index.add(embeddings.astype('float32'))
        
        for i, text in enumerate(texts):
            self.documents.append({
                'text': text,
                'metadata': metadata[i]
            })
        
        self._save_vector_store()
    
    def _save_vector_store(self):
        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        docs_path = os.path.join(self.vector_db_path, "documents.pkl")
        
        faiss.write_index(self.index, index_path)
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        if self.index.ntotal == 0:
            return []
        
        query_embedding = self.model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx >= 0 and idx < len(self.documents):
                results.append({
                    'text': self.documents[idx]['text'],
                    'metadata': self.documents[idx]['metadata'],
                    'score': float(score)
                })
        
        return results
    
    def calculate_similarity_score(self, text1: str, text2: str) -> float:
        embeddings = self.model.encode([text1, text2])
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        similarity = np.dot(embeddings[0], embeddings[1])
        return float(similarity)
    
    def evaluate_cv_against_job(self, cv_sections: Dict[str, str], job_description: str, job_requirements: str) -> EvaluationResult:
        job_context = f"Job Description: {job_description}\n\nRequirements: {job_requirements}"
        
        skills_score = self._evaluate_skills_match(cv_sections.get('skills', ''), job_requirements)
        
        experience_score = self._evaluate_experience_match(cv_sections.get('experience', ''), job_context)
        
        education_score = self._evaluate_education_match(cv_sections.get('education', ''), job_requirements)
        
        overall_score = (skills_score * 0.4 + experience_score * 0.4 + education_score * 0.2)
        
        strengths, weaknesses, recommendations = self._generate_detailed_feedback(
            cv_sections, job_context, skills_score, experience_score, education_score
        )
        
        feedback = self._generate_summary_feedback(overall_score, strengths, weaknesses)
        
        return EvaluationResult(
            overall_score=round(overall_score, 1),
            skills_score=round(skills_score, 1),
            experience_score=round(experience_score, 1),
            education_score=round(education_score, 1),
            feedback=feedback,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    def _evaluate_skills_match(self, cv_skills: str, job_requirements: str) -> float:
        if not cv_skills or not job_requirements:
            return 0.0
        
        similarity = self.calculate_similarity_score(cv_skills, job_requirements)
        return min(100.0, max(0.0, similarity * 100))
    
    def _evaluate_experience_match(self, cv_experience: str, job_context: str) -> float:
        if not cv_experience or not job_context:
            return 0.0
        
        similarity = self.calculate_similarity_score(cv_experience, job_context)
        return min(100.0, max(0.0, similarity * 100))
    
    def _evaluate_education_match(self, cv_education: str, job_requirements: str) -> float:
        if not cv_education:
            return 50.0  # Neutral score if no education provided
        
        if not job_requirements:
            return 70.0  # Default score if no specific education requirements
        
        similarity = self.calculate_similarity_score(cv_education, job_requirements)
        return min(100.0, max(30.0, similarity * 100))
    
    def _generate_detailed_feedback(self, cv_sections: Dict[str, str], job_context: str, 
                                  skills_score: float, experience_score: float, education_score: float):
        strengths = []
        weaknesses = []
        recommendations = []
        
        if skills_score >= 70:
            strengths.append("Strong technical skills alignment with job requirements")
        elif skills_score < 50:
            weaknesses.append("Limited technical skills match with job requirements")
            recommendations.append("Consider highlighting transferable skills or gaining additional technical competencies")
        
        if experience_score >= 70:
            strengths.append("Relevant professional experience for the role")
        elif experience_score < 50:
            weaknesses.append("Limited relevant professional experience")
            recommendations.append("Emphasize transferable experience and achievements from related roles")
        
        if education_score >= 70:
            strengths.append("Educational background aligns well with job requirements")
        elif education_score < 50:
            weaknesses.append("Educational qualifications may not fully match job requirements")
            recommendations.append("Consider pursuing additional certifications or training")
        
        if len(cv_sections.get('skills', '')) < 100:
            recommendations.append("Expand the skills section with more specific technical competencies")
        
        if len(cv_sections.get('experience', '')) < 200:
            recommendations.append("Provide more detailed descriptions of work experience and achievements")
        
        return strengths, weaknesses, recommendations
    
    def _generate_summary_feedback(self, overall_score: float, strengths: List[str], weaknesses: List[str]) -> str:
        if overall_score >= 80:
            summary = "Excellent candidate with strong alignment to job requirements."
        elif overall_score >= 65:
            summary = "Good candidate with solid qualifications for the role."
        elif overall_score >= 50:
            summary = "Moderate candidate with some relevant qualifications."
        else:
            summary = "Limited alignment with job requirements."
        
        feedback_parts = [summary]
        
        if strengths:
            feedback_parts.append(f"Key strengths: {', '.join(strengths)}")
        
        if weaknesses:
            feedback_parts.append(f"Areas for improvement: {', '.join(weaknesses)}")
        
        return " ".join(feedback_parts)