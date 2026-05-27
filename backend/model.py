import re
import json
import os
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import preprocess_text, extract_sections, detect_language

# Load roles from JSON
ROLES_FILE = os.path.join(os.path.dirname(__file__), 'roles.json')
with open(ROLES_FILE, 'r') as f:
    JOB_ROLES = json.load(f)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

class AdvancedAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    def get_keyword_density(self, text):
        words = re.findall(r'\w+', text.lower())
        total_words = len(words)
        freq = Counter(words)
        density = {word: round((count / total_words) * 100, 2) for word, count in freq.most_common(15)}
        return density

    def check_formatting(self, text):
        issues = []
        word_count = len(text.split())
        if word_count < 300:
            issues.append("Resume might be too short for professional roles.")
        elif word_count > 1000:
            issues.append("Resume is quite long; consider condensing it to 1-2 pages.")
        
        if text.count('•') < 5 and text.count('-') < 5:
            issues.append("Lack of bullet points detected; use them for better readability.")
            
        return {
            "score": 100 - (len(issues) * 15),
            "issues": issues
        }

    def rewrite_bullets(self, text):
        weak_patterns = [
            (r"(?i)responsible for", "Spearheaded and executed"),
            (r"(?i)helped with", "Collaborated on and optimized"),
            (r"(?i)worked on", "Engineered and delivered"),
            (r"(?i)handled", "Orchestrated"),
        ]
        
        suggestions = []
        for pattern, replacement in weak_patterns:
            if re.search(pattern, text):
                suggestions.append(f"Replace '{pattern}' with '{replacement}' to show leadership.")
        
        return suggestions

    def analyze_advanced(self, text, job_role="software_engineer", custom_role=None, jd=None):
        sections = extract_sections(text)
        
        # Dynamic Role Resolution
        if job_role == "other" and custom_role:
            role_info = {
                "core_skills": [],
                "tools": [],
                "description_keywords": []
            }
            if nlp:
                doc = nlp(custom_role.lower())
                # Extract nouns and entities from the custom role name
                keywords = [chunk.text for chunk in doc.noun_chunks]
                if not keywords:
                    keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
                role_info["core_skills"] = list(set(keywords))
            else:
                role_info["core_skills"] = custom_role.lower().split()
                
            # If JD is provided, it acts as the primary source of truth for 'other' roles
            if jd:
                jd_words = re.findall(r'\b[a-zA-Z]{3,}\b', jd.lower())
                freq = Counter(jd_words)
                top_jd_keywords = [word for word, count in freq.most_common(10) if word not in ["and", "the", "with", "for"]]
                role_info["core_skills"].extend(top_jd_keywords)
                
            job_role = custom_role.lower().replace(" ", "_")
        else:
            role_info = JOB_ROLES.get(job_role, JOB_ROLES["software_engineer"])
        
        target_text = jd if jd else " ".join(role_info["core_skills"] + role_info["description_keywords"])
        tfidf_matrix = self.vectorizer.fit_transform([text, target_text])
        match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

        section_scores = {
            "skills": 30 if sections["skills"] else 0,
            "experience": 25 if len(sections["experience"].split()) > 100 else (15 if sections["experience"] else 0),
            "projects": 20 if sections["projects"] else 0,
            "education": 15 if sections["education"] else 5
        }

        extracted_words = set(re.findall(r'\w+', text.lower()))
        missing_keywords = [kw for kw in role_info["core_skills"] if kw not in extracted_words]
        overused = [word for word, density in self.get_keyword_density(text).items() if density > 4]

        feedback = {
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }

        if match_score > 75:
            feedback["strengths"].append("Excellent alignment with the target role's core requirements.")
        elif match_score < 40:
            feedback["weaknesses"].append("Low semantic match with industry standards for this role.")

        feedback["suggestions"].extend(self.rewrite_bullets(text))
        
        formatting = self.check_formatting(text)
        lang = detect_language(text)
        
        total_score = sum(section_scores.values()) + (match_score * 0.1)
        total_score = min(100, total_score)

        return {
            "overall_score": round(total_score, 2),
            "language": lang,
            "match_percentage": round(match_score, 2),
            "section_scores": section_scores,
            "keyword_density": self.get_keyword_density(text),
            "missing_keywords": missing_keywords,
            "overused_keywords": overused,
            "formatting_report": formatting,
            "feedback": feedback,
            "role_context": job_role
        }

    def generate_chat_response(self, message: str, context: dict) -> str:
        """
        Simulates an LLM response using rule-based NLP on the analysis context.
        In production, replace this with an OpenAI or Gemini API call.
        """
        msg_lower = message.lower()
        
        # 1. Answer about skills / missing keywords
        if any(word in msg_lower for word in ["skill", "missing", "keyword", "learn", "add"]):
            missing = context.get("missing_keywords", [])
            if missing:
                return f"Based on the analysis for **{context.get('role_context', 'your role').replace('_', ' ')}**, you should focus on adding these critical skills: <br>• " + "<br>• ".join(missing[:5]) + "<br><br>Adding these will significantly boost your ATS match."
            return "Your skills section looks perfectly aligned with the role! You aren't missing any critical keywords."
            
        # 2. Answer about formatting / structure
        if any(word in msg_lower for word in ["format", "structure", "length", "look", "design"]):
            issues = context.get("formatting_report", {}).get("issues", [])
            if issues:
                return "I noticed a few formatting areas to improve:<br><br>" + "<br>".join([f"• {issue}" for issue in issues])
            return "Your formatting looks highly professional. The length is optimal and bullet points are well-structured."
            
        # 3. Answer about score / ATS
        if any(word in msg_lower for word in ["score", "ats", "percentage", "match", "low"]):
            score = context.get("overall_score", 0)
            if score < 50:
                return f"Your score is **{score}/100**. It's quite low because you might be missing critical sections or keywords for this specific role. I recommend reviewing my 'AI Recommendations' to rewrite your bullet points and adding the missing skills."
            elif score < 80:
                return f"Your score is **{score}/100**. This is decent, but you can push it over 80 by quantifying your achievements (e.g., 'increased sales by 20%') and matching the exact keywords from the Job Description."
            return f"Excellent! Your score is **{score}/100**. Your resume is highly competitive for this role."

        # 4. Answer about improvements / suggestions
        if any(word in msg_lower for word in ["improve", "suggestion", "recommend", "weakness"]):
            weaknesses = context.get("feedback", {}).get("weaknesses", [])
            suggestions = context.get("feedback", {}).get("suggestions", [])
            reply = ""
            if weaknesses:
                reply += "Here are your main weaknesses:<br>• " + "<br>• ".join(weaknesses) + "<br><br>"
            if suggestions:
                reply += "Here is how you can fix them:<br>• " + "<br>• ".join(suggestions)
            return reply if reply else "Your resume is very strong. I don't have any major suggestions right now!"

        # Fallback response
        return "I am your AI Career Coach. I can help you understand your **score**, suggest **skills** to add, or help fix your **formatting**. What would you like to focus on?"
