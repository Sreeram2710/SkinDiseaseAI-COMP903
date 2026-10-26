
# EVD-006 — SkinDiseaseAI Application Testing

**Project:** SkinDiseaseAI — COMP903 Research Project  
**Testing date:** 22 October 2026  
**Application:** Streamlit Research Platform v0.1.0  
**Environment:** Windows 11, Python 3.11, Microsoft Edge  
**Local application:** http://localhost:8501

## 1. Objective

Verify the initial functionality and navigation of the SkinDiseaseAI research application before integrating trained deep learning models.

## 2. Test Results

| Test ID | Test Description | Result |
|---|---|---|
| AT-001 | Overview dashboard loads and displays dataset statistics | PASS |
| AT-002 | JPG image uploads and displays a preview | PASS |
| AT-003 | Uploaded image metadata is displayed | PASS |
| AT-004 | EfficientNetB0 and ResNet50 comparison interface loads | PASS |
| AT-005 | Evaluation metrics are displayed as pending | PASS |
| AT-006 | Research Evidence and About Project screenshots captured | EVIDENCE SAVED — content not independently verified |

## 3. Screenshot Evidence

### EVD-006-A: Overview Dashboard

![Overview Dashboard](EVD-006_Overview_Dashboard.png)

The dashboard presents dataset quality statistics, including 27,153 images, zero detected corrupt files and 588 exact duplicate groups.

### EVD-006-B: Image Upload Test

![Image Upload Test](EVD-006_Image_Upload_Test.png)

An uploaded JPEG image was successfully previewed. Its filename, dimensions, format and colour mode were displayed. Disease classification was not performed.

### EVD-006-C: Model Comparison

![Model Comparison](EVD-006_Model_Comparison.png)

The application displays EfficientNetB0 and ResNet50 as proposed transfer-learning architectures. Accuracy, precision, recall, F1-score, confusion matrix and inference time are marked pending.

### EVD-006-D: Research Evidence

![Research Evidence](EVD-006_Research_Evidence.png)

Screenshot captured to document the Research Evidence interface.

### EVD-006-E: About Project

![About Project](EVD-006_About_Project.png)

Screenshot captured to document the project information interface.

## 4. Current Limitations

- Trained CNN models have not been integrated.
- Skin disease predictions are unavailable.
- Grad-CAM visualisations are unavailable.
- Model evaluation metrics have not been measured.
- Clinical validation has not been performed.
- Testing has so far focused on selected interface functionality rather than complete end-to-end testing.

## 5. Conclusion

The initial Streamlit research application is operational, and selected interface tests passed. Five screenshots were saved as evidence. Further work will focus on duplicate-aware data preprocessing, model training and comparative evaluation.

**Research safety statement:** SkinDiseaseAI is an experimental research prototype and is not intended for clinical diagnosis or treatment.

## EVD-006 — EfficientNetB0 Model Inference Test

**Test date:** 26 October 2026

**Objective:** Verify that the SkinDiseaseAI application can load a trained EfficientNetB0 model and perform binary skin-image classification.

### Test Procedure
1. Launched the Streamlit application.
2. Opened the Image Analysis page.
3. Uploaded the research dataset image `0_0.jpg`.
4. Clicked Analyse Image.
5. Observed the prediction output.

### Observed Results
- Model: EfficientNetB0
- Input size: 224 × 224 RGB
- Melanoma class score: 0.1%
- Other dataset classes score: 99.9%
- Model inference: PASS
- Image preview: PASS

### Research Limitations
The scores are experimental model outputs, not calibrated clinical probabilities. This test confirms that inference executes successfully but does not establish clinical accuracy or diagnostic safety.

### Screenshot Evidence
![EfficientNetB0 Prediction Test](EVD-006_EfficientNetB0_Prediction_Test.png)
