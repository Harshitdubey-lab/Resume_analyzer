# Backend Architecture

> Detailed documentation of the AI Resume Analyzer's backend — FastAPI server, NLP engine, and scoring system.

## Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | High-performance async web framework |
| **spaCy** (`en_core_web_sm`) | NLP tokenization, lemmatization, noun-chunk extraction |
| **scikit-learn** | TF-IDF vectorization and cosine similarity |
| **pdfplumber** | PDF text extraction |
| **python-docx** | DOCX text extraction |
| **langdetect** | Resume language detection (English/Hindi/Other) |
| **Pydantic** | Request/response validation (via FastAPI) |

---

## Module Map

```
backend/
├── __init__.py       → Package initializer
├── main.py           → FastAPI app, route definitions, CORS, static mount
├── model.py          → AdvancedAnalyzer class — core NLP and scoring engine
├── utils.py          → Text extraction, cleaning, preprocessing, section parsing
├── role_data.py      → Legacy job role database (Python dict) + impact verbs
└── roles.json        → Extended job role database (16+ roles, loaded at startup)
```

---

## Module Details

### `main.py` — Application Entry Point

- Creates the FastAPI app instance with title `"Production-Grade Resume AI"`
- Configures CORS middleware (allows all origins for development)
- Instantiates the `AdvancedAnalyzer` singleton
- Defines API routes (`/upload-resume`, `/analyze`, `/chat`)
- Mounts the `frontend/` directory as static files at root `/`
- Static file mount is placed **last** to avoid overriding API routes

### `model.py` — AdvancedAnalyzer Engine

The core intelligence module containing the `AdvancedAnalyzer` class.

**Constructor**: Initializes a TF-IDF vectorizer with unigram + bigram support (`ngram_range=(1, 2)`).

#### Methods

| Method | Signature | Purpose |
|---|---|---|
| `get_keyword_density` | `(text) → dict` | Top-15 word frequencies as percentage |
| `check_formatting` | `(text) → dict` | Checks word count (300–1000) and bullet usage |
| `rewrite_bullets` | `(text) → list` | Detects weak verbs, suggests power-verb replacements |
| `analyze_advanced` | `(text, job_role, custom_role, jd) → dict` | **Main analysis pipeline** |
| `generate_chat_response` | `(message, context) → str` | Rule-based chatbot with intent matching |

#### `analyze_advanced()` — The Core Pipeline

```
1. Extract sections (skills, experience, projects, education)
2. Resolve job role (built-in OR custom via spaCy NER)
3. Build target text (from JD or role keywords)
4. TF-IDF vectorize [resume_text, target_text]
5. Compute cosine similarity → match_percentage
6. Score each section (skills:30, experience:25, projects:20, education:15)
7. Detect missing keywords + overused keywords (density > 4%)
8. Generate feedback (strengths, weaknesses, suggestions)
9. Check formatting + detect language
10. total_score = section_scores + (match_score × 0.1), capped at 100
```

#### Chat Intent Matching

| Intent Keywords | Response Type |
|---|---|
| `skill`, `missing`, `keyword`, `learn`, `add` | Lists missing skills |
| `format`, `structure`, `length`, `look`, `design` | Formatting issues |
| `score`, `ats`, `percentage`, `match`, `low` | Score explanation |
| `improve`, `suggestion`, `recommend`, `weakness` | Weaknesses + fixes |
| *(fallback)* | Generic capabilities prompt |

### `utils.py` — Text Processing Utilities

| Function | Purpose |
|---|---|
| `detect_language(text)` | Identifies English/Hindi/Other via `langdetect` |
| `extract_text_from_pdf(path)` | Extracts text page-by-page with `pdfplumber` |
| `extract_text_from_docx(path)` | Joins paragraph texts from DOCX |
| `clean_text(text)` | Collapses whitespace, strips edges |
| `preprocess_text(text)` | spaCy tokenization, stopword removal, lemmatization |
| `extract_sections(text)` | Heuristic header-based section parser |

#### Section Extraction Headers

| Section | Recognized Keywords |
|---|---|
| Education | `education`, `academic`, `university`, `college`, `school`, `degree` |
| Experience | `experience`, `work`, `employment`, `history`, `professional` |
| Projects | `projects`, `personal projects`, `academic projects` |
| Skills | `skills`, `technical skills`, `technologies`, `competencies` |

### `roles.json` — 16+ Job Role Database

Loaded at startup. Each role contains `core_skills`, `tools`, and `description_keywords` arrays. Supports: Software Engineer, Data Scientist, Data Analyst, ML Engineer, AI Engineer, Backend/Frontend/Full Stack Developer, DevOps Engineer, Cloud Engineer, Cybersecurity Analyst, Mobile Developer, UI/UX Designer, Product Manager, Business Analyst, QA Engineer.

### `role_data.py` — Legacy (Not Actively Used)

Contains the original 3-role Python dict and `IMPACT_VERBS` list. Retained for reference; the system uses `roles.json` instead.

---

## Scoring Algorithm

| Component | Max Points | Logic |
|---|---|---|
| Skills section | 30 | 30 if exists, else 0 |
| Experience section | 25 | 25 if >100 words, 15 if exists but short, else 0 |
| Projects section | 20 | 20 if exists, else 0 |
| Education section | 15 | 15 if exists, else 5 (baseline) |
| ATS Match Bonus | ~10 | `cosine_similarity × 0.1` |
| **Total** | **100** | `min(100, section_scores + ats_bonus)` |

---

## Error Handling

| Scenario | Handling |
|---|---|
| spaCy model not installed | Falls back to basic tokenization |
| Invalid file format | HTTP 400 error |
| Missing JD | Uses role keywords as target text |
| Unknown job role | Falls back to `software_engineer` |
