import streamlit as st
from PIL import Image

from core.face_mesh import detect_face_mesh
from core.colour_analysis import analyze_skin
from core.face_shape import analyze_face_shape
from recommendations.recommendation import get_recommendations


# --------------------------------------------------------
# Page Config
# --------------------------------------------------------

st.set_page_config(
    page_title="GlowGuide AI",
    page_icon="✨",
    layout="wide"
)


# --------------------------------------------------------
# Custom CSS
# --------------------------------------------------------

st.markdown("""
<style>

/* -----------------------------
   Hide Streamlit
------------------------------*/

#MainMenu{
    visibility:hidden;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* -----------------------------
   Background
------------------------------*/

.stApp{

    background:#F8F7F4;

}

.block-container{

    max-width:1200px;

    padding-top:2rem;

    padding-bottom:4rem;

}

/* -----------------------------
   Typography
------------------------------*/

html,
body,
[class*="css"]{

    font-family:Inter,sans-serif;

    color:#3A3A3A;

}

h1,h2,h3,h4{

    color:#2F2F2F !important;

    font-weight:700;

}

p{

    color:#666666 !important;

    line-height:1.8;

}

/* -----------------------------
Hero
------------------------------*/

.hero{

    text-align:center;

    margin-top:20px;

    margin-bottom:60px;

}

.hero-chip{

    display:inline-block;

    padding:8px 20px;

    background:#F0E8E5;

    color:#9A8277;

    border-radius:30px;

    font-size:14px;

    font-weight:600;

    letter-spacing:.5px;

    margin-bottom:25px;

}

.hero-title{

    font-size:72px;

    font-weight:700;

    color:#2F2F2F;

    margin-bottom:15px;

    letter-spacing:-2px;

}

.hero-sub{

    max-width:760px;

    margin:auto;

    font-size:22px;

    color:#666666;

}

/* -----------------------------
Section
------------------------------*/

.section-title{

    font-size:38px;

    font-weight:700;

    color:#2F2F2F;

    margin-top:60px;

    margin-bottom:25px;

}

/* -----------------------------
Cards
------------------------------*/

.card{

    background:white;

    padding:28px;

    border-radius:22px;

    border:1px solid #E8E5E2;

    box-shadow:0 8px 30px rgba(0,0,0,.05);

}

/* -----------------------------
Analysis Cards
------------------------------*/

.analysis-card{

    background:white;

    border-radius:18px;

    border:1px solid #E8E5E2;

    padding:24px;

    height:150px;

    display:flex;

    flex-direction:column;

    justify-content:center;

    align-items:center;

    box-shadow:0 8px 22px rgba(0,0,0,.05);

}

.analysis-label{

    color:#888888;

    font-size:15px;

    margin-bottom:12px;

}

.analysis-value{

    color:#2F2F2F;

    font-size:30px;

    font-weight:700;

}

/* -----------------------------
Recommendation Cards
------------------------------*/

.product-card{

    background:white;

    border-radius:20px;

    border:1px solid #E8E5E2;

    padding:24px;

    box-shadow:0 8px 22px rgba(0,0,0,.05);

    margin-bottom:18px;

}

.product-type{

    font-size:13px;

    letter-spacing:1px;

    text-transform:uppercase;

    color:#B08E84;

}

.product-name{

    font-size:24px;

    color:#2F2F2F;

    font-weight:700;

    margin-top:8px;

    margin-bottom:8px;

}

.product-desc{

    color:#6D6D6D;

    font-size:15px;

}

/* -----------------------------
Buttons
------------------------------*/

.stButton>button{

    background:#DCCBC5;

    color:#2F2F2F;

    border:none;

    border-radius:12px;

    height:48px;

    font-weight:600;

}

.stButton>button:hover{

    background:#D2BDB7;

}

/* -----------------------------
Footer
------------------------------*/

.footer{

    text-align:center;

    color:#8A8A8A;

    margin-top:80px;

    line-height:2;

}

</style>
""",unsafe_allow_html=True)


# --------------------------------------------------------
# Hero Section
# --------------------------------------------------------

st.markdown("""

<div class="hero">

<div class="hero-chip">

AI Powered Beauty Analysis

</div>

<div class="hero-title">

GlowGuide AI

</div>

<div class="hero-sub">

Upload one selfie to discover your skin tone,
undertone, face shape and receive AI-powered
makeup recommendations curated specifically
for you.

</div>

</div>

""",unsafe_allow_html=True)

# ==========================================================
# Upload Section
# ==========================================================

