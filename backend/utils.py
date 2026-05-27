import pdfplumber
import docx
import re
import spacy
from typing import List
from langdetect import detect

def detect_language(text: str) -> str:
    """Detects if the resume is in English or Hindi."""
    try:
        lang = detect(text)
        return "English" if lang == 'en' else ("Hindi" if lang == 'hi' else "Other")
    except:
        return "Unknown"

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not found, we'll need to download it in the setup step
    nlp = None

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def clean_text(text: str) -> str:
    """Cleans and preprocesses the extracted text."""
    # Remove special characters and numbers (optional, keeping for context usually)
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    text = text.strip()
    return text

def preprocess_text(text: str) -> List[str]:
    """Tokenizes and removes stopwords."""
    if nlp is None:
        # Fallback if spacy isn't loaded
        return text.lower().split()
    
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return tokens

def extract_sections(text: str):
    """Simple heuristic to extract sections from resume text."""
    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": ""
    }
    
    keywords = {
        "education": ["education", "academic", "university", "college", "school", "degree"],
        "experience": ["experience", "work", "employment", "history", "professional"],
        "projects": ["projects", "personal projects", "academic projects"],
        "skills": ["skills", "technical skills", "technologies", "competencies"]
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        clean_line = line.strip().lower()
        found_header = False
        for section, keys in keywords.items():
            if any(key == clean_line for key in keys):
                current_section = section
                found_header = True
                break
        
        if not found_header and current_section:
            sections[current_section] += line + " "
            
    return sections
