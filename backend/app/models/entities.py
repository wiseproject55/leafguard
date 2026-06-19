"""ORM models. Multi-table relational schema (satisfies the
'no single-database / no CRUD-only' guideline through related entities)."""
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship

from app.db.session import Base


def _utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="farmer")  # farmer | agronomist | admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    diagnoses = relationship("Diagnosis", back_populates="user")


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    scientific_name = Column(String(255), nullable=True)

    diseases = relationship("Disease", back_populates="crop")


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    label = Column(String(255), unique=True, nullable=False)  # model class label
    common_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_healthy = Column(Boolean, default=False)

    crop = relationship("Crop", back_populates="diseases")
    treatments = relationship("Treatment", back_populates="disease")


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    category = Column(String(50), default="chemical")  # chemical | organic | cultural
    title = Column(String(255), nullable=False)
    instructions = Column(Text, nullable=False)

    disease = relationship("Disease", back_populates="treatments")


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_filename = Column(String(512), nullable=False)
    predicted_label = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    user = relationship("User", back_populates="diagnoses")
    feedback = relationship("Feedback", back_populates="diagnosis", uselist=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    corrected_label = Column(String(255), nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    diagnosis = relationship("Diagnosis", back_populates="feedback")
