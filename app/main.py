"""SkinDiseaseAI COMP903 research prototype Streamlit application."""
from pathlib import Path
import json

import streamlit as st
from PIL import Image, UnidentifiedImageError

from model_inference import predict_melanoma

ROOT_DIR = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT_DIR / 'evidence'
SUMMARY_PATH = EVIDENCE_DIR / '04_Image_Quality' / 'EVD-004_Summary.json'
MODEL_PATH = ROOT_DIR / 'models' / 'efficientnetb0_melanoma_best.keras'

st.set_page_config(
    page_title='SkinDiseaseAI | Research Platform',
    page_icon='🔬',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.markdown('''
<style>
:root { --navy:#10263F; --teal:#087F8C; --muted:#64748B; --background:#F5F8FC; }
.stApp { background:var(--background); }
h1,h2,h3 { color:var(--navy); letter-spacing:-0.5px; }
[data-testid="stSidebar"] { background:#10263F; }
[data-testid="stSidebar"] * { color:#F8FAFC; }
[data-testid="stMetric"] {
    background:white; border:1px solid #E2E8F0;
    padding:18px; border-radius:14px;
}
[data-testid="stMetricValue"] { color:#087F8C; }
.hero {
    padding:30px; border-radius:18px;
    background:linear-gradient(115deg,#10263F,#14576B);
    color:white; margin-bottom:22px;
}
.hero h1 { color:white; margin:0; }
.hero p { color:#D8E9F0; margin-top:10px; }
.info-card {
    background:white; border:1px solid #E2E8F0;
    padding:22px; border-radius:14px; margin-bottom:16px;
}
.info-card h3 { margin-top:0; }
.eyebrow {
    font-size:12px; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; color:#087F8C;
}
.footer-note { color:#64748B; font-size:13px; margin-top:35px; }
</style>
''', unsafe_allow_html=True)


def load_summary():
    if SUMMARY_PATH.is_file():
        try:
            with SUMMARY_PATH.open('r', encoding='utf-8') as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError):
            st.warning('Research summary could not be loaded.')
    return {}


summary = load_summary()


def get_stat(key):
    value = summary.get(key)
    return f'{value:,}' if isinstance(value, int) else 'Not available'


with st.sidebar:
    st.title('🔬 SkinDiseaseAI')
    st.caption('COMP903 • Research Platform')
    st.divider()
    page = st.radio(
        'Navigation',
        ['Overview', 'Image Analysis', 'Model Comparison',
         'Research Evidence', 'About Project'],
        label_visibility='collapsed',
    )
    st.divider()
    st.caption('RESEARCH STATUS')
    if MODEL_PATH.is_file():
        st.success('EfficientNetB0 melanoma model available')
    else:
        st.info('Melanoma model file not found')
    st.caption('ResNet50 eczema training incomplete')
    st.caption('Research prototype • Not for clinical diagnosis')

if page == 'Overview':
    st.markdown('''
    <div class="hero">
        <div class="eyebrow" style="color:#8DE0DB;">AI-ASSISTED DERMATOLOGY RESEARCH</div>
        <h1>SkinDiseaseAI</h1>
        <p>An explainable deep-learning research platform for skin image classification.</p>
    </div>
    ''', unsafe_allow_html=True)

    st.subheader('Dataset Research Overview')
    a, b, c, d = st.columns(4)
    with a:
        st.metric('Images Analysed', get_stat('total_files'))
    with b:
        st.metric('Readable Images', get_stat('readable_files'))
    with c:
        st.metric('Corrupted Images', get_stat('corrupt_files'))
    with d:
        st.metric('Duplicate Groups', get_stat('duplicate_groups'))

    left, right = st.columns([1.4, 1])
    with left:
        st.markdown('''
        <div class="info-card"><h3>Research Objective</h3>
        <p>Investigate transfer learning for skin condition images and examine
        model performance, reproducibility and explainability.</p>
        <p>Architectures: EfficientNetB0 and ResNet50.</p></div>
        ''', unsafe_allow_html=True)
    with right:
        st.markdown('''
        <div class="info-card"><h3>Development Progress</h3>
        <p>✓ Dataset acquired</p>
        <p>✓ Image integrity and duplicate analysis</p>
        <p>✓ Duplicate-aware dataset splits prepared</p>
        <p>✓ EfficientNetB0 melanoma model saved locally</p>
        <p>○ ResNet50 eczema model pending</p>
        <p>○ Independent clinical validation not performed</p></div>
        ''', unsafe_allow_html=True)
    st.info('Dataset-quality findings and model outputs are research observations, not clinical evidence.')

