import streamlit as st
import requests
from PIL import Image

st.set_page_config(
    page_title="OCR Text Extractor",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 2rem;
}

.title {
    text-align:center;
    font-size:48px;
    font-weight:700;
    color:#4F46E5;
}

.subtitle {
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:30px;
}

.result-box {
    background-color:#f5f5f5;
    padding:20px;
    border-radius:12px;
    border:1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">📄 AI OCR Extractor</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Upload an image and extract text instantly</p>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    col1, col2 = st.columns(2)

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

    with col2:

        if st.button("🚀 Extract Text", use_container_width=True):

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

                st.success("Text Extracted Successfully")

                st.markdown(
                    f"""
                    <div class="result-box">
                    <pre>{text}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.download_button(
                    "📥 Download Text",
                    text,
                    file_name="ocr_output.txt"
                )

            except:
                st.error("Could not extract text.")
