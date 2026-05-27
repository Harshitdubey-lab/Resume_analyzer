# AI Resume Analyzer — Application Overview

> A comprehensive, non-technical overview of the application, its features, and how it works.

## What Is This?

The **AI Resume Analyzer** is a full-stack web application that evaluates resumes using Natural Language Processing (NLP) and Machine Learning techniques. It provides:

- A **composite ATS score** (0–100) based on multiple criteria
- **Semantic matching** against job descriptions
- **Keyword gap analysis** to identify missing skills
- **Formatting feedback** to improve structure
- An **AI chatbot coach** to answer questions about your resume

---

## Key Features

### 🎯 ATS Compatibility Scoring
Get a comprehensive score from 0–100 based on skills, experience, projects, education, and keyword optimization. The score uses TF-IDF cosine similarity against industry benchmarks.

### 🔍 Semantic Job Description Matching
Paste any job description and the analyzer will compute how closely your resume matches using vector-based semantic similarity — not just keyword matching.

### 📊 Role-Specific Analysis
Choose from **16+ built-in job roles** including Software Engineer, Data Scientist, ML Engineer, DevOps Engineer, Product Manager, and more. Each role has curated skill benchmarks.

### 🏷️ Keyword Gap Detection
See exactly which critical skills and technologies are **missing** from your resume for your target role, displayed as visual tags.

### 📈 Score Distribution Radar Chart
A Chart.js radar visualization shows how your resume performs across 5 dimensions: Skills, Experience, Projects, Education, and Keywords.

### ✍️ AI-Powered Bullet Rewriting
The analyzer detects weak action verbs like "Responsible for" or "Helped with" and suggests power-verb replacements like "Spearheaded" or "Engineered".

### 📋 Formatting Audit
Automatic checks for resume length (too short/long), bullet point usage, and structural consistency.

### 🌐 Language Detection
Automatically detects whether the resume is in English, Hindi, or another language.

### 💬 AI Career Coach Chatbot
After analysis, chat with an AI coach that can explain your score, suggest skills to add, identify formatting issues, and provide improvement recommendations.

### 📜 Analysis History
Your last 5 analyses are saved in the browser (localStorage) so you can track improvement over time.

### 🎨 Midnight Pro UI
A premium dark-themed glassmorphic interface with animated backgrounds, smooth transitions, and modern typography.

---

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  1. UPLOAD  │ ──→ │  2. ANALYZE  │ ──→ │   3. IMPROVE    │
│             │     │              │     │                 │
│ PDF or DOCX │     │ NLP Engine   │     │ Score Dashboard │
│ Select Role │     │ TF-IDF Match │     │ Missing Skills  │
│ Paste JD    │     │ Section Scan │     │ AI Chat Coach   │
└─────────────┘     └──────────────┘     └─────────────────┘
```

1. **Upload** your resume (PDF or DOCX) and select your target job role
2. **Analyze** — the NLP engine extracts text, identifies sections, computes semantic similarity, and generates a comprehensive score
3. **Improve** — review your scores, fill keyword gaps, fix formatting issues, and chat with the AI coach for personalized advice

---

## Scoring Breakdown

| Component | Weight | What It Measures |
|---|---|---|
| **Skills Section** | 30 points | Presence and completeness of a skills section |
| **Experience Section** | 25 points | Depth of work experience content (>100 words = full score) |
| **Projects Section** | 20 points | Presence of project descriptions |
| **Education Section** | 15 points | Presence of educational background |
| **ATS Keyword Match** | 10 points | Cosine similarity with role/JD target text |
| **Total** | **100** | Capped at 100 |

---

## Supported Job Roles

| # | Role | Key Skills Evaluated |
|---|---|---|
| 1 | Software Engineer | Python, Java, C++, System Design, DSA |
| 2 | Data Scientist | Python, R, ML, Deep Learning, Statistics |
| 3 | Data Analyst | SQL, Excel, Tableau, Python, Statistics |
| 4 | Machine Learning Engineer | TensorFlow, PyTorch, MLOps, Feature Engineering |
| 5 | AI Engineer | NLP, Computer Vision, Transformers, LLMs |
| 6 | Backend Developer | Node.js, Django, FastAPI, Databases, REST |
| 7 | Frontend Developer | React, Vue, Angular, CSS, JavaScript |
| 8 | Full Stack Developer | Both frontend + backend technologies |
| 9 | DevOps Engineer | Docker, Kubernetes, CI/CD, AWS, Terraform |
| 10 | Cloud Engineer | AWS, Azure, GCP, Infrastructure as Code |
| 11 | Cybersecurity Analyst | Pentesting, SIEM, Encryption, Compliance |
| 12 | Mobile App Developer | React Native, Flutter, Swift, Kotlin |
| 13 | UI/UX Designer | Figma, Wireframing, User Research, Prototyping |
| 14 | Product Manager | Roadmapping, Agile, Stakeholder Management |
| 15 | Business Analyst | Requirements, Data Modeling, Process Mapping |
| 16 | QA Engineer | Selenium, Jest, Test Planning, Automation |
| 17 | Other (Custom) | User-defined — analyzed via spaCy NER + JD keywords |

---

## Limitations

- **No real LLM integration** — The chatbot uses rule-based intent matching, not GPT/Gemini. It can be upgraded to use an LLM API.
- **English-focused** — While language detection exists, the NLP analysis and keyword matching are optimized for English resumes.
- **Heuristic section parsing** — Section extraction uses keyword matching on headers, which may miss non-standard resume formats.
- **No persistent storage** — Analysis results are not saved server-side. Only the browser's localStorage keeps a history of scores.
- **Single-user** — No authentication or multi-user support.

---

## Tech Stack Summary

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JS, Chart.js |
| **Backend** | Python, FastAPI, Uvicorn |
| **NLP** | spaCy, scikit-learn (TF-IDF + Cosine Similarity) |
| **File Processing** | pdfplumber (PDF), python-docx (DOCX) |
| **Language Detection** | langdetect |
| **Fonts** | Google Fonts — Outfit |
