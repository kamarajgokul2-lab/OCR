import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="OCR Extractor", layout="wide")

st.title("📄 OCR Text Extractor")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image)

    if st.button("Extract Text"):

        api_key = st.secrets["OCR_API_KEY"]

        payload = {
            "apikey": api_key,
            "language": "eng"
        }

        files = {
            "file": uploaded_file.getvalue()
        }

        response = requests.post(
            "https://api.ocr.space/parse/image",
            files=files,
            data=payload
        )

        result = response.json()

        try:
            text = result["ParsedResults"][0]["ParsedText"]
            st.text_area("Extracted Text", text, height=300)

        except:
            st.error("OCR failed")