elif page == 'Image Analysis':
    st.title('Skin Image Analysis')
    st.caption('AI-assisted image classification | EfficientNetB0 melanoma research model')
    st.warning(
        'Research prototype only. Do not use this application to diagnose, '
        'exclude, or manage melanoma or any other medical condition.'
    )
    uploaded_file = st.file_uploader(
        'Upload a skin image',
        type=['jpg', 'jpeg', 'png'],
        help='Use only images you are permitted to analyse, without identifying details.',
    )

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            image.load()
            left, right = st.columns([1, 1])
            with left:
                st.image(image, caption='Uploaded image preview', use_container_width=True)
            with right:
                st.subheader('Image Information')
                st.write(f'**Filename:** {uploaded_file.name}')
                st.write(f'**Dimensions:** {image.width} × {image.height}')
                st.write(f'**Format:** {image.format}')
                st.write(f'**Colour mode:** {image.mode}')
                st.info('Grad-CAM: Not implemented yet.')

            st.divider()
            st.subheader('AI Research Classification')
            if not MODEL_PATH.is_file():
                st.error('The trained melanoma model is missing from the models folder.')
            elif st.button('Analyse Image', type='primary'):
                try:
                    with st.spinner('Running EfficientNetB0 inference...'):
                        result = predict_melanoma(image)
                    m, o = st.columns(2)
                    with m:
                        st.metric('Melanoma class score', f"{result['melanoma_score']:.1%}")
                    with o:
                        st.metric('Other dataset classes score', f"{result['other_classes_score']:.1%}")
                    st.caption(
                        'Binary model: melanoma versus all other dataset classes. '
                        'Input: 224 × 224 RGB. These scores are not calibrated '
                        'clinical probabilities or a diagnostic risk estimate.'
                    )
                    st.warning(
                        'A low melanoma score does not rule out melanoma. '
                        'This model has not been clinically validated.'
                    )
                except Exception as error:
                    st.error(f'Model inference could not be completed: {error}')
        except (UnidentifiedImageError, OSError, ValueError):
            st.error('The uploaded file could not be decoded as an image.')

    st.caption(
        'Upload permitted, non-identifying research images only. '
        'This prototype is not a medical service.'
    )

elif page == 'Model Comparison':
    st.title('Model Comparison')
    st.caption('Research experiments — outcomes must be validated on the held-out test set')
    a, b = st.columns(2)
    with a:
        st.subheader('EfficientNetB0')
        st.write('Task: Melanoma vs all other dataset classes')
        st.write('Training: Completed; saved model available locally'
                 if MODEL_PATH.is_file() else 'Training artefact missing')
        st.write('Held-out test evaluation: Pending')
    with b:
        st.subheader('ResNet50')
        st.write('Task: Eczema vs all other dataset classes')
        st.write('Training: Interrupted; checkpoint not recovered')
        st.write('Held-out test evaluation: Pending')
    st.divider()
    st.subheader('Evaluation Framework')
    st.dataframe(
        {'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-score',
                    'ROC-AUC', 'Confusion matrix', 'Inference time'],
         'EfficientNetB0': ['Pending'] * 7,
         'ResNet50': ['Pending'] * 7},
        hide_index=True, use_container_width=True,
    )
    st.info(
        'These models address different binary tasks. Comparing their scores '
        'directly is not a controlled architecture comparison.'
    )

elif page == 'Research Evidence':
    st.title('Research Evidence')
    st.caption('Documented experiment files, dataset analyses, and application testing')
    evidence_items = [
        ('EVD-002', 'Dataset Acquisition', '02_Dataset_Download'),
        ('EVD-003', 'Dataset Class Analysis', '03_Dataset_Analysis'),
        ('EVD-004', 'Image Quality and Duplicates', '04_Image_Quality'),
        ('EVD-005', 'Duplicate Resolution and Dataset Splitting', '05_Duplicate_Resolution'),
        ('EVD-006', 'Application Testing', '06_Application_Testing'),
    ]
    for evidence_id, title, folder in evidence_items:
        folder_path = EVIDENCE_DIR / folder
        with st.expander(f'{evidence_id} — {title}'):
            st.write(f'Evidence folder: `evidence/{folder}`')
            if folder_path.is_dir():
                files = sorted(p.name for p in folder_path.iterdir() if p.is_file())
                if files:
                    for filename in files:
                        st.write(f'• {filename}')
                else:
                    st.write('No evidence files recorded in this folder yet.')
            else:
                st.write('Evidence folder not yet available.')

elif page == 'About Project':
    st.title('About SkinDiseaseAI')
    st.markdown('''
### Project Purpose
SkinDiseaseAI is a COMP903 postgraduate research prototype examining
skin-image classification using deep learning.

### Current and Planned Capabilities
- Image upload and preview
- EfficientNetB0 melanoma-versus-other dataset class scoring
- ResNet50 eczema model (training not completed)
- Held-out test evaluation (pending)
- Grad-CAM explainability (planned)
- Research evidence and reproducibility documentation

### Important Limitations
This system is not clinically validated and must not be used for diagnosis,
treatment, screening, or any other medical decision. Dataset label quality,
near duplicates, and unknown patient-level overlap remain research limitations.
''')

st.markdown('''
<div class="footer-note">
SkinDiseaseAI • COMP903 Research Project • Experimental software • Not for clinical use
</div>
''', unsafe_allow_html=True)
