import os
from pathlib import Path

import cv2
from ultralytics import YOLO

_root = Path(__file__).resolve().parent.parent
_path = Path(os.environ.get("MODEL_PATH", _root / "models" / "best.pt"))
_model = None


def _model_load():
    global _model
    if _model is None:
        if not _path.is_file():
            raise FileNotFoundError(f"Model not found: {_path}")
        _model = YOLO(str(_path))
    return _model


def predict_image(image_path: str):
    model = _model_load()
    try:
        results = model(image_path)
    except Exception as exc:
        raise ValueError("Bad or unreadable image.") from exc

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")

    h, w = img.shape[:2]
    area = h * w
    damage = 0
    dets = []

    for r in results:
        if not r.boxes:
            continue
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            damage += (x2 - x1) * (y2 - y1)
            dets.append({
                "label": model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]) * 100, 2),
                "bbox": [x1, y1, x2, y2],
            })

    return {
        "detections": dets,
        "total_damage_percent": round((damage / area) * 100, 2) if area else 0,
    }
