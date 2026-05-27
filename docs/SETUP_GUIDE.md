# Setup Guide — Running on Another Device

> Step-by-step instructions to clone, install, and run the AI Resume Analyzer on any machine.

## Prerequisites

| Requirement | Minimum Version | Check Command |
|---|---|---|
| **Python** | 3.9+ | `python --version` |
| **pip** | Latest | `pip --version` |
| **Git** | Any | `git --version` |

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/resume-analyzer.git
cd resume-analyzer
```

---

## Step 2: Create a Virtual Environment

It is **strongly recommended** to use a virtual environment to avoid dependency conflicts.

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt after activation.

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `python-multipart` | File upload support |
| `pdfplumber` | PDF text extraction |
| `python-docx` | DOCX text extraction |
| `spacy` | NLP tokenization and lemmatization |
| `scikit-learn` | TF-IDF vectorization |
| `pandas` | Data manipulation |
| `fpdf2` | PDF report generation |
| `jinja2` | Template rendering |
| `langdetect` | Language detection |

---

## Step 4: Download the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

This downloads the English language model (~12MB) required for NLP processing.

> **Note**: If you skip this step, the app will still run but will fall back to basic tokenization without lemmatization.

---

## Step 5: Run the Server

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

| Flag | Purpose |
|---|---|
| `--reload` | Auto-restart on code changes (development mode) |
| `--host 0.0.0.0` | Accept connections from any network interface |
| `--port 8000` | Run on port 8000 |

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

---

## Step 6: Open in Browser

Navigate to:

```
http://localhost:8000
```

The full application (frontend + backend) is served from this single URL.

---

## Step 7 (Optional): Expose to the Internet via ngrok

If you want to share the app publicly:

### Install ngrok dependency

```bash
pip install pyngrok
```

### Run the tunnel (in a separate terminal)

```bash
python scripts/start_ngrok.py
```

This will output a public URL like:

```
=======================================================
YOUR GLOBAL URL IS: https://abc123.ngrok.io
=======================================================
```

Share this URL with anyone to let them use your analyzer remotely.

> **Note**: You need an ngrok account and auth token for this. Visit [ngrok.com](https://ngrok.com) to sign up.

---

## Step 8 (Optional): Generate PDF Report

```bash
python scripts/generate_report.py
```

This creates `artifacts/Project_Summary_Report.pdf` with project documentation.

---

## Quick Start (TL;DR)

```bash
# Clone
git clone https://github.com/<your-username>/resume-analyzer.git
cd resume-analyzer

# Setup
python -m venv venv
source venv/bin/activate      # Linux/Mac
# .\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run
python -m uvicorn backend.main:app --reload

# Open http://localhost:8000
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'backend'`

**Cause**: Running the server from the wrong directory.

**Fix**: Make sure you're in the project root (where `requirements.txt` is) and use `python -m uvicorn` instead of `uvicorn`:

```bash
cd resume-analyzer
python -m uvicorn backend.main:app --reload
```

---

### `OSError: [E050] Can't find model 'en_core_web_sm'`

**Cause**: spaCy language model not downloaded.

**Fix**:

```bash
python -m spacy download en_core_web_sm
```

---

### `Address already in use` (Port 8000)

**Cause**: Another process is using port 8000.

**Fix**: Use a different port:

```bash
python -m uvicorn backend.main:app --reload --port 8001
```

Then open `http://localhost:8001`.

---

### `langdetect.lang_detect_exception.LangDetectException`

**Cause**: Resume text is too short or empty for language detection.

**Fix**: This is handled gracefully by the backend (returns `"Unknown"`). No action needed.

---

### API calls fail with CORS errors

**Cause**: Frontend is being served from a different origin (e.g., opening `index.html` directly in the browser via `file://`).

**Fix**: Always access the app through `http://localhost:8000`, not by opening the HTML file directly. FastAPI serves both the API and frontend from the same origin.

---

## Project Structure

```
resume-analyzer/
├── backend/                  # FastAPI server + NLP engine
│   ├── __init__.py
│   ├── main.py               # App entry point, API routes
│   ├── model.py               # AdvancedAnalyzer class
│   ├── utils.py               # Text extraction, preprocessing
│   ├── role_data.py           # Legacy role database
│   └── roles.json             # Extended role database (16+ roles)
│
├── frontend/                 # Static UI
│   ├── index.html             # Page structure
│   ├── style.css              # Midnight Pro theme
│   └── script.js              # Application logic
│
├── scripts/                  # Utility scripts
│   ├── generate_report.py     # PDF report generator
│   └── start_ngrok.py         # ngrok tunnel launcher
│
├── docs/                     # Documentation
├── requirements.txt          # Python dependencies
├── .gitignore
├── LICENSE                   # MIT
├── CONTRIBUTING.md
└── README.md
```
