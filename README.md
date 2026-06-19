<div align="center">

<img src="docs/assets/logo.png" alt="LeafGuard logo" width="160" />

# LeafGuard  Wise Project · OUK Capstone

AI-Based Crop Disease Detection and Treatment Advisory Web Platform

![Python](https://img.shields.io/badge/python-3.11-blue)
![Java Script](https://img.shields.io/badge/javascript-ES2022-f1e05a)
![Languages](https://img.shields.io/badge/languages-Python%20%7C%20JavaScript%20%7C%20HTML%20%7C%20CSS%20%7C%20Dockerfile-informational)

</div>

## Overview

A user uploads a photo of a crop leaf. An EfficientNet-B0 (transfer learning) image classifier predicts the disease or healthy state. The platform returns a confidence-ranked diagnosis and a treatment advisory drawn from a relational catalog. Authenticated users get a persistent diagnosis history and can submit correctness feedback.

## Documentation

- [Functionalities Map](docs/FUNCTIONALITIES.md)
- [Proposal Skeleton](docs/PROPOSAL_SKELETON.md)
- Showcase page: [docs/index.html](docs/index.html)

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + React Router |
| Backend | FastAPI (Python 3.11) |
| ML | PyTorch + torchvision EfficientNet-B0 (transfer learning) |
| Database | PostgreSQL (SQLAlchemy ORM, 6 related tables) |
| Auth | JWT (OAuth2 password flow), bcrypt password hashing |
| Packaging | Docker + docker-compose |
| CI | GitHub Actions (`.github/workflows/ci.yml`) |

## Functionalities

14 implemented functionalities spanning auth, inference, advisory, history, and ops. Full list with endpoint references: [docs/FUNCTIONALITIES.md](docs/FUNCTIONALITIES.md).

| # | Functionality | Where |
|---|---------------|-------|
| 1 | User registration | `POST /auth/register` |
| 2 | JWT login / session | `POST /auth/login`, `GET /auth/me` |
| 3 | Leaf image upload + validation | `POST /diagnosis/predict` |
| 4 | EfficientNet disease classification | `services/inference.py` |
| 5 | Top-K confidence ranking | `services/inference.py` |
| 6 | Treatment advisory join | `routes/diagnosis.py` |
| 7 | Persistent per-user diagnosis history | `GET /diagnosis/history` |
| 8 | Disease catalog browsing | `GET /diseases`, `GET /diseases/{label}` |
| 9 | User feedback on predictions | `POST /feedback` |
| 10 | Model training pipeline | `ml/training/train.py` |
| 11 | Model evaluation | `ml/training/evaluate.py` |
| 12 | Health/readiness endpoint | `GET /health` |
| 13 | Containerized deployment | `docker-compose.yml` |
| 14 | CI pipeline | `.github/workflows/ci.yml` |

## Repository layout

```
leafguard/
  backend/          FastAPI service
    app/
      api/routes/    auth, diagnosis, catalog endpoints
      core/          config, security
      db/            session, seed
      models/        SQLAlchemy entities (6 tables)
      schemas/       Pydantic contracts
      services/      inference service (EfficientNet)
  ml/
    training/        train.py, evaluate.py
    data/            dataset (PlantVillage layout, gitignored)
    saved_models/    checkpoint + class_index.json (gitignored)
  frontend/          React + Vite SPA
  docs/              proposal, functionalities map, showcase page
  .github/workflows/ CI
  docker-compose.yml
```

## Installation

### Quick start (Docker)

```bash
docker compose up --build
# frontend: http://localhost:8080
# backend:  http://localhost:8000/docs
```

The API starts even without a trained model; `/diagnosis/predict` returns HTTP 503 until a checkpoint exists in `ml/saved_models/`.

### Local development (without Docker)

Backend:
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # adjust POSTGRES_* and SECRET_KEY
python -m app.db.seed         # populate crops/diseases/treatments
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev                   # http://localhost:5173, proxies /api to :8000
```

### Train the model

```bash
# place PlantVillage images under ml/data/train and ml/data/val (see ml/data/README.md)
python ml/training/train.py --data-dir ml/data --epochs 10
python ml/training/evaluate.py --data-dir ml/data --split val
```

Outputs `ml/saved_models/leafguard_efficientnet.pt` and `class_index.json`. Restart the backend to load the new checkpoint.

## Technologies used

**Languages:** Python · JavaScript · HTML · CSS · Dockerfile

**Frameworks/Tools:** React · Vite · FastAPI · PyTorch · torchvision · PostgreSQL · SQLAlchemy · Docker · GitHub Actions

## Team members — Wise Project

| Member | Role | Description | Links |
|--------|------|--------------|-------|
| Alvin Mwakingali | ML / Data | *Demo By alivn* | *Demo By alivn* |
| David Ndegwa | Backend | *Demo By alivn* | *Demo By alivn* |
| Grace Omukitsa | Frontend | *Demo By alivn* | *Demo By alivn* |
| Mollenta Achieng | DevOps / QA | *Demo By alivn* | *Demo By alivn* |

Names and roles sourced from `docs/index.html` team section. Photos, bios, and LinkedIn/GitHub/email links not present in any uploaded file this is just a demo

## Disclaimer

Treatment advisory text in `app/db/seed.py` is scaffolding and must be reviewed by a qualified agronomist before any real-world use.