st.markdown(
    '<div class="section-title">Upload Your Selfie</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

<h3 style="margin-top:0;">📸 Upload Image</h3>

<p>
Upload a clear front-facing selfie in good lighting.
For the best results, avoid filters and ensure your
entire face is visible.
</p>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# ==========================================================
# Image Processing
# ==========================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    with st.spinner("Analyzing your face..."):

        result = detect_face_mesh(image)

        analysis = None
        face_shape = None
        recommendations = None

        if result["landmarks"] is not None:

            face_shape = analyze_face_shape(
                result["image"],
                result["landmarks"]
            )

        if result["skin"] is not None:

            analysis = analyze_skin(
                result["skin"]
            )

            if analysis is not None:

                recommendations = get_recommendations(
                    analysis["tone"],
                    analysis["undertone"]
                )

    st.success("✨ Analysis completed successfully!")

    # ==========================================================
    # Analysis Results
    # ==========================================================

    st.markdown(
        '<div class="section-title">Analysis Results</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="large")
    # -----------------------------
    # Original Image
    # -----------------------------

    with col1:

        st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

        st.markdown("### Original Image")

        st.image(
            image,
            use_container_width=True
        )

        st.markdown("""
</div>
""", unsafe_allow_html=True)

    # -----------------------------
    # Face Mesh
    # -----------------------------

    with col2:

        st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

        st.markdown("### Face Mesh")

        st.image(
            result["image"],
            channels="BGR",
            use_container_width=True
        )

        st.markdown("""
</div>
""", unsafe_allow_html=True)
        
    # -----------------------------
    # Skin Extraction
    # -----------------------------

    with col3:

        st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

        st.markdown("### Skin Extraction")

        if result["skin"] is not None:

            st.image(
                result["skin"],
                channels="BGR",
                use_container_width=True
            )

        st.markdown("""
</div>
""", unsafe_allow_html=True)

    if result["mask"] is not None:

        with st.expander("View Skin Mask"):

            st.image(
                result["mask"],
                use_container_width=True
            )

    # ==========================================================
    # Analysis Summary
    # ==========================================================

    if analysis is not None:

        st.markdown(
            '<div class="section-title">Analysis Summary</div>',
            unsafe_allow_html=True
        )

        face_shape_name = "Unknown"

        if face_shape is not None:

            face_shape_name = face_shape["shape"]

        cards = [

            ("Skin Tone", analysis["tone"]),

            ("Undertone", analysis["undertone"]),

            ("Face Shape", face_shape_name),

            ("ITA Score", analysis["ita"])

        ]

        c1, c2, c3, c4 = st.columns(4)

        for col, (title, value) in zip(
            [c1, c2, c3, c4],
            cards
        ):

            with col:

                st.markdown(
f"""
<div class="analysis-card">

<div class="analysis-label">
{title}
</div>

<div class="analysis-value">
{value}
</div>

</div>
""",
unsafe_allow_html=True
                )

        # --------------------------------------------------------
        # Detailed Analysis
        # --------------------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        left, right = st.columns(2, gap="large")

        with left:

            with st.container(border=True):

                st.subheader("Skin Statistics")

                st.write(
                    f"**Average RGB:** {analysis['rgb']}"
                )

                st.write(
                    f"**LAB Values:** {analysis['lab']}"
                )

                st.write(
                    f"**ITA Score:** {analysis['ita']}"
                )

        with right:

            if face_shape is not None:

                with st.container(border=True):

                    st.subheader("Face Measurements")

                    for key, value in face_shape["measurements"].items():

                        st.write(
                            f"**{key}:** {value}"
                        )

        # ==========================================================
        # Personalized Recommendations
        # ==========================================================

        st.markdown(
            '<div class="section-title">Personalized Recommendations</div>',
            unsafe_allow_html=True
        )

        recommendation_items = [

            (
                "Foundation",
                recommendations["Foundation"],
                "Recommended foundation shade for your skin tone."
            ),

            (
                "Lipstick",
                recommendations["Lipstick"],
                "Lip colour that complements your undertone."
            ),

            (
                "Blush",
                recommendations["Blush"],
                "Blush shade suitable for your complexion."
            ),

            (
                "Eyeshadow",
                recommendations["Eyeshadow"],
                "Eyeshadow shades that suit your overall look."
            )

        ]

        left, right = st.columns(2, gap="large")

        for index, item in enumerate(recommendation_items):

            category, product, description = item

            column = left if index % 2 == 0 else right

            with column:

                st.markdown(
f"""
<div class="product-card">

<div class="product-type">
{category}
</div>

<div class="product-name">
{product}
</div>

<div class="product-desc">
{description}
</div>

</div>
""",
unsafe_allow_html=True
                )

        # --------------------------------------------------------
        # Future Features
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-title">Future Features</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:

            st.button(
                "✨ Virtual Makeup Try-On",
                disabled=True,
                use_container_width=True
            )

        with c2:

            st.button(
                "📄 Download Beauty Report",
                disabled=True,
                use_container_width=True
            )

# ==========================================================
# Footer
# ==========================================================

st.divider()

st.markdown("""
<div class="footer">

<h3 style="color:#2F2F2F;margin-bottom:10px;">
GlowGuide AI
</h3>

<p>
AI-Powered Personalized Beauty Analysis
</p>

<p style="font-size:15px;">
Built using Python • OpenCV • MediaPipe • Streamlit
</p>

<p style="margin-top:20px;">
Made with ❤️ by
<b style="color:#2F2F2F;">Aarushi Singh</b>
</p>

</div>
""", unsafe_allow_html=True)