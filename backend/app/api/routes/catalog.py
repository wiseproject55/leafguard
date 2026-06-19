"""Disease catalog browsing and user feedback on predictions."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Diagnosis, Disease, Feedback
from app.schemas.schemas import DiseaseOut, FeedbackCreate

router = APIRouter(tags=["catalog"])


@router.get("/diseases", response_model=List[DiseaseOut])
def list_diseases(db: Session = Depends(get_db)):
    return db.query(Disease).order_by(Disease.common_name).all()


@router.get("/diseases/{label}", response_model=DiseaseOut)
def get_disease(label: str, db: Session = Depends(get_db)):
    disease = db.query(Disease).filter(Disease.label == label).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease


@router.post("/feedback", status_code=201)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == payload.diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    fb = Feedback(
        diagnosis_id=payload.diagnosis_id,
        is_correct=payload.is_correct,
        corrected_label=payload.corrected_label,
        comment=payload.comment,
    )
    db.add(fb)
    db.commit()
    return {"status": "recorded"}
