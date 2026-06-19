# LeafGuard

AI-Based Crop Disease Detection and Treatment Advisory Web Platform.

A user uploads a photo of a crop leaf; an EfficientNet image classifier predicts
the disease (or healthy state); the platform returns a confidence-ranked
diagnosis and a treatment advisory drawn from a relational catalog. Authenticated
users get a persistent diagnosis history and can submit correctness feedback.

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + React Router |
| Backend | FastAPI (Python 3.11) |
| ML | PyTorch + torchvision EfficientNet-B0 (transfer learning) |
| Database | PostgreSQL (SQLAlchemy ORM, 6 related tables) |
| Auth | JWT (OAuth2 password flow), bcrypt password hashing |
| Packaging | Docker + docker-compose |
| CI | GitHub Actions |

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
  docs/              proposal, functionalities map, report outline
  .github/workflows/ CI
  docker-compose.yml
```

## Quick start (Docker)

```bash
docker compose up --build
# frontend: http://localhost:8080
# backend:  http://localhost:8000/docs
```

The API starts even without a trained model; `/diagnosis/predict` returns
HTTP 503 until a checkpoint exists in `ml/saved_models/`.

## Local development (without Docker)

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

## Train the model

```bash
# place PlantVillage images under ml/data/train and ml/data/val (see ml/data/README.md)
python ml/training/train.py --data-dir ml/data --epochs 10
python ml/training/evaluate.py --data-dir ml/data --split val
```

Outputs `ml/saved_models/leafguard_efficientnet.pt` and `class_index.json`.
Restart the backend to load the new checkpoint.

## Disclaimer

Treatment advisory text in `app/db/seed.py` is scaffolding and must be reviewed
by a qualified agronomist before any real-world use.
