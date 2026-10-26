
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
import csv
import json
import random
from datetime import datetime, timezone

# --------------------------------------------------
# SkinDiseaseAI — Duplicate-Aware Dataset Preparation
# COMP903 Research Project
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "IMG_CLASSES"
OUTPUT_DIR = ROOT / "evidence" / "05_Duplicate_Resolution"

SEED = 42
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}


def calculate_hash(file_path):
    """Calculate SHA-256 from the original file bytes."""
    digest = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(
            lambda: file.read(1024 * 1024), b""
        ):
            digest.update(block)

    return digest.hexdigest()


def save_csv(file_path, rows, columns):
    with open(
        file_path, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=columns
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    print("=" * 60)
    print("SkinDiseaseAI — Dataset Preparation")
    print("=" * 60)

    if not DATA_DIR.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {DATA_DIR}"
        )

    OUTPUT_DIR.mkdir(
        parents=True, exist_ok=True
    )

    class_dirs = sorted(
        p for p in DATA_DIR.iterdir()
        if p.is_dir()
    )

    print(f"Detected disease categories: {len(class_dirs)}")

    records = []
    hash_groups = defaultdict(list)

    # STEP 1 — Build dataset inventory
    for class_dir in class_dirs:
        images = sorted(
            p for p in class_dir.rglob("*")
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTENSIONS
        )

        print(
            f"Scanning {class_dir.name}: "
            f"{len(images)} images"
        )

        for image_path in images:
            image_hash = calculate_hash(image_path)

            record = {
                "image_path": image_path.relative_to(
                    ROOT
                ).as_posix(),
                "class_name": class_dir.name,
                "sha256": image_hash,
                "split": "",
                "status": "",
            }

            records.append(record)
            hash_groups[image_hash].append(record)

    # STEP 2 — Handle conflicting class labels
    accepted_by_class = defaultdict(list)

    conflicting_groups = 0
    excluded_conflicting_images = 0
    excluded_same_class_duplicates = 0

    for image_hash, group in hash_groups.items():

        unique_classes = {
            item["class_name"]
            for item in group
        }

        if len(unique_classes) > 1:
            conflicting_groups += 1
            excluded_conflicting_images += len(group)

            for item in group:
                item["status"] = (
                    "excluded_cross_class_conflict"
                )
                item["split"] = "excluded"

            continue

        # Keep exactly one representative image
        # from each same-class exact-duplicate group.
        representative = group[0]
        representative["status"] = "accepted"

        accepted_by_class[
            representative["class_name"]
        ].append(representative)

        for duplicate in group[1:]:
            duplicate["status"] = (
                "excluded_same_class_duplicate"
            )
            duplicate["split"] = "excluded"
            excluded_same_class_duplicates += 1

    # STEP 3 — Create reproducible class-stratified splits
    rng = random.Random(SEED)

    for class_name in sorted(accepted_by_class):
        items = accepted_by_class[class_name]

        # Stable initial order before random shuffle
        items.sort(key=lambda x: x["image_path"])
        rng.shuffle(items)

        count = len(items)

        train_end = int(count * TRAIN_RATIO)
        val_end = train_end + int(
            count * VAL_RATIO
        )

        for i, item in enumerate(items):
            if i < train_end:
                item["split"] = "train"
            elif i < val_end:
                item["split"] = "validation"
            else:
                item["split"] = "test"

    # STEP 4 — Verify leakage prevention
    split_hashes = defaultdict(set)

    for item in records:
        if item["split"] in {
            "train", "validation", "test"
        }:
            split_hashes[item["sha256"]].add(
                item["split"]
            )

    leakage_groups = sum(
        len(splits) > 1
        for splits in split_hashes.values()
    )

    if leakage_groups != 0:
        raise RuntimeError(
            "Exact-duplicate leakage detected!"
        )

    # STEP 5 — Export manifest
    manifest_path = (
        OUTPUT_DIR / "EVD-005_Dataset_Manifest.csv"
    )

    save_csv(
        manifest_path,
        records,
        [
            "image_path",
            "class_name",
            "sha256",
            "split",
            "status",
        ],
    )

    # STEP 6 — Per-class split summary
    per_class = []

    for class_dir in class_dirs:
        class_records = [
            r for r in records
            if r["class_name"] == class_dir.name
        ]

        counts = Counter(
            r["split"] for r in class_records
        )

        per_class.append({
            "class_name": class_dir.name,
            "original_images": len(class_records),
            "train": counts["train"],
            "validation": counts["validation"],
            "test": counts["test"],
            "excluded": counts["excluded"],
        })

    save_csv(
        OUTPUT_DIR / "EVD-005_Class_Splits.csv",
        per_class,
        [
            "class_name",
            "original_images",
            "train",
            "validation",
            "test",
            "excluded",
        ],
    )

    # STEP 7 — Overall report
    overall = Counter(
        r["split"] for r in records
    )

    summary = {
        "project": "SkinDiseaseAI COMP903",
        "created_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "random_seed": SEED,
        "original_images": len(records),
        "original_categories": len(class_dirs),
        "unique_content_hashes": len(hash_groups),
        "cross_class_conflict_groups": conflicting_groups,
        "excluded_conflicting_images":
            excluded_conflicting_images,
        "excluded_same_class_duplicates":
            excluded_same_class_duplicates,
        "training_images": overall["train"],
        "validation_images": overall["validation"],
        "test_images": overall["test"],
        "total_excluded": overall["excluded"],
        "exact_duplicate_leakage_groups":
            leakage_groups,
        "split_method":
            "Class-stratified, SHA-256 deduplicated",
        "limitations": [
            "Cross-class labels require expert review.",
            "Only byte-identical duplicates are detected.",
            "Near-duplicate and patient-level leakage "
            "have not been ruled out.",
            "No clinical validation has been performed."
        ],
        "class_distribution": per_class,
    }

    summary_path = (
        OUTPUT_DIR / "EVD-005_Summary.json"
    )

    with open(
        summary_path, "w", encoding="utf-8"
    ) as file:
        json.dump(summary, file, indent=2)

    print("\n" + "=" * 60)
    print("DATASET PREPARATION SUMMARY")
    print("=" * 60)

    print(f"Original images: {len(records)}")
    print(f"Cross-class conflict groups: {conflicting_groups}")
    print(
        "Excluded conflicting images: "
        f"{excluded_conflicting_images}"
    )
    print(
        "Excluded same-class duplicates: "
        f"{excluded_same_class_duplicates}"
    )

    print(f"Training: {overall['train']}")
    print(f"Validation: {overall['validation']}")
    print(f"Testing: {overall['test']}")
    print(f"Total excluded: {overall['excluded']}")

    print(
        "Exact-duplicate leakage groups: "
        f"{leakage_groups}"
    )

    print(f"\nEvidence saved to: {OUTPUT_DIR}")
    print("Original dataset remains unchanged.")

    if leakage_groups == 0:
        print("\nRESULT: PASS — No exact-duplicate leakage")


if __name__ == "__main__":
    main()
