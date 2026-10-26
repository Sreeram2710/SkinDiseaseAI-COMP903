# COMP903 — Supervisor Evidence Index

## Research Project
Deep Learning-Based Image Classification for
Automated Detection of Skin Diseases

## Evidence Summary

| ID | Component | Status | Supporting Evidence |
|---|---|---|---|
| EVD-002 | Dataset download and ZIP verification | PASS | [Description](evidence/02_Dataset_Download/EVD-002_Description.md) |
| EVD-003 | Dataset class distribution | PASS — file counts | [Class Counts](evidence/03_Dataset_Analysis/EVD-003_Class_Counts.csv) |
| EVD-004 | Image quality and duplicate checks | Pending | To be added |
| EVD-005 | Image preprocessing | Pending | To be added |
| EVD-006 | Train/validation/test splitting | Pending | To be added |
| EVD-007 | EfficientNetB0 melanoma model | Pending | To be added |
| EVD-008 | ResNet50 eczema model | Pending | To be added |
| EVD-009 | Explainable AI — Grad-CAM | Pending | To be added |
| EVD-010 | Streamlit application | Pending | To be added |
| EVD-011 | Application testing | Pending | To be added |

## Verified Dataset Summary

- Dataset: Kaggle Skin Diseases Image Dataset
- Dataset ID: ismailpromus/skin-diseases-image-dataset
- Total image files: 27,153
- Disease categories: 10
- Melanoma images: 3,140
- Eczema images: 1,677
- Archive size: 5.19 GB

## Research Classification

**EfficientNetB0:** Melanoma versus other included diseases.

**ResNet50:** Eczema versus other included diseases.

## Research Evidence Rules

1. Save screenshots and experimental outputs in the appropriate evidence folder.
2. Record the objective, method, actual result and limitations.
3. Mark an experiment PASS only after verification.
4. Keep original research outputs unchanged.
5. Do not publish private images, API credentials or restricted dataset files.

## Progress Report 1

Target submission: 29 October 2026.

Include verified progress, encountered problems,
solutions and the plan for the next reporting period.
## EVD-004 - Image Quality and Duplicate Analysis
[Open EVD-004 Research Report](evidence/04_Image_Quality/EVD-004_Description.md)

---

## EVD-006 — Application Interface and Functional Testing

**Date:** 22 October 2026  
**Status:** Initial application testing completed

The SkinDiseaseAI Streamlit research application was tested to verify core interface functionality before model integration.

### Verified functionality
- Overview dashboard displaying dataset statistics
- JPEG image upload and image metadata display
- EfficientNetB0 and ResNet50 comparison interface
- Evaluation metrics correctly marked as pending

### Evidence
- [Application Testing Report](evidence/06_Application_Testing/EVD-006_Description.md)
- [Overview Dashboard](evidence/06_Application_Testing/EVD-006_Overview_Dashboard.png)
- [Image Upload Test](evidence/06_Application_Testing/EVD-006_Image_Upload_Test.png)
- [Model Comparison](evidence/06_Application_Testing/EVD-006_Model_Comparison.png)
- [Research Evidence](evidence/06_Application_Testing/EVD-006_Research_Evidence.png)
- [About Project](evidence/06_Application_Testing/EVD-006_About_Project.png)

**Current limitation:** Model training, predictions and Grad-CAM visualisations remain pending.

**Clinical disclaimer:** This is research software, not a clinically validated diagnostic tool.


---

## EVD-005 — Duplicate Resolution and Dataset Preprocessing

**Date:** 22 October 2026  
**Status:** Completed — exact-duplicate verification passed

### Dataset Results

| Measure | Result |
|---|---:|
| Original images | 27,153 |
| Disease categories | 10 |
| Cross-class duplicate groups | 117 |
| Images excluded for conflicting labels | 240 |
| Redundant same-class duplicates excluded | 501 |
| Total excluded images | 741 |
| Training images | 18,484 |
| Validation images | 3,957 |
| Testing images | 3,971 |
| Exact-duplicate leakage groups | 0 |

### Evidence

- [Preprocessing Research Report](evidence/05_Duplicate_Resolution/EVD-005_Description.md)
- [Dataset Split Verification Screenshot](evidence/05_Duplicate_Resolution/EVD-005_Dataset_Split_Verification.png)
- [Dataset Manifest](evidence/05_Duplicate_Resolution/EVD-005_Dataset_Manifest.csv)
- [Class Split Summary](evidence/05_Duplicate_Resolution/EVD-005_Class_Splits.csv)
- [Preprocessing Summary](evidence/05_Duplicate_Resolution/EVD-005_Summary.json)

### Research Limitations

Exact-duplicate leakage was not detected. Near-duplicate and patient-level leakage have not yet been ruled out. The dataset remains subject to label-quality review and clinical validation.

**Next research activity:** Train and evaluate EfficientNetB0 and ResNet50 using the prepared dataset.

## EVD-007 — EfficientNetB0 Model Evaluation

**Status:** Evaluation completed on 26 October 2026.

- Test images evaluated: 3,971
- Accuracy: 96.27%
- Precision: 87.82%
- Recall: 79.62%
- F1-score: 83.52%
- ROC-AUC: 0.9838
- Exact hash overlaps across accepted splits: 0

### Evidence
- [Evaluation Description](evidence/07_Model_Evaluation/EVD-007_Description.md)
- [Confusion Matrix](evidence/07_Model_Evaluation/confusion_matrix.png)
- [Metrics JSON](evidence/07_Model_Evaluation/metrics.json)
- [Classification Report](evidence/07_Model_Evaluation/classification_report.txt)
- [Prediction Results](evidence/07_Model_Evaluation/predictions.csv)

**Limitation:** The relationship between the original Colab training split and this evaluation split still requires verification. Clinical validation has not been performed.
