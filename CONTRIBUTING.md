# Contributing Guide

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/seed_products.py
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend/simulator
npm install
npm run dev
```

## Testing

```bash
cd backend
pytest --cov=app --cov-report=html
```

Target: 90% coverage

## Code Style

- **Python:** Black, isort, pylint
- **JavaScript:** ESLint (if added)
- Follow existing patterns

## Pull Request Process

1. Create feature branch
2. Add tests (TDD preferred)
3. Ensure all tests pass
4. Update documentation
5. Submit PR with description

## Architecture Guidelines

- Services must be protocol-agnostic
- Follow gateway pattern
- Add tests for new features
- Document decisions in DECISION_LOG.md

