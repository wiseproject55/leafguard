"""Diagnosis routes: predict from an uploaded leaf image, attach the
treatment advisory, persist the diagnosis, and list user history."""
import io
import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.api.deps import get_optional_user
from app.db.session import get_db
from app.models.entities import Diagnosis, Disease, User
from app.schemas.schemas import DiagnosisOut, DiseaseOut, PredictionResult
from app.services.inference import inference_service

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 8 * 1024 * 1024


@router.post("/predict", response_model=PredictionResult)
async def predict(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported image type")

    raw = await file.read()
    if len(raw) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image too large (max 8MB)")

    try:
        image = Image.open(io.BytesIO(raw))
        image.verify()
        image = Image.open(io.BytesIO(raw))
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Invalid image file")

    try:
        result = inference_service.predict(image)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    fname = f"{uuid.uuid4().hex}_{file.filename}"
    with open(os.path.join(UPLOAD_DIR, fname), "wb") as f:
        f.write(raw)

    record = Diagnosis(
        user_id=user.id if user else None,
        image_filename=fname,
        predicted_label=result["predicted_label"],
        confidence=result["confidence"],
    )
    db.add(record)
    db.commit()

    disease = (
        db.query(Disease)
        .filter(Disease.label == result["predicted_label"])
        .first()
    )
    return PredictionResult(
        predicted_label=result["predicted_label"],
        confidence=result["confidence"],
        top_k=result["top_k"],
        disease=DiseaseOut.model_validate(disease) if disease else None,
    )


@router.get("/history", response_model=List[DiagnosisOut])
def history(
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Login required for history")
    return (
        db.query(Diagnosis)
        .filter(Diagnosis.user_id == user.id)
        .order_by(Diagnosis.created_at.desc())
        .all()
    )
