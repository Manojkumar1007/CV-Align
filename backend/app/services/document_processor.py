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
        # Preserve some line breaks for better section parsing
        # Convert multiple spaces to single space but keep line breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
        text = re.sub(r'\n\s*\n', '\n', text)  # Multiple newlines to single newline
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
        
        # Try to split by common section headers first
        section_patterns = {
            'experience': r'\b(experience|work\s+history|employment|professional\s+experience)\b',
            'education': r'\b(education|academic|qualification|academic\s+background)\b',
            'skills': r'\b(skills|technical\s+skills|competencies|core\s+competencies)\b',
            'summary': r'\b(summary|profile|objective|professional\s+summary)\b',
            'certifications': r'\b(certification|certificate|license|certifications)\b'
        }
        
        # If text has proper line breaks, use line-by-line processing
        lines = text.split('\n')
        if len(lines) > 5:  # Proper multi-line text
            current_section = 'contact_info'
            section_content = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                line_lower = line.lower()
                
                # Check if this line is a section header
                section_found = None
                for section_name, pattern in section_patterns.items():
                    if re.search(pattern, line_lower):
                        section_found = section_name
                        break
                
                if section_found:
                    if section_content:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = section_found
                    section_content = []
                    continue
                
                section_content.append(line)
            
            if section_content:
                sections[current_section] = '\n'.join(section_content)
        
        else:  # Single line or few lines - use regex to extract sections
            # Extract contact info (first part before any section keywords)
            contact_match = re.search(r'^(.*?)(?=' + '|'.join(section_patterns.values()) + ')', text, re.IGNORECASE)
            if contact_match:
                sections['contact_info'] = contact_match.group(1).strip()
            
            # Extract each section using regex
            for section_name, pattern in section_patterns.items():
                # Find section start
                start_match = re.search(pattern, text, re.IGNORECASE)
                if start_match:
                    start_pos = start_match.end()
                    
                    # Find next section or end of text
                    next_patterns = [p for p in section_patterns.values() if p != pattern]
                    end_pos = len(text)
                    
                    for next_pattern in next_patterns:
                        next_match = re.search(next_pattern, text[start_pos:], re.IGNORECASE)
                        if next_match:
                            end_pos = min(end_pos, start_pos + next_match.start())
                    
                    section_text = text[start_pos:end_pos].strip()
                    if section_text:
                        sections[section_name] = section_text
        
        return sections
    
    def extract_candidate_info(self, text: str) -> Dict[str, Optional[str]]:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        email_match = re.search(email_pattern, text)
        phone_match = re.search(phone_pattern, text)
        
        # Try to extract name from the beginning of the text
        name = None
        
        # Always start with the text_start method for more reliable extraction
        text_start = text[:300]  # First 300 characters
        
        # Method 1: Try to find name before phone number
        phone_match_start = re.search(phone_pattern, text_start)
        if phone_match_start:
            potential_name = text_start[:phone_match_start.start()].strip()
            # Remove common prefixes and clean up
            potential_name = re.sub(r'^(resume|cv|curriculum\s+vitae)\s*', '', potential_name, flags=re.IGNORECASE)
            potential_name = re.sub(r'[^\w\s\-\.]', '', potential_name).strip()
            
            # Check if it looks like a valid name (2-4 words, not too long)
            words = potential_name.split()
            if len(words) >= 2 and len(words) <= 4 and len(potential_name) <= 50:
                # Additional validation - not common CV sections
                if not any(section in potential_name.lower() for section in ['education', 'experience', 'skills', 'contact', 'objective', 'summary']):
                    name = potential_name
        
        # Method 2: Try to find name before email if phone method didn't work
        if not name:
            email_match_start = re.search(email_pattern, text_start)
            if email_match_start:
                potential_name = text_start[:email_match_start.start()].strip()
                # Remove common prefixes and clean up
                potential_name = re.sub(r'^(resume|cv|curriculum\s+vitae)\s*', '', potential_name, flags=re.IGNORECASE)
                potential_name = re.sub(r'[^\w\s\-\.]', '', potential_name).strip()
                
                # Check if it looks like a valid name
                words = potential_name.split()
                if len(words) >= 2 and len(words) <= 4 and len(potential_name) <= 50:
                    # Additional validation - not common CV sections
                    if not any(section in potential_name.lower() for section in ['education', 'experience', 'skills', 'contact', 'objective', 'summary']):
                        name = potential_name
        
        # Method 3: Fallback to line-by-line if text has proper line breaks
        if not name:
            lines = text.split('\n')
            if len(lines) > 1:
                for line in lines[:3]:  # Check only first 3 lines
                    line = line.strip()
                    if line:
                        # Remove common prefixes
                        clean_line = re.sub(r'^(resume|cv|curriculum\s+vitae)\s*', '', line, flags=re.IGNORECASE)
                        clean_line = re.sub(r'[^\w\s\-\.]', '', clean_line).strip()
                        
                        words = clean_line.split()
                        # Valid name criteria: 2-4 words, no emails, no phones, reasonable length
                        if (len(words) >= 2 and len(words) <= 4 and len(clean_line) <= 50 and
                            not re.search(email_pattern, clean_line) and 
                            not re.search(phone_pattern, clean_line) and
                            not any(section in clean_line.lower() for section in ['education', 'experience', 'skills', 'contact', 'objective', 'summary', 'roll', 'number'])):
                            name = clean_line
                            break
        
        return {
            'name': name,
            'email': email_match.group() if email_match else None,
            'phone': phone_match.group() if phone_match else None
        }