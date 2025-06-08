# 🧪 MF Fibrosis Grading Portal

This is a **Streamlit-based web portal** for automated **grading of myelofibrosis (MF)** from **silver-stained reticulin images**. It uses basic image processing (OpenCV + NumPy) to segment reticulin fibers and assign an MF grade (0–3) based on fiber density.

---

## 🚀 Features

- 📤 Upload **multiple** silver-stained histology images (TIFF, PNG, JPG).
- 🧠 Automatically compute:
  - Reticulin fiber area (%)
  - MF Grade (MF-0 to MF-3)
  - MF Level (continuous 0–3 scale)
- 🖼 Annotates these metrics on each image
- 📦 One-click download of all results as a ZIP

---

## 📊 MF Grading Criteria

| Reticulin Area (%) | MF Grade | MF Level |
|--------------------|----------|----------|
| ≤ 5%               | MF-0     | 0–0.5    |
| 5–15%              | MF-1     | 0.5–1.5  |
| 15–30%             | MF-2     | 1.5–2.5  |
| > 30%              | MF-3     | 2.5–3.0  |

---

## 🧩 Tech Stack

- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [Pillow (PIL)](https://python-pillow.org/)
- NumPy

---

## 📦 Installation

### 🔧 Local Setup

```bash
git clone https://github.com/shukla115/fibrosis.git
cd fibrosis

# Create virtual environment (optional but recommended)
python -m venv .venv
.venv\\Scripts\\activate  # on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run aryan2.py
