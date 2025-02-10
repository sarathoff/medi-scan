import streamlit as st
import tempfile
import os
import requests
from PIL import Image
import io
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Google API
GOOGLE_API_KEY = "AIzaSyDVBniPYoMEGOE360X89Pd3-GS5_tkSDrQ"
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_prescription(image_path, lang_code):
    """Analyze the prescription image using Google's Generative API."""
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    image_file = genai.upload_file(path=image_path)
    response = model.generate_content(
        [
            f"Extract and provide details about the medicines mentioned in this prescription in {lang_code}. Include their purpose, dosage information, and any important warnings.",
            image_file
        ]
    )
    return response.text

def save_uploaded_image(uploaded_file):
    """Save uploaded image to a temporary file and return the path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Medicine Info Extractor", layout="centered")
st.title("📄 Medicine Info Extractor")
st.write("Upload an image of a prescription to get detailed medicine information.")

# Simplified language selection
language_options = {
    "English": "en",
    "தமிழ் (Tamil)": "ta",
    "हिंदी (Hindi)": "hi",
    "বাংলা (Bengali)": "bn",
    "मराठी (Marathi)": "mr",
    "ગુજરાતી (Gujarati)": "gu",
    "ಕನ್ನಡ (Kannada)": "kn",
    "తెలుగు (Telugu)": "te",
    "മലയാളം (Malayalam)": "ml",
    "ਪੰਜਾਬੀ (Punjabi)": "pa"
}
lang_name = st.selectbox("Choose your language", list(language_options.keys()))
lang_code = language_options[lang_name]

# Upload or take a picture
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
captured_image = st.camera_input("Take a picture")

image_path = None
if uploaded_file:
    image_path = save_uploaded_image(uploaded_file)
elif captured_image:
    image_path = save_uploaded_image(io.BytesIO(captured_image.getvalue()))

if image_path:
    st.image(image_path, caption="Uploaded Image", use_column_width=True)
    if st.button("Get Medicine Details"):
        with st.spinner("Fetching medicine information..."):
            medicine_info = analyze_prescription(image_path, lang_code)
        st.subheader("Medicine Details")
        st.write(medicine_info)
