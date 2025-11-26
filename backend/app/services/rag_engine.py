import os
import numpy as np
import re
from typing import List, Dict, Any
import faiss
import pickle
from dataclasses import dataclass
import json
from .llm_service import LLMService
from .prompts import CV_EVALUATION_PROMPTS

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
    def __init__(self, embedding_model_name: str = "embeddinggemma:300m", generation_model_name: str = "gemma:4b"):
        self.llm_service = LLMService(embedding_model_name, generation_model_name)
        self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./database/vector_store")
        self.index = None
        self.documents = []
        # Initialize with a placeholder dimension, will be updated in _initialize_vector_store
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        os.makedirs(self.vector_db_path, exist_ok=True)

        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        docs_path = os.path.join(self.vector_db_path, "documents.pkl")

        if os.path.exists(index_path) and os.path.exists(docs_path):
            self.index = faiss.read_index(index_path)
            self.embedding_dimension = self.index.d  # Get dimension from existing index
            with open(docs_path, 'rb') as f:
                self.documents = pickle.load(f)
        else:
            # Use a sample embedding to determine the correct dimension
            sample_embedding = self.llm_service.embed_query("sample text")
            self.embedding_dimension = len(sample_embedding)
            print(f"Initialized FAISS index with embedding dimension: {self.embedding_dimension}")
            self.index = faiss.IndexFlatIP(self.embedding_dimension)
            self.documents = []

    def add_documents(self, texts: List[str], metadata: List[Dict] = None):
        if metadata is None:
            metadata = [{}] * len(texts)

        # Generate embeddings using Ollama with embeddingGemma
        embeddings = self.llm_service.embed_documents(texts)
        embeddings = np.array(embeddings)
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

        self.index.add(embeddings.astype('float32'))

        for i, text in enumerate(texts):
            self.documents.append({
                'text': text,
                'metadata': metadata[i]
            })

        self._save_vector_store()

    def add_cv_chunks(self, cv_chunks: List[Dict[str, str]]):
        """
        Add chunked CV content to the vector store with appropriate metadata.

        Args:
            cv_chunks: List of dictionaries containing 'text' and 'metadata' keys
        """
        texts = [chunk['text'] for chunk in cv_chunks]
        metadatas = [chunk['metadata'] for chunk in cv_chunks]

        self.add_documents(texts, metadatas)

    def search_cv_chunks(self, query: str, k: int = 5, section_filter: str = None) -> List[Dict]:
        """
        Search for similar CV chunks, with optional section filtering.

        Args:
            query: The search query
            k: Number of results to return
            section_filter: Optional section to filter by ('skills', 'experience', etc.)

        Returns:
            List of matching chunks with metadata
        """
        results = self.search_similar(query, k)

        if section_filter:
            results = [r for r in results if r['metadata'].get('section') == section_filter]

        return results

    def evaluate_cv_with_rag_context(self, cv_sections: Dict[str, str], job_description: str, job_requirements: str) -> EvaluationResult:
        """
        Enhanced evaluation using RAG to retrieve relevant context from CV chunks.

        Args:
            cv_sections: Dictionary containing CV sections
            job_description: Job description
            job_requirements: Job requirements

        Returns:
            EvaluationResult with scores and feedback
        """
        job_context = f"Job Description: {job_description}\n\nRequirements: {job_requirements}"

        # Retrieve relevant chunks for each evaluation aspect
        skills_chunks = self.search_cv_chunks(job_requirements, k=3, section_filter='skills')
        experience_chunks = self.search_cv_chunks(job_context, k=3, section_filter='experience')
        education_chunks = self.search_cv_chunks(job_requirements, k=3, section_filter='education')

        # Use retrieved chunks for more targeted evaluation
        cv_skills = cv_sections.get('skills', '')
        cv_experience = cv_sections.get('experience', '')
        cv_education = cv_sections.get('education', '')

        # If we find relevant chunks, we can use them as additional context
        retrieved_skills = " ".join([chunk['text'] for chunk in skills_chunks])
        retrieved_experience = " ".join([chunk['text'] for chunk in experience_chunks])
        retrieved_education = " ".join([chunk['text'] for chunk in education_chunks])

        # Enhance original content with retrieved context
        enhanced_skills = cv_skills + " " + retrieved_skills
        enhanced_experience = cv_experience + " " + retrieved_experience
        enhanced_education = cv_education + " " + retrieved_education

        skills_score = self._evaluate_skills_match_llm(enhanced_skills, job_requirements)
        experience_score = self._evaluate_experience_match_llm(enhanced_experience, job_context)
        education_score = self._evaluate_education_match_llm(enhanced_education, job_requirements)

        overall_score = (skills_score * 0.4 + experience_score * 0.4 + education_score * 0.2)

        # Generate detailed feedback using LLM
        strengths, weaknesses, recommendations, feedback = self._generate_detailed_feedback_llm(
            cv_sections, job_description, job_requirements
        )

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

    def _save_vector_store(self):
        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        docs_path = os.path.join(self.vector_db_path, "documents.pkl")

        faiss.write_index(self.index, index_path)
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents, f)

    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        if self.index.ntotal == 0:
            return []

        # Generate embedding for query using Ollama with embeddingGemma
        query_embedding = np.array(self.llm_service.embed_query(query)).reshape(1, -1)
        # Normalize query embedding for cosine similarity
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
        # Generate embeddings for both texts using Ollama with embeddingGemma
        embeddings = self.llm_service.embed_documents([text1, text2])
        embeddings = np.array(embeddings)
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

        similarity = np.dot(embeddings[0], embeddings[1])
        return float(similarity)

    def evaluate_cv_against_job(self, cv_sections: Dict[str, str], job_description: str, job_requirements: str) -> EvaluationResult:
        job_context = f"Job Description: {job_description}\n\nRequirements: {job_requirements}"

        skills_score = self._evaluate_skills_match_llm(cv_sections.get('skills', ''), job_requirements)

        experience_score = self._evaluate_experience_match_llm(cv_sections.get('experience', ''), job_context)

        education_score = self._evaluate_education_match_llm(cv_sections.get('education', ''), job_requirements)

        overall_score = (skills_score * 0.4 + experience_score * 0.4 + education_score * 0.2)

        # Generate detailed feedback using LLM
        strengths, weaknesses, recommendations, feedback = self._generate_detailed_feedback_llm(
            cv_sections, job_description, job_requirements
        )

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

    def _evaluate_skills_match_llm(self, cv_skills: str, job_requirements: str) -> float:
        """
        Evaluate skills match using LLM
        """
        if not cv_skills or not job_requirements:
            return 0.0

        prompt = CV_EVALUATION_PROMPTS["skills_evaluation"].format(
            cv_skills=cv_skills,
            job_requirements=job_requirements
        )

        try:
            response = self.llm_service.generate_text(prompt)
            # Extract numeric score from the response
            score_match = re.search(r'\d+', response)
            if score_match:
                score = float(score_match.group())
                return max(0.0, min(100.0, score))  # Ensure score is between 0-100
            else:
                # Fallback to similarity if LLM didn't return a numeric score
                similarity = self.calculate_similarity_score(cv_skills, job_requirements)
                return min(100.0, max(0.0, similarity * 100))
        except Exception:
            # Fallback to similarity if LLM fails
            similarity = self.calculate_similarity_score(cv_skills, job_requirements)
            return min(100.0, max(0.0, similarity * 100))

    def _evaluate_experience_match_llm(self, cv_experience: str, job_context: str) -> float:
        """
        Evaluate experience match using LLM
        """
        if not cv_experience or not job_context:
            return 0.0

        prompt = CV_EVALUATION_PROMPTS["experience_evaluation"].format(
            cv_experience=cv_experience,
            job_context=job_context
        )

        try:
            response = self.llm_service.generate_text(prompt)
            # Extract numeric score from the response
            score_match = re.search(r'\d+', response)
            if score_match:
                score = float(score_match.group())
                return max(0.0, min(100.0, score))  # Ensure score is between 0-100
            else:
                # Fallback to similarity if LLM didn't return a numeric score
                similarity = self.calculate_similarity_score(cv_experience, job_context)
                return min(100.0, max(0.0, similarity * 100))
        except Exception:
            # Fallback to similarity if LLM fails
            similarity = self.calculate_similarity_score(cv_experience, job_context)
            return min(100.0, max(0.0, similarity * 100))

    def _evaluate_education_match_llm(self, cv_education: str, job_requirements: str) -> float:
        """
        Evaluate education match using LLM
        """
        if not cv_education:
            return 50.0  # Neutral score if no education provided

        if not job_requirements:
            return 70.0  # Default score if no specific education requirements

        prompt = CV_EVALUATION_PROMPTS["education_evaluation"].format(
            cv_education=cv_education,
            job_requirements=job_requirements
        )

        try:
            response = self.llm_service.generate_text(prompt)
            # Extract numeric score from the response
            score_match = re.search(r'\d+', response)
            if score_match:
                score = float(score_match.group())
                return max(30.0, min(100.0, score))  # Ensure score is between 30-100
            else:
                # Fallback to similarity if LLM didn't return a numeric score
                similarity = self.calculate_similarity_score(cv_education, job_requirements)
                return min(100.0, max(30.0, similarity * 100))
        except Exception:
            # Fallback to similarity if LLM fails
            similarity = self.calculate_similarity_score(cv_education, job_requirements)
            return min(100.0, max(30.0, similarity * 100))

    def get_soft_skills_score(self, cv_sections: Dict[str, str], job_context: str) -> float:
        """
        Get soft skills assessment score using LLM
        """
        cv_text = "\n".join([f"{section}: {content}" for section, content in cv_sections.items() if content])

        prompt = CV_EVALUATION_PROMPTS["soft_skills_evaluation"].format(
            cv_text=cv_text,
            job_context=job_context
        )

        try:
            response = self.llm_service.generate_text(prompt)
            # Extract numeric score from the response
            score_match = re.search(r'\d+', response)
            if score_match:
                score = float(score_match.group())
                return max(0.0, min(100.0, score))  # Ensure score is between 0-100
            else:
                return 50.0  # Default score if LLM doesn't return a numeric response
        except Exception:
            return 50.0  # Default score if LLM fails

    def get_contextual_score(self, cv_sections: Dict[str, str], job_description: str, job_requirements: str, context_info: str = "") -> float:
        """
        Get contextual understanding score using LLM
        """
        cv_text = "\n".join([f"{section}: {content}" for section, content in cv_sections.items() if content])

        prompt = CV_EVALUATION_PROMPTS["contextual_understanding"].format(
            cv_text=cv_text,
            job_description=job_description,
            job_requirements=job_requirements,
            context_info=context_info
        )

        try:
            response = self.llm_service.generate_text(prompt)
            # Extract numeric score from the response
            score_match = re.search(r'\d+', response)
            if score_match:
                score = float(score_match.group())
                return max(0.0, min(100.0, score))  # Ensure score is between 0-100
            else:
                return 50.0  # Default score if LLM doesn't return a numeric response
        except Exception:
            return 50.0  # Default score if LLM fails

    def _generate_detailed_feedback_llm(self, cv_sections: Dict[str, str], job_description: str, job_requirements: str):
        """
        Generate detailed feedback using LLM with enhanced soft skills assessment
        """
        cv_text = "\n".join([f"{section}: {content}" for section, content in cv_sections.items() if content])

        prompt = CV_EVALUATION_PROMPTS["detailed_feedback_with_soft_skills"].format(
            cv_text=cv_text,
            job_description=job_description,
            job_requirements=job_requirements
        )

        try:
            response = self.llm_service.generate_text(prompt)

            # Try to parse JSON response
            try:
                # Attempt to extract JSON from response (in case LLM adds extra text)
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)

                    strengths = result.get("strengths", [])
                    weaknesses = result.get("weaknesses", [])
                    recommendations = result.get("recommendations", [])
                    soft_skills_assessment = result.get("soft_skills_assessment", [])
                    summary = result.get("summary", "")

                    # Include soft skills assessment in strengths/weaknesses if not already covered
                    strengths.extend(soft_skills_assessment)

                    return strengths, weaknesses, recommendations, summary
                else:
                    # If no JSON found, return empty feedback
                    return [], [], [], "Unable to generate detailed feedback"
            except json.JSONDecodeError:
                # If JSON parsing fails, return empty feedback
                return [], [], [], "Unable to generate detailed feedback"
        except Exception:
            # Fallback to default feedback
            job_context = f"Job Description: {job_description}\n\nRequirements: {job_requirements}"
            skills_score = self._evaluate_skills_match(cv_sections.get('skills', ''), job_requirements)
            experience_score = self._evaluate_experience_match(cv_sections.get('experience', ''), job_context)
            education_score = self._evaluate_education_match(cv_sections.get('education', ''), job_requirements)
            return self._generate_detailed_feedback(cv_sections, job_context, skills_score, experience_score, education_score), [], [], "Default feedback generated due to LLM error"