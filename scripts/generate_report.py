from fpdf import FPDF
import os

class ProjectReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Resume Analyzer Project Documentation', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_report():
    pdf = ProjectReport()
    pdf.add_page()

    # Introduction
    pdf.chapter_title("1. Project Overview")
    pdf.chapter_body(
        "The Resume Analyzer is a full-stack web application designed to evaluate resumes using Natural Language Processing (NLP) "
        "and Machine Learning techniques. It provides a comprehensive score (0-100) based on multiple parameters and offers "
        "actionable feedback for improvement."
    )

    # Technical Stack
    pdf.chapter_title("2. Technical Stack")
    pdf.chapter_body(
        "- Backend: FastAPI (Python)\n"
        "- NLP Engine: spaCy / TF-IDF (Scikit-learn)\n"
        "- Frontend: HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla)\n"
        "- Visualization: Chart.js\n"
        "- File Extraction: pdfplumber, python-docx"
    )

    # Core Features
    pdf.chapter_title("3. Core Features")
    pdf.chapter_body(
        "- Dual Format Support: Processes both PDF and DOCX files.\n"
        "- ATS Scoring: Evaluates compatibility with job descriptions using TF-IDF cosine similarity.\n"
        "- Section Analysis: Heuristic-based extraction of Skills, Experience, Projects, and Education.\n"
        "- Dynamic Feedback: Generates strengths, weaknesses, and suggestions in real-time.\n"
        "- Modern UI: Responsive, glassmorphic design with animated charts."
    )

    # Scoring Logic
    pdf.chapter_title("4. Scoring Distribution")
    pdf.chapter_body(
        "- Skills Match: 30%\n"
        "- Experience Quality: 25%\n"
        "- Project Portfolio: 20%\n"
        "- Educational Background: 15%\n"
        "- Keywords & ATS Optimization: 10%"
    )

    # ML Model Explanation
    pdf.chapter_title("5. Machine Learning & NLP Logic")
    pdf.chapter_body(
        "The system uses a TF-IDF (Term Frequency-Inverse Document Frequency) Vectorizer to transform text into numerical vectors. "
        "Cosine Similarity is then applied to calculate the distance between the resume vector and the job description (or ideal profile) vector. "
        "Additionally, spaCy is used for text normalization and stopword removal to ensure the analyzer focuses on meaningful technical keywords."
    )

    # Output path — adjusted for running from project root
    output_path = os.path.join(os.getcwd(), "artifacts", "Project_Summary_Report.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"Report generated at: {output_path}")

if __name__ == "__main__":
    generate_report()
