
"""
COMP903 — Skin Disease Image Quality Analysis

Purpose:
    Validate the extracted skin disease dataset and
    produce reproducible research evidence.

Checks:
    1. Total image file count
    2. Image readability and corruption
    3. Image dimensions
    4. Image colour modes
    5. Image formats
    6. Exact duplicate files using SHA-256

Outputs:
    evidence/04_Image_Quality/

Important:
    Original dataset images are never modified.
"""

from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from PIL import Image
import hashlib
import csv
import json


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data" / "IMG_CLASSES"

OUTPUT_DIR = ROOT / "evidence" / "04_Image_Quality"

EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# --------------------------------------------------
# 2. CSV OUTPUT HELPER
# --------------------------------------------------

def save_csv(filename, rows, fieldnames):

    output_path = OUTPUT_DIR / filename

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {output_path.name}")


# --------------------------------------------------
# 3. MAIN IMAGE QUALITY ANALYSIS
# --------------------------------------------------

def main():

    print("=" * 60)
    print("COMP903 — SKIN DISEASE IMAGE QUALITY ANALYSIS")
    print("=" * 60)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DATA_DIR.is_dir():

        raise FileNotFoundError(
            f"Dataset directory not found: {DATA_DIR}"
        )

    files = sorted(
        path
        for path in DATA_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in EXTENSIONS
    )

    total_files = len(files)

    print(f"\nDataset location: {DATA_DIR}")
    print(f"Total image files found: {total_files}")

    if total_files == 0:
        raise RuntimeError("No image files found.")

    # Statistics
    class_counts = Counter()
    image_modes = Counter()
    image_formats = Counter()
    dimensions = Counter()

    # SHA-256 -> image paths
    hashes = defaultdict(list)

    corrupt_files = []
    image_records = []

    # ----------------------------------------------
    # 4. VALIDATE EVERY IMAGE
    # ----------------------------------------------

    for index, path in enumerate(files, start=1):

        relative_path = path.relative_to(DATA_DIR)

        class_name = relative_path.parts[0]

        class_counts[class_name] += 1

        try:

            # Validate image structure.
            with Image.open(path) as img:
                img.verify()

            # Reopen and decode pixel data.
            with Image.open(path) as img:

                img.load()

                width, height = img.size
                mode = img.mode
                image_format = img.format or "Unknown"

            # --------------------------------------
            # 5. CORRECT SHA-256 FILE HANDLING
            # --------------------------------------

            # The context manager closes the file
            # automatically after the hash is made.

            with path.open("rb") as image_file:

                sha256 = hashlib.file_digest(
                    image_file,
                    "sha256"
                ).hexdigest()

            # --------------------------------------
            # 6. RECORD IMAGE STATISTICS
            # --------------------------------------

            hashes[sha256].append(
                str(relative_path)
            )

            image_modes[mode] += 1

            image_formats[image_format] += 1

            dimensions[
                f"{width}x{height}"
            ] += 1

            image_records.append({

                "file": str(relative_path),

                "class": class_name,

                "width": width,

                "height": height,

                "mode": mode,

                "format": image_format,

                "sha256": sha256
            })

        except Exception as exc:

            corrupt_files.append({

                "file": str(relative_path),

                "error": str(exc)
            })

        if index % 1000 == 0 or index == total_files:

            print(
                f"Checked {index}/{total_files} images"
            )

    # ----------------------------------------------
    # 7. DETECT EXACT DUPLICATES
    # ----------------------------------------------

    duplicate_rows = []

    duplicate_groups = 0

    for digest, paths in hashes.items():

        if len(paths) > 1:

            duplicate_groups += 1

            for duplicate_path in paths:

                duplicate_rows.append({

                    "sha256": digest,

                    "file": duplicate_path,

                    "group_size": len(paths)
                })

    # ----------------------------------------------
    # 8. SAVE IMAGE INVENTORY
    # ----------------------------------------------

    save_csv(

        "EVD-004_Image_Inventory.csv",

        image_records,

        [
            "file",
            "class",
            "width",
            "height",
            "mode",
            "format",
            "sha256"
        ]
    )

    # ----------------------------------------------
    # 9. SAVE CORRUPT IMAGE REPORT
    # ----------------------------------------------

    save_csv(

        "EVD-004_Corrupt_Images.csv",

        corrupt_files,

        [
            "file",
            "error"
        ]
    )

    # ----------------------------------------------
    # 10. SAVE EXACT DUPLICATE REPORT
    # ----------------------------------------------

    save_csv(

        "EVD-004_Exact_Duplicates.csv",

        duplicate_rows,

        [
            "sha256",
            "file",
            "group_size"
        ]
    )

    # ----------------------------------------------
    # 11. GENERATE RESEARCH SUMMARY
    # ----------------------------------------------

    summary = {

        "date": datetime.now().isoformat(),

        "dataset_path": str(DATA_DIR),

        "total_files": total_files,

        "readable_files": len(image_records),

        "corrupt_files": len(corrupt_files),

        "duplicate_groups": duplicate_groups,

        "files_in_duplicate_groups": len(
            duplicate_rows
        ),

        "class_counts": dict(class_counts),

        "image_modes": dict(image_modes),

        "image_formats": dict(image_formats),

        "top_dimensions": dimensions.most_common(
            20
        ),

        "limitations": [
            "Exact duplicates are detected using SHA-256.",
            "Near-duplicate images are not detected.",
            "Incorrect disease labels are not identified.",
            "Clinical correctness is not established."
        ]
    }

    summary_path = (
        OUTPUT_DIR / "EVD-004_Summary.json"
    )

    with summary_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=2
        )

    # ----------------------------------------------
    # 12. PRINT FINAL RESULTS
    # ----------------------------------------------

    print("\n" + "=" * 60)

    print("IMAGE QUALITY ANALYSIS COMPLETED")

    print("=" * 60)

    print(f"Total files: {total_files}")

    print(
        f"Readable files: {len(image_records)}"
    )

    print(
        f"Corrupt files: {len(corrupt_files)}"
    )

    print(
        f"Exact duplicate groups: {duplicate_groups}"
    )

    print(
        "Files in duplicate groups: "
        f"{len(duplicate_rows)}"
    )

    print("\nImages per disease category:")

    for class_name, count in sorted(
        class_counts.items()
    ):

        print(
            f"  {class_name}: {count}"
        )

    print("\nImage colour modes:")

    for mode, count in image_modes.items():

        print(f"  {mode}: {count}")

    print("\nImage formats:")

    for image_format, count in image_formats.items():

        print(
            f"  {image_format}: {count}"
        )

    print("\nEvidence saved to:")

    print(OUTPUT_DIR)

    print("\nAnalysis finished successfully.")


# --------------------------------------------------
# 13. PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    main()
