# Functionalities Map

The OUK guidelines require a **minimum of 10–12 functionalities** and explicitly
disallow simple inventory systems, CRUD-only apps, and single-database systems.
LeafGuard is an AI image-classification platform with a multi-table relational
backend, satisfying both constraints. Implemented functionalities:

| # | Functionality | Where | Status |
|---|---------------|-------|--------|
| 1 | User registration | `POST /auth/register` | Implemented |
| 2 | JWT login / authenticated session | `POST /auth/login`, `GET /auth/me` | Implemented |
| 3 | Leaf image upload with validation (type/size/decode) | `POST /diagnosis/predict` | Implemented |
| 4 | EfficientNet disease classification (inference) | `services/inference.py` | Implemented |
| 5 | Top-K confidence ranking | `services/inference.py` | Implemented |
| 6 | Treatment advisory join (disease → treatments) | `routes/diagnosis.py` | Implemented |
| 7 | Persistent per-user diagnosis history | `GET /diagnosis/history` | Implemented |
| 8 | Disease catalog browsing | `GET /diseases`, `GET /diseases/{label}` | Implemented |
| 9 | User feedback on predictions (active-learning signal) | `POST /feedback` | Implemented |
| 10 | Model training pipeline (transfer learning + augmentation) | `ml/training/train.py` | Implemented |
| 11 | Model evaluation (overall + per-class accuracy) | `ml/training/evaluate.py` | Implemented |
| 12 | Health/readiness endpoint (model load state) | `GET /health` | Implemented |
| 13 | Containerized deployment (compose: db + api + web) | `docker-compose.yml` | Implemented |
| 14 | CI pipeline (backend import + frontend build) | `.github/workflows/ci.yml` | Implemented |

## Possible enhancements (Chapter 6 — Future Work)

- Role-based access (agronomist review queue using the `role` field + feedback).
- Offline/PWA mode for low-connectivity field use.
- Grad-CAM heatmap overlay showing the lesion region driving the prediction.
- SMS/USSD interface for feature-phone access.
- Retraining loop that consumes accumulated `feedback` rows.
