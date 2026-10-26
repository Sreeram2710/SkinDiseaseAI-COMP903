"""Evaluate the trained melanoma-vs-other EfficientNetB0 on the held-out manifest split."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
from sklearn.metrics import (
    accuracy_score, average_precision_score, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
    classification_report, ConfusionMatrixDisplay,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence/05_Duplicate_Resolution/EVD-005_Dataset_Manifest.csv"
MODEL = ROOT / "models/efficientnetb0_melanoma_best.keras"
OUT = ROOT / "results/efficientnetb0_melanoma_test"
BATCH_SIZE = 32
THRESHOLD = 0.5


def resolve_image(image_path: str) -> Path:
    candidate = Path(image_path.replace("\\", "/"))
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_image(path: Path) -> np.ndarray:
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = im.resize((224, 224), Image.Resampling.BILINEAR)
        return np.asarray(im, dtype=np.float32)  # EfficientNet expects 0..255


def main() -> None:
    if not MANIFEST.is_file() or not MODEL.is_file():
        raise FileNotFoundError(f"Check manifest {MANIFEST} and model {MODEL}")

    with MANIFEST.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    required = {"image_path", "class_name", "sha256", "split", "status"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Unexpected manifest columns or empty file")

    accepted = [r for r in rows if r["status"].strip().lower() == "accepted"]
    by_hash = defaultdict(set)
    for row in accepted:
        by_hash[row["sha256"].strip()].add(row["split"].strip().lower())
    leakage = sum(len(splits) > 1 for splits in by_hash.values())
    if leakage:
        raise ValueError(f"STOP: {leakage} exact hashes appear in multiple splits")

    test = [r for r in accepted if r["split"].strip().lower() == "test"]
    if not test:
        raise ValueError("No accepted test rows")
    paths = [resolve_image(r["image_path"]) for r in test]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"{len(missing)} test image files missing. Example: {missing[0]}")

    # The dataset's exact positive folder name, confirmed in the Colab notebook.
    positive = "2. Melanoma 15.75k"
    if not any(r["class_name"].strip() == positive for r in test):
        raise ValueError("Melanoma class folder not found in test manifest; inspect class naming")
    y_true = np.array([int(r["class_name"].strip() == positive) for r in test], dtype=np.int32)
    if np.unique(y_true).size != 2:
        raise ValueError("Both positive and negative test classes are required")

    print(f"TEST IMAGES: {len(test)} (melanoma={y_true.sum()}, other={len(y_true)-y_true.sum()})")
    print("No exact SHA-256 hash overlaps across accepted splits: PASS")
    print("Loading trained model...")
    model = tf.keras.models.load_model(str(MODEL), compile=False)
    if model.input_shape[1:] != (224, 224, 3) or model.output_shape[-1] != 1:
        raise ValueError(f"Unexpected input/output shape: {model.input_shape}, {model.output_shape}")

    scores = []
    for start in range(0, len(paths), BATCH_SIZE):
        batch = np.stack([load_image(p) for p in paths[start:start + BATCH_SIZE]])
        pred = model.predict(batch, verbose=0).reshape(-1)
        if not np.all(np.isfinite(pred)) or np.any((pred < 0) | (pred > 1)):
            raise ValueError("Model produced invalid scores")
        scores.extend(pred.astype(float).tolist())
        print(f"Evaluated {min(start+BATCH_SIZE, len(paths))}/{len(paths)} images", end="\r", flush=True)
    print()
    y_scores = np.asarray(scores)
    y_pred = (y_scores >= THRESHOLD).astype(np.int32)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    metrics = {
        "model": "EfficientNetB0 melanoma vs other classes",
        "split": "test", "test_images": int(len(test)),
        "positives": int(y_true.sum()), "negatives": int(len(y_true)-y_true.sum()),
        "threshold": THRESHOLD,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall_sensitivity": float(recall_score(y_true, y_pred, zero_division=0)),
        "specificity": float(cm[0, 0] / cm[0].sum()),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_scores)),
        "average_precision": float(average_precision_score(y_true, y_scores)),
        "confusion_matrix_rows_true_0_1_cols_pred_0_1": cm.tolist(),
        "exact_hash_overlap": 0,
        "limitations": "Not clinically validated. Near-duplicate/patient leakage not excluded; verify test split was not used in model training or model selection.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    with (OUT / "predictions.csv").open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(["image_path", "class_name", "sha256", "true_melanoma", "melanoma_score", "predicted_melanoma"])
        writer.writerows((row["image_path"], row["class_name"], row["sha256"], int(y), float(s), int(pred)) for row, y, s, pred in zip(test, y_true, y_scores, y_pred))
    (OUT / "classification_report.txt").write_text(
        classification_report(y_true, y_pred, labels=[0, 1], target_names=["Other classes", "Melanoma"], zero_division=0),
        encoding="utf-8",
    )
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ConfusionMatrixDisplay(cm, display_labels=["Other", "Melanoma"]).plot(ax=ax, cmap="Blues", colorbar=False, values_format="d")
    ax.set_title("EfficientNetB0 — Held-out Test Set")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=180)
    plt.close(fig)
    print(json.dumps(metrics, indent=2))
    print("EVALUATION COMPLETE. Results:", OUT)


if __name__ == "__main__":
    main()
