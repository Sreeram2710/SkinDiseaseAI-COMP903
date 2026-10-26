# EVD-003 — Dataset Class Distribution Analysis

**Project:** SkinDiseaseAI — COMP903
**Date:** 22 October 2026
**Status:** PASS — Image file counts verified

## Objective

Analyse the downloaded skin disease dataset to identify the available disease categories, count image files, and confirm the melanoma and eczema classes required for the proposed CNN experiments.

## Dataset Source

- Platform: Kaggle
- Dataset ID: ismailpromus/skin-diseases-image-dataset
- Directory: data/IMG_CLASSES/
- Total image files: 27,153
- Disease categories: 10

## Class Distribution

| Disease Category | Image Count |
|---|---:|
| Eczema | 1,677 |
| Warts and other viral infections | 2,103 |
| Melanoma | 3,140 |
| Atopic Dermatitis | 1,257 |
| Basal Cell Carcinoma | 3,323 |
| Melanocytic Nevi | 7,970 |
| Benign Keratosis-like Lesions | 2,079 |
| Psoriasis and related diseases | 2,055 |
| Seborrheic Keratoses and other benign tumours | 1,847 |
| Tinea and other fungal infections | 1,702 |
| **Total** | **27,153** |

## Research Findings

The dataset contains all 10 expected disease categories.

The melanoma class contains 3,140 image files, while the eczema class contains 1,677.

The difference in class sizes must be considered when designing the classification experiments.

The largest class is Melanocytic Nevi, containing 7,970 image files.

## Proposed Classification

### EfficientNetB0

Binary classifier:
- Positive class: Melanoma
- Negative class: Other selected skin disease categories

### ResNet50

Binary classifier:
- Positive class: Eczema
- Negative class: Other selected skin disease categories

The final negative-class composition and dataset splitting strategy must be documented before training.

## Method

PowerShell was used to recursively count image files with supported extensions in each disease directory.

The class counts were exported to CSV and checked against the dataset total.

## Limitations

- Image readability has not yet been verified.
- Duplicate images have not yet been identified.
- Folder labels have not been independently validated.
- Counts alone do not establish image quality.
- Train/validation/test splitting has not yet been performed.

## Next Steps

1. Check image readability and corruption.
2. Identify duplicate and near-duplicate images.
3. Review image dimensions and formats.
4. Define preprocessing methods.
5. Prevent data leakage during splitting.
6. Prepare EfficientNetB0 and ResNet50 training pipelines.

## Supporting Evidence

- EVD-003_Class_Counts.csv
- EVD-003_Class_Distribution.txt