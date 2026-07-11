import streamlit as st
from PIL import Image

from core.face_mesh import detect_face_mesh
from core.colour_analysis import analyze_skin
from recommendations.recommendation import get_recommendations
from core.face_shape import analyze_face_shape

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="GlowGuide AI",
    page_icon="💄",
    layout="wide"
)

st.title("💄 GlowGuide AI")
st.markdown(
    "### AI-Powered Makeup Analysis & Recommendation System"
)

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a selfie",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------
# Process Image
# -----------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    with st.spinner("Analyzing your face..."):

        result = detect_face_mesh(image)
        face_shape = None

    if result["landmarks"] is not None:

        face_shape = analyze_face_shape(
        result["image"],
        result["landmarks"]
        )
        analysis = None
        recommendations = None

        if result["skin"] is not None:

            analysis = analyze_skin(result["skin"])

            if analysis is not None:

                recommendations = get_recommendations(
                    analysis["tone"],
                    analysis["undertone"]
                )

    # -------------------------------------------------------
    # Display Images
    # -------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Original Image")
        st.image(
            image,
            use_container_width=True
        )

    with col2:
        st.subheader("Face Mesh")
        st.image(
            result["image"],
            channels="BGR",
            use_container_width=True
        )

    with col3:
        st.subheader("Skin Extraction")

        if result["skin"] is not None:

            st.image(
                result["skin"],
                channels="BGR",
                use_container_width=True
            )

        if result["mask"] is not None:

            st.subheader("Skin Mask")

            st.image(
                result["mask"],
                use_container_width=True
            )

    # -------------------------------------------------------
    # Analysis
    # -------------------------------------------------------

    if analysis is not None:

        st.divider()

        st.header("📊 Skin Analysis")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Skin Tone",
                analysis["tone"]
            )

            st.metric(
                "Undertone",
                analysis["undertone"]
            )

            if face_shape is not None:
                st.metric(
                "Face Shape",
                face_shape["shape"]
                )

        with c2:

            st.write("Average RGB")

            st.code(str(analysis["rgb"]))

            st.write("LAB Values")

            st.code(str(analysis["lab"]))

            if face_shape is not None:

                with st.expander("📐 Face Measurements"):

                    st.json(
                    face_shape["measurements"]
                    )

        st.divider()

        st.header("💄 Makeup Recommendations")

        r1, r2 = st.columns(2)

        with r1:

            st.success(
                f"Foundation: {recommendations['Foundation']}"
            )

            st.success(
                f"Lipstick: {recommendations['Lipstick']}"
            )

        with r2:

            st.success(
                f"Blush: {recommendations['Blush']}"
            )

            st.success(
                f"Eyeshadow: {recommendations['Eyeshadow']}"
            )

    else:

        st.error("No face detected.")