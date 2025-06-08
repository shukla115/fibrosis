# Streamlit app for MF grading from silver-stained reticulin images
import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import tempfile
import zipfile
import os

st.set_page_config(page_title="MF Fibrosis Grading Portal", layout="centered")
st.title("🩺 MF Grading from Reticulin (Silver-Stained) Images")

uploaded_files = st.file_uploader("Upload one or more silver-stained images", type=["tif", "tiff", "png", "jpg"], accept_multiple_files=True)

results = []

if uploaded_files:
    output_dir = tempfile.mkdtemp()

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        # Convert to grayscale and enhance
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        equalized = cv2.equalizeHist(gray)

        # Thresholding to detect reticulin fibers
        _, binary_reticulin = cv2.threshold(equalized, 50, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary_reticulin, cv2.MORPH_OPEN, kernel)

        # Calculate reticulin metrics
        fiber_area = np.sum(cleaned == 255)
        total_area = cleaned.size
        fiber_percent = (fiber_area / total_area) * 100

        # Assign MF grade and continuous level
        if fiber_percent <= 5:
            mf_grade = "MF-0"
            mf_level = round(fiber_percent / 10, 2)
        elif fiber_percent <= 15:
            mf_grade = "MF-1"
            mf_level = round(0.5 + (fiber_percent - 5) / 10, 2)
        elif fiber_percent <= 30:
            mf_grade = "MF-2"
            mf_level = round(1.5 + (fiber_percent - 15) / 15, 2)
        else:
            mf_grade = "MF-3"
            mf_level = round(min(2.5 + (fiber_percent - 30) / 30, 3.0), 2)

        # Annotate results onto the image
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        font = ImageFont.truetype("arial.ttf", 24) if hasattr(ImageFont, 'truetype') else None
        annotation_text = f"Reticulin Area: {fiber_percent:.2f}%\nMF Grade: {mf_grade}\nMF Level: {mf_level}"
        draw.text((10, 10), annotation_text, fill=(255, 0, 0), font=font)

        output_path = os.path.join(output_dir, f"annotated_{uploaded_file.name}.png")
        annotated.save(output_path)

        results.append({
            "filename": uploaded_file.name,
            "fiber_percent": fiber_percent,
            "mf_grade": mf_grade,
            "mf_level": mf_level,
            "image_path": output_path
        })

    st.subheader("📊 Batch Results")
    for result in results:
        st.markdown(f"**{result['filename']}**")
        st.markdown(f"- Reticulin Area: {result['fiber_percent']:.2f}%")
        st.markdown(f"- MF Grade: {result['mf_grade']}")
        st.markdown(f"- MF Level (0–3): {result['mf_level']}")
        st.image(result['image_path'], caption="Annotated Result", use_column_width=True)

    # Create a zip of all annotated results
    zip_path = os.path.join(output_dir, "mf_batch_results.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for result in results:
            zipf.write(result['image_path'], arcname=os.path.basename(result['image_path']))

    with open(zip_path, "rb") as f:
        st.download_button("Download All Annotated Images as ZIP", f, file_name="mf_batch_results.zip")
