# Contributing to AI Resume Analyzer

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/Harshitdubey-lab/Resume_analyzer.git
   cd resume-analyzer
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up** the development environment — see [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md)

## Development Workflow

1. Make your changes in the appropriate directory:
   - **Backend logic** → `backend/`
   - **Frontend UI** → `frontend/`
   - **Documentation** → `docs/`
   - **Utility scripts** → `scripts/`

2. **Test your changes** locally:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
   Open `http://localhost:8000` and verify everything works.

3. **Commit** with a clear message:
   ```bash
   git add .
   git commit -m "feat: add keyword density visualization"
   ```

## Commit Message Convention

Use the following prefixes for clarity:

| Prefix | Usage |
|--------|-------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `style:` | CSS / formatting changes (no logic change) |
| `refactor:` | Code restructuring (no feature change) |
| `test:` | Adding or updating tests |

## Submitting a Pull Request

1. **Push** your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a **Pull Request** against the `main` branch of the original repo
3. Describe your changes clearly in the PR description
4. Wait for review and address any feedback

## Project Structure

```
├── backend/       → FastAPI server, NLP engine, scoring logic
├── frontend/      → HTML/CSS/JS UI with Chart.js
├── scripts/       → Utility scripts (report generation, ngrok tunnel)
├── docs/          → Project documentation
└── requirements.txt
```

## Reporting Issues

- Use **GitHub Issues** to report bugs or suggest features
- Include steps to reproduce for bugs
- Include screenshots for UI-related issues

## Code Style

- **Python**: Follow PEP 8 conventions
- **JavaScript**: Use `const`/`let` (no `var`), consistent naming
- **CSS**: Use the existing CSS variable system defined in `style.css`

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
