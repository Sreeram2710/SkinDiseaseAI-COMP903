
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "efficientnetb0_melanoma_best.keras"

IMAGE_SIZE = (224, 224)


@st.cache_resource(show_spinner="Loading melanoma research model...")
def load_melanoma_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_PATH}"
        )

    model = tf.keras.models.load_model(
        str(MODEL_PATH),
        compile=False,
    )
    return model


def predict_melanoma(image: Image.Image):
    model = load_melanoma_model()

    # Convert to RGB and resize.
    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    # EfficientNetB0 includes preprocessing internally.
    # Retain the raw 0–255 pixel scale.
    array = np.asarray(image, dtype=np.float32)
    array = np.expand_dims(array, axis=0)

    prediction = model.predict(array, verbose=0)

    probability = float(prediction.reshape(-1)[0])

    if not np.isfinite(probability):
        raise ValueError("Model returned a non-finite prediction.")

    if not 0.0 <= probability <= 1.0:
        raise ValueError("Model returned a value outside 0–1.")

    return {
        "melanoma_score": probability,
        "other_classes_score": 1.0 - probability,
        "model": "EfficientNetB0",
        "input_size": IMAGE_SIZE,
    }
