"""Seed the catalog with crops, diseases, and treatment advisories.

Disease labels follow the PlantVillage dataset naming convention
(Crop___Condition). Treatment text is generic advisory scaffolding and
MUST be reviewed/replaced with agronomist-validated guidance before any
real-world deployment.

Run:  python -m app.db.seed
"""
from app.db.session import Base, SessionLocal, engine
from app.models.entities import Crop, Disease, Treatment

# (crop, scientific_name)
CROPS = {
    "Tomato": "Solanum lycopersicum",
    "Potato": "Solanum tuberosum",
    "Maize": "Zea mays",
    "Pepper": "Capsicum annuum",
}

# label -> (crop, common_name, is_healthy, description)
DISEASES = {
    "Tomato___Early_blight": ("Tomato", "Tomato Early Blight", False,
        "Fungal disease (Alternaria solani) causing concentric brown lesions on older leaves."),
    "Tomato___Late_blight": ("Tomato", "Tomato Late Blight", False,
        "Caused by Phytophthora infestans; water-soaked lesions that spread rapidly in humid conditions."),
    "Tomato___Leaf_Mold": ("Tomato", "Tomato Leaf Mold", False,
        "Caused by Passalora fulva; yellow spots on upper leaf surface, olive mold beneath."),
    "Tomato___healthy": ("Tomato", "Healthy Tomato", True,
        "No disease detected."),
    "Potato___Early_blight": ("Potato", "Potato Early Blight", False,
        "Alternaria solani lesions with concentric rings on lower leaves."),
    "Potato___Late_blight": ("Potato", "Potato Late Blight", False,
        "Phytophthora infestans; rapidly spreading dark lesions, major yield threat."),
    "Potato___healthy": ("Potato", "Healthy Potato", True,
        "No disease detected."),
    "Maize___Common_rust": ("Maize", "Maize Common Rust", False,
        "Puccinia sorghi; reddish-brown pustules on both leaf surfaces."),
    "Maize___Northern_Leaf_Blight": ("Maize", "Northern Leaf Blight", False,
        "Exserohilum turcicum; long elliptical grey-green lesions."),
    "Maize___healthy": ("Maize", "Healthy Maize", True,
        "No disease detected."),
    "Pepper___Bacterial_spot": ("Pepper", "Pepper Bacterial Spot", False,
        "Xanthomonas spp.; water-soaked spots becoming necrotic."),
    "Pepper___healthy": ("Pepper", "Healthy Pepper", True,
        "No disease detected."),
}

# label -> list of (category, title, instructions)
TREATMENTS = {
    "Tomato___Early_blight": [
        ("cultural", "Sanitation", "Remove and destroy infected lower leaves; rotate crops yearly."),
        ("chemical", "Fungicide", "Apply a protectant fungicide (e.g. chlorothalonil or mancozeb) per label rates."),
    ],
    "Tomato___Late_blight": [
        ("cultural", "Airflow & spacing", "Increase plant spacing; avoid overhead irrigation."),
        ("chemical", "Fungicide", "Apply systemic fungicides early; remove infected plants promptly."),
    ],
    "Potato___Late_blight": [
        ("cultural", "Field hygiene", "Destroy volunteer plants and cull piles; plant certified seed."),
        ("chemical", "Fungicide", "Preventive fungicide programme during cool, wet weather."),
    ],
    "Maize___Common_rust": [
        ("cultural", "Resistant varieties", "Plant rust-resistant hybrids where available."),
        ("chemical", "Fungicide", "Foliar fungicide if infection appears before tasseling under high pressure."),
    ],
}


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        crop_objs = {}
        for name, sci in CROPS.items():
            c = db.query(Crop).filter(Crop.name == name).first()
            if not c:
                c = Crop(name=name, scientific_name=sci)
                db.add(c)
                db.flush()
            crop_objs[name] = c

        for label, (crop, common, healthy, desc) in DISEASES.items():
            d = db.query(Disease).filter(Disease.label == label).first()
            if not d:
                d = Disease(
                    crop_id=crop_objs[crop].id,
                    label=label,
                    common_name=common,
                    is_healthy=healthy,
                    description=desc,
                )
                db.add(d)
                db.flush()
            for cat, title, instr in TREATMENTS.get(label, []):
                exists = (
                    db.query(Treatment)
                    .filter(Treatment.disease_id == d.id, Treatment.title == title)
                    .first()
                )
                if not exists:
                    db.add(Treatment(disease_id=d.id, category=cat, title=title, instructions=instr))

        db.commit()
        print(f"Seeded {len(CROPS)} crops, {len(DISEASES)} diseases.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
