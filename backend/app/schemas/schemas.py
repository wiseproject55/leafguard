"""Pydantic schemas (API contracts)."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Auth ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Treatments / Diseases ----------
class TreatmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: str
    title: str
    instructions: str


class DiseaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    label: str
    common_name: str
    description: Optional[str]
    is_healthy: bool
    treatments: List[TreatmentOut] = []


# ---------- Diagnosis ----------
class PredictionResult(BaseModel):
    predicted_label: str
    confidence: float
    top_k: List[dict]
    disease: Optional[DiseaseOut] = None


class DiagnosisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_filename: str
    predicted_label: str
    confidence: float
    created_at: datetime


# ---------- Feedback ----------
class FeedbackCreate(BaseModel):
    diagnosis_id: int
    is_correct: bool
    corrected_label: Optional[str] = None
    comment: Optional[str] = None
