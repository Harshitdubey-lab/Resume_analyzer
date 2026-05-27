# API Reference

> Complete documentation of every API endpoint in the AI Resume Analyzer.

## Base URL

```
http://localhost:8000
```

---

## Endpoints Overview

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/upload-resume` | Upload and extract text from a resume |
| `POST` | `/analyze` | Full resume analysis with scoring |
| `POST` | `/chat` | AI career coach chatbot |
| `GET` | `/` | Serve frontend UI (static files) |

---

## `POST /upload-resume`

Upload a resume file and get the extracted text back.

### Request

- **Content-Type**: `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | File (PDF/DOCX) | ✅ | The resume file to extract text from |

### Response — `200 OK`

```json
{
  "filename": "john_doe_resume.pdf",
  "extracted_text": "John Doe\nSoftware Engineer\n10+ years of experience in..."
}
```

> **Note**: `extracted_text` is truncated to the first 1000 characters with `...` appended.

### Error — `400 Bad Request`

```json
{
  "detail": "Invalid file format. Only PDF and DOCX are supported."
}
```

### Used By

This endpoint is currently **not called** by the frontend. It exists as a standalone utility for text extraction without analysis.

---

## `POST /analyze`

The main analysis endpoint. Processes a resume against a job role and optional job description.

### Request

- **Content-Type**: `multipart/form-data`

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | File (PDF/DOCX) | ✅ | — | Resume file |
| `job_role` | string | ❌ | `"software_engineer"` | Target role key (see roles list below) |
| `custom_role` | string | ❌ | `None` | Custom role name (only used when `job_role="other"`) |
| `job_description` | string | ❌ | `None` | Full job description text for semantic matching |

#### Valid `job_role` Values

```
software_engineer, data_scientist, data_analyst, machine_learning_engineer,
ai_engineer, backend_developer, frontend_developer, full_stack_developer,
devops_engineer, cloud_engineer, cybersecurity_analyst, mobile_app_developer,
ui_ux_designer, product_manager, business_analyst, qa_engineer, other
```

### Response — `200 OK`

```json
{
  "overall_score": 72.45,
  "language": "English",
  "match_percentage": 34.52,
  "section_scores": {
    "skills": 30,
    "experience": 25,
    "projects": 0,
    "education": 15
  },
  "keyword_density": {
    "python": 3.21,
    "data": 2.89,
    "experience": 1.45
  },
  "missing_keywords": ["docker", "kubernetes", "system design"],
  "overused_keywords": ["the", "and"],
  "formatting_report": {
    "score": 85,
    "issues": ["Lack of bullet points detected; use them for better readability."]
  },
  "feedback": {
    "strengths": ["Excellent alignment with the target role's core requirements."],
    "weaknesses": [],
    "suggestions": ["Replace 'responsible for' with 'Spearheaded and executed' to show leadership."]
  },
  "role_context": "software_engineer"
}
```

### Response Field Descriptions

| Field | Type | Description |
|---|---|---|
| `overall_score` | float | Composite score 0–100 |
| `language` | string | Detected language: `"English"`, `"Hindi"`, or `"Other"` |
| `match_percentage` | float | TF-IDF cosine similarity with target (0–100) |
| `section_scores` | object | Individual scores for skills, experience, projects, education |
| `keyword_density` | object | Top-15 words with their frequency percentage |
| `missing_keywords` | array | Role-critical skills not found in resume |
| `overused_keywords` | array | Words appearing with >4% density |
| `formatting_report` | object | Score (0–100) and list of formatting issues |
| `feedback` | object | Arrays of strengths, weaknesses, and suggestions |
| `role_context` | string | The resolved job role key used for analysis |

### Used By

**Frontend** — `script.js`, line 81:
```javascript
const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    body: formData
});
```
Called when the user clicks the **"Analyze Resume"** button. Response is passed to `displayResults(data)`.

---

## `POST /chat`

Send a message to the AI career coach chatbot along with analysis context.

### Request

- **Content-Type**: `application/json`

```json
{
  "message": "What skills am I missing?",
  "context": {
    "overall_score": 72.45,
    "missing_keywords": ["docker", "kubernetes"],
    "formatting_report": { "score": 85, "issues": [] },
    "feedback": { "strengths": [], "weaknesses": [], "suggestions": [] },
    "role_context": "software_engineer"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | ✅ | The user's question |
| `context` | object | ✅ | The full analysis response object from `/analyze` |

### Response — `200 OK`

```json
{
  "reply": "Based on the analysis for **software engineer**, you should focus on adding these critical skills: <br>• docker<br>• kubernetes<br><br>Adding these will significantly boost your ATS match."
}
```

> **Note**: The `reply` field contains HTML formatting (`<br>`, `<b>`, `**`) for direct rendering in the chat UI.

### Used By

**Frontend** — `script.js`, line 183:
```javascript
const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text, context: currentAnalysisContext })
});
```
Called when the user sends a message in the **chat widget**.

---

## `GET /` — Static File Server

Serves the frontend application from the `frontend/` directory.

| Path | Serves |
|---|---|
| `/` | `frontend/index.html` |
| `/style.css` | `frontend/style.css` |
| `/script.js` | `frontend/script.js` |

**Implementation**: FastAPI `StaticFiles` mount with `html=True` for SPA-like behavior.

```python
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
```

---

## CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

All origins, methods, and headers are allowed. This is suitable for development but should be restricted in production.
