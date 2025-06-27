import os
import re
from typing import Dict, Optional
from PyPDF2 import PdfReader
from docx import Document
import aiofiles

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    async def extract_text_from_file(self, file_path: str) -> str:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return await self._extract_from_pdf(file_path)
        elif file_extension == '.docx':
            return await self._extract_from_docx(file_path)
        elif file_extension == '.txt':
            return await self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    async def _extract_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return self._clean_text(text)
    
    async def _extract_from_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
        
        return self._clean_text(text)
    
    async def _extract_from_txt(self, file_path: str) -> str:
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                text = await file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
        
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def extract_cv_sections(self, text: str) -> Dict[str, str]:
        sections = {
            'contact_info': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'certifications': '',
            'full_text': text
        }
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        current_section = 'contact_info'
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in ['experience', 'work history', 'employment']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'experience'
                section_content = []
                continue
            elif any(keyword in line_lower for keyword in ['education', 'academic', 'qualification']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'education'
                section_content = []
                continue
            elif any(keyword in line_lower for keyword in ['skills', 'technical skills', 'competencies']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'skills'
                section_content = []
                continue
            elif any(keyword in line_lower for keyword in ['summary', 'profile', 'objective']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'summary'
                section_content = []
                continue
            elif any(keyword in line_lower for keyword in ['certification', 'certificate', 'license']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'certifications'
                section_content = []
                continue
            
            section_content.append(line)
        
        if section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def extract_candidate_info(self, text: str) -> Dict[str, Optional[str]]:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        email_match = re.search(email_pattern, text)
        phone_match = re.search(phone_pattern, text)
        
        lines = text.split('\n')
        name = None
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 4 and not re.search(r'[^\w\s-.]', line):
                if not re.search(email_pattern, line) and not re.search(phone_pattern, line):
                    name = line
                    break
        
        return {
            'name': name,
            'email': email_match.group() if email_match else None,
            'phone': phone_match.group() if phone_match else None
        }