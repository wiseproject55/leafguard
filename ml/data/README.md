# Dataset

This project is built around the **PlantVillage** dataset (publicly available,
healthy + diseased leaf images organized by `Crop___Condition` folders).

## Expected layout

```
ml/data/
  train/
    Tomato___Early_blight/
    Tomato___Late_blight/
    Potato___Late_blight/
    ...
  val/
    Tomato___Early_blight/
    ...
```

## Notes

- Folder names become class labels and must match the labels in
  `backend/app/db/seed.py` for the treatment advisory join to resolve.
- Use a stratified train/val split (e.g. 80/20) so every class appears in both.
- `class_index.json` is generated automatically by `train.py` from the
  `ImageFolder` class ordering — do not hand-edit it.

## Reproduce

1. Place images under `ml/data/train` and `ml/data/val`.
2. `python ml/training/train.py --data-dir ml/data --epochs 10`
3. `python ml/training/evaluate.py --data-dir ml/data --split val`
