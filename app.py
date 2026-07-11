import streamlit as st
from PIL import Image
from utils.face_mesh import detect_face_mesh

st.set_page_config(
    page_title="GLOW GUIDE AI",
    page_icon="💄"
)

st.title("💄 GLOW GUIDE")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    result = detect_face_mesh(image)

    processed_image = result["image"]
    landmarks = result["landmarks"]

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    st.subheader("Face Detection Result")
    st.image(
        processed_image,
        channels="BGR",
        use_container_width=True
    )

