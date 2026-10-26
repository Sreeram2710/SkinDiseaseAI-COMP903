# EVD-002 — Dataset Download Verification

**Project:** SkinDiseaseAI — COMP903
**Date:** 22 October 2026
**Status:** PASS — Download and ZIP listing verified

## Objective
Download and verify the Kaggle Skin Diseases Image Dataset
selected for the COMP903 research project.

## Dataset Information
- Source: Kaggle
- Dataset ID: ismailpromus/skin-diseases-image-dataset
- Downloaded archive: skin-diseases-image-dataset.zip
- File size: 5.19 GB
- Expected images: 27,153
- Expected categories: 10

## Procedure
1. Authenticated using Kaggle CLI.
2. Downloaded the dataset to the data folder.
3. Verified the ZIP filename and file size.
4. Checked that the ZIP archive listing was readable.
5. Recorded the terminal output as evidence.

## Observed Results
- Download reached 100%.
- Archive exists in the expected location.
- Archive size is approximately 5.19 GB.
- ZIP listing check returned PASS.

## Limitations
The ZIP listing check does not verify every compressed
image or confirm the actual number of usable images.

## Next Steps
1. Extract the downloaded dataset.
2. Count images in each disease category.
3. Identify corrupted and duplicate images.
4. Verify melanoma and eczema class labels.

## Supporting Evidence
EVD-002_Dataset_Download_Verification.png