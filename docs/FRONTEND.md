# Frontend Architecture

> Detailed documentation of the AI Resume Analyzer's frontend layer.

## Tech Stack

| Technology | Purpose |
|---|---|
| **HTML5** | Semantic page structure |
| **CSS3** | Glassmorphic design system with custom properties |
| **Vanilla JavaScript** | Application logic, DOM manipulation, API calls |
| **Chart.js** | Radar chart for score distribution visualization |
| **Google Fonts (Outfit)** | Modern typography (weights: 300, 400, 600, 800) |

---

## File Map

```
frontend/
├── index.html    → Page structure, semantic markup, all UI components
├── style.css     → Complete design system, animations, responsive layout
└── script.js     → Application logic, API integration, chart rendering
```

---

## Design System

### CSS Custom Properties

The UI is built on a centralized variable system defined at the `:root` level in `style.css`:

| Variable | Purpose |
|---|---|
| `--bg-primary` | Main background color (deep dark) |
| `--bg-card` | Card/container background with transparency |
| `--glass-border` | Border color for glassmorphic elements |
| `--text-primary` | Primary text color |
| `--text-muted` | Secondary/subtle text color |
| `--accent` | Primary accent (violet `#8b5cf6`) |
| `--accent-glow` | Glow effect color for interactive elements |
| `--success` | Positive indicator (green `#10b981`) |

### Color Palette

The "Midnight Pro" theme uses a curated dark palette:

- **Background**: Near-black (`#0a0a0f`) with subtle purple undertones
- **Accent**: Violet (`#8b5cf6`) used for CTAs, highlights, and data visualization
- **Success**: Emerald green (`#10b981`) for positive scores (>70)
- **Glass Effects**: `rgba(255, 255, 255, 0.03–0.08)` with `backdrop-filter: blur()`

### Typography

- **Font Family**: `'Outfit', sans-serif`
- **Hierarchy**:
  - `h1` — 800 weight, gradient text effect
  - `h3/h4` — 600 weight, card headers
  - Body — 400 weight
  - Labels — 300 weight, muted color

---

## Component Breakdown

### 1. Navigation Bar
- **Location**: Top of page, fixed
- **Contains**: Logo (`AIAnalyzer`), navigation links (Home, Analyze, Tips)
- **Styling**: Transparent background with glass border bottom

### 2. Background Blobs
- **Purpose**: Animated ambient background decoration
- **Implementation**: Three `div.blob` elements with CSS `@keyframes` animation
- **Colors**: Purple/violet gradients, blurred with `filter: blur()`
- **Animation**: Slow floating movement for a "living" feel

### 3. Hero Section
- **Contains**: Headline with gradient text, subtitle, upload container
- **Gradient Text**: CSS `background: linear-gradient(...)` with `-webkit-background-clip: text`

### 4. Upload Container
- **Job Role Selector** (`<select#jobRole>`):
  - 16 built-in roles + "Other (Specify)" option
  - Selecting "Other" reveals `<input#customRoleInput>` via JS toggle
- **Drop Zone** (`div#dropZone`):
  - Drag & Drop support with visual feedback (`.drag-over` class)
  - Click-to-browse via hidden `<input#fileInput>`
  - SVG upload icon
  - Updates text to show selected filename
- **Job Description Textarea** (`<textarea#jobDescription>`):
  - Optional JD paste for semantic matching
- **Analyze Button** (`button#analyzeBtn`):
  - Triggers the analysis API call

### 5. Results Dashboard (`section#results`)
- **Hidden by default**, shown after successful analysis
- **Score Card**:
  - SVG progress ring (animated `stroke-dashoffset`)
  - Numeric score with counter animation
  - Language badge
  - Radar chart (Chart.js) for section score distribution
- **Feedback Grid** (3 cards):
  - Strengths (green accent)
  - Weaknesses / Areas for Improvement
  - AI Recommendations / Suggestions
- **Analytics Grid** (3 cards):
  - Keyword Density Analysis
  - ATS Keyword Gaps (rendered as `.tag` spans)
  - Formatting & Structure report

### 6. Analysis History (`div#historyList`)
- Stored in `localStorage` under key `resumeHistory`
- Shows last 5 analyses with role name, date, and score
- Persists across browser sessions

### 7. Tips Section
- Three static tip cards with emoji icons
- Topics: Quantify Results, Use Keywords, Keep it Simple

### 8. Loading Overlay (`div#loader`)
- Full-screen overlay with spinner
- Shown during API calls, hidden on completion

### 9. Chat Widget
- **Toggle Button** (`button#chatToggleBtn`): Floating action button, hidden until first analysis
- **Chat Window** (`div#chatWindow`):
  - Header with close button
  - Message area with AI/user message bubbles
  - Input field + send button
  - Supports Enter key to send

---

## State Management

The frontend manages state through simple JavaScript variables:

| Variable | Type | Purpose |
|---|---|---|
| `selectedFile` | `File \| null` | Currently selected resume file |
| `currentAnalysisContext` | `Object \| null` | Full analysis response from backend (passed to chat) |
| `myChart` | `Chart \| null` | Current Chart.js instance (destroyed before re-render) |
| `localStorage['resumeHistory']` | `JSON string` | Array of `{ score, role, date }` objects (max 5) |

---

## Key Functions in `script.js`

| Function | Purpose |
|---|---|
| `handleFileSelect(file)` | Validates file type, updates UI with filename |
| `displayResults(data)` | Master render function — populates all result sections |
| `animateValue(obj, start, end, duration)` | Smooth numeric counter animation using `requestAnimationFrame` |
| `renderScoreChart(breakdown)` | Creates/updates the Chart.js radar chart |
| `populateList(id, items)` | Fills a `<ul>` with `<li>` items from an array |
| `saveToHistory(score, role)` | Persists analysis to localStorage |
| `renderHistory()` | Reads localStorage and renders history items |
| `sendChatMessage()` | Sends user message + context to `/chat` endpoint |
| `addMessage(text, sender)` | Appends a message bubble to the chat DOM |

---

## Animations

| Animation | Implementation | Location |
|---|---|---|
| Background blobs | CSS `@keyframes` with `transform: translate()` | `style.css` |
| Progress ring fill | Dynamic `stroke-dashoffset` via JS | `script.js` → `displayResults()` |
| Score counter | `requestAnimationFrame` loop | `script.js` → `animateValue()` |
| Smooth scroll to results | `scrollIntoView({ behavior: 'smooth' })` | `script.js` → `displayResults()` |
| Drop zone hover | CSS `:hover` and `.drag-over` class | `style.css` |
| Card hover effects | CSS `transform: translateY()` + `box-shadow` | `style.css` |

---

## External Dependencies

| Dependency | CDN URL | Version |
|---|---|---|
| Chart.js | `https://cdn.jsdelivr.net/npm/chart.js` | Latest |
| Google Fonts (Outfit) | `https://fonts.googleapis.com/css2?family=Outfit` | Weights: 300,400,600,800 |

> **Note**: No build tools, bundlers, or package managers are used. The frontend is entirely static and served by FastAPI's `StaticFiles` mount.
