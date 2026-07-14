import streamlit as st
from PIL import Image

from core.face_mesh import detect_face_mesh
from core.colour_analysis import analyze_skin
from core.face_shape import analyze_face_shape
from recommendations.recommendation import get_recommendations


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="GlowGuide AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* ---------------------------------------------------- */
/* Hide Streamlit */
/* ---------------------------------------------------- */

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

/* ---------------------------------------------------- */
/* Background */
/* ---------------------------------------------------- */

.stApp{

background:#F8F7F4;

}

.block-container{

max-width:1250px;

padding-top:2rem;

padding-bottom:3rem;

}

/* ---------------------------------------------------- */
/* Typography */
/* ---------------------------------------------------- */

html,
body,
[class*="css"]{

font-family:"Inter",sans-serif;

color:#353535;

}

h1,h2,h3,h4{

color:#353535 !important;

}

p{

color:#6B7280 !important;

}

/* ---------------------------------------------------- */
/* Hero */
/* ---------------------------------------------------- */

.hero{

background:#FDF2F4;

border:1px solid #F0D9DF;

border-radius:30px;

padding:70px;

text-align:center;

margin-bottom:60px;

}

.hero-badge{

display:inline-block;

padding:10px 22px;

background:white;

border-radius:25px;

font-size:14px;

font-weight:600;

letter-spacing:2px;

color:#C77C93;

margin-bottom:25px;

}

.hero-title{

font-size:64px;

font-weight:700;

margin-bottom:18px;

color:#353535;

}

.hero-sub{

font-size:21px;

max-width:720px;

margin:auto;

line-height:1.8;

color:#6B7280;

}

/* ---------------------------------------------------- */
/* Section Heading */
/* ---------------------------------------------------- */

.section-title{

font-size:34px;

font-weight:700;

margin-top:50px;

margin-bottom:25px;

color:#353535;

}

/* --------------------------------------------------
Recommendation Cards
---------------------------------------------------*/

.rec-card{

    background:#FFFFFF;

    border:1px solid #F2D9DF;

    border-radius:24px;

    padding:30px;

    min-height:500px;

    box-shadow:
        0 8px 24px rgba(0,0,0,.05);

    transition:.3s;

}

.rec-card:hover{

    transform:translateY(-6px);

    box-shadow:
        0 18px 36px rgba(0,0,0,.08);

}
            
.rec-badge{

    display:inline-block;

    padding:8px 16px;

    border-radius:999px;

    font-size:13px;

    font-weight:700;

    margin-bottom:22px;

}

.badge-budget{

    background:#FFF7DA;

    color:#A97700;

}

.badge-best{

    background:#FFF1CC;

    color:#B88600;

}

.badge-premium{

    background:#FDF2F4;

    color:#C27C91;

}

.rec-brand{

    font-size:28px;

    font-weight:700;

    color:#353535;

    margin-bottom:6px;

}

.rec-product{

    font-size:17px;

    font-weight:500;

    color:#6B7280;

    line-height:1.6;

    margin-bottom:24px;

}
            
.rec-label{

    font-size:13px;

    font-weight:700;

    letter-spacing:1px;

    text-transform:uppercase;

    color:#9CA3AF;

    margin-top:14px;

}

.rec-value{

    font-size:17px;

    color:#444;

    margin-top:4px;

}

.rec-price{

    font-size:34px;

    font-weight:800;

    color:#D37E9B;

    margin-top:24px;

}

.rec-reason{

    margin-top:22px;

    padding-top:18px;

    border-top:1px solid #F2D9DF;

    color:#666;

    font-size:15px;

    line-height:1.8;

}
            
</style>
""", unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""

<div class="hero">

<div class="hero-badge">

✨ AI POWERED BEAUTY ANALYSIS

</div>

<div class="hero-title">

GlowGuide AI

</div>

<div class="hero-sub">

Discover your skin tone, undertone,
face shape and receive personalized
makeup recommendations curated
specifically for your complexion.

</div>

</div>

""", unsafe_allow_html=True)

# ==========================================================
# Upload Section
# ==========================================================

st.markdown(
    '<div class="section-title">Upload Your Selfie</div>',
    unsafe_allow_html=True
)

st.info(
    "📸 Upload a clear front-facing selfie in natural lighting for the most accurate analysis."
)

uploaded_file = st.file_uploader(
    "Choose an Image",
    type=["jpg", "jpeg", "png"]
)

# ==========================================================
# Image Processing
# ==========================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    left, right = st.columns([1.3, 1])

    with left:

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    with right:

        st.markdown("### Ready to Analyze")

        st.write(
            """
            Your image has been uploaded successfully.

            Click the button below to begin:

            • Face Detection

            • Skin Tone Detection

            • Undertone Detection

            • Face Shape Detection

            • Personalized Makeup Recommendations
            """
        )

        analyze = st.button(
            "✨ Analyze My Face",
            use_container_width=True
        )

    if analyze:

        progress = st.progress(0)

        status = st.empty()

        # ----------------------------------------

        status.write("📸 Detecting face...")

        progress.progress(20)

        result = detect_face_mesh(image)

        analysis = None
        face_shape = None
        recommendations = None

        # ----------------------------------------

        status.write("😊 Detecting face shape...")

        progress.progress(45)

        if result["landmarks"] is not None:

            face_shape = analyze_face_shape(
                result["image"],
                result["landmarks"]
            )

        # ----------------------------------------

        status.write("🎨 Analyzing skin tone...")

        progress.progress(70)

        if result["skin"] is not None:

            analysis = analyze_skin(
                result["skin"]
            )

        # ----------------------------------------

        status.write("💄 Generating recommendations...")

        progress.progress(90)

        if analysis is not None:

            recommendations = get_recommendations(
                analysis["tone"],
                analysis["undertone"]
            )

        progress.progress(100)

        status.empty()

        progress.empty()

        st.success(
            "✨ Analysis completed successfully!"
        )

        # ==========================================================
        # Analysis Results
        # ==========================================================
        st.markdown(
            '<div class="section-title">Analysis Results</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------------
        # Original Image
        # ----------------------------------------------------------

        with col1:

            with st.container(border=True):

                st.subheader("📷 Original Image")

                st.image(
                    image,
                    use_container_width=True
                )

        # ----------------------------------------------------------
        # Face Mesh
        # ----------------------------------------------------------

        with col2:

            with st.container(border=True):

                st.subheader("🧠 Face Mesh")

                st.image(
                    result["image"],
                    channels="BGR",
                    use_container_width=True
                )

        # ----------------------------------------------------------
        # Skin Extraction
        # ----------------------------------------------------------

        with col3:

            with st.container(border=True):

                st.subheader("🎨 Skin Extraction")

                if result["skin"] is not None:

                    st.image(
                        result["skin"],
                        channels="BGR",
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "Skin could not be extracted."
                    )

        if result["mask"] is not None:

            with st.expander("View Skin Mask"):

                st.image(
                    result["mask"],
                    use_container_width=True
                )

        # ==========================================================
        # Beauty Profile
        # ==========================================================

        if analysis is not None:

            st.markdown(
                '<div class="section-title">Beauty Profile</div>',
                unsafe_allow_html=True
            )

            face_shape_name = "Unknown"

            if face_shape is not None:

                face_shape_name = face_shape["shape"]

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "🎨 Skin Tone",
                    analysis["tone"]
                )

            with c2:

                st.metric(
                    "🌡 Undertone",
                    analysis["undertone"]
                )

            with c3:

                st.metric(
                    "😊 Face Shape",
                    face_shape_name
                )

            with c4:

                st.metric(
                    "📊 ITA Score",
                    round(analysis["ita"], 2)
                )

            st.markdown("---")

            left, right = st.columns(2)

            with left:

                with st.container(border=True):

                    st.subheader("📈 Skin Statistics")

                    st.write(
                        f"**Average RGB:** {analysis['rgb']}"
                    )

                    st.write(
                        f"**LAB Values:** {analysis['lab']}"
                    )

                    st.write(
                        f"**ITA Score:** {analysis['ita']:.2f}"
                    )

            with right:

                if face_shape is not None:

                    with st.container(border=True):

                        st.subheader("📐 Face Measurements")

                        for key, value in face_shape["measurements"].items():

                            st.write(
                                f"**{key}:** {value}"
                            )
        
        # ==========================================================
        # Personalized Recommendations
        # ==========================================================

        if recommendations is not None:

            st.markdown(
                '<div class="section-title">✨ Personalized Makeup Recommendations</div>',
                unsafe_allow_html=True
            )

            category_icons = {
                "Foundation": "🧴",
                "Lipstick": "💄",
                "Blush": "🌸",
                "Eyeshadow": "👁️"
            }

            badge_classes = {
                "💰 Budget Pick": "badge-budget",
                "⭐⭐ Best Value": "badge-best",
                "✨ Premium Pick": "badge-premium"
            }

            for category, products in recommendations.items():

                st.markdown(
                    f"""
                    <h2 style="
                        margin-top:40px;
                        margin-bottom:30px;
                        color:#353535;
                    ">
                        {category_icons.get(category,"✨")} {category}
                    </h2>
                    """,
                    unsafe_allow_html=True
                )

                columns = st.columns(3)

                for column, (tier, product) in zip(columns, products.items()):

                    with column:

                        badge_class = badge_classes.get(
                            tier,
                            "badge-budget"
                        )

                        # -----------------------------
                        # Shade
                        # -----------------------------

                        shade = (
                            product.get("Shade")
                            or product.get("Shade / Variant")
                            or product.get("Shade/Variant")
                            or product.get("Palette")
                            or product.get("Variant")
                            or product.get("Color")
                            or "-"
                        )

                        # -----------------------------
                        # Finish
                        # -----------------------------

                        finish = ""

                        if "Finish" in product:

                            finish = f"""
<div class="rec-label">
Finish
</div>

<div class="rec-value">
{product["Finish"]}
</div>
"""

                        # -----------------------------
                        # Shade Preview
                        # -----------------------------

                        shade_preview = ""

                        if "Hex" in product:

                            shade_preview = f"""
<div style="
display:flex;
align-items:center;
gap:10px;
margin-top:18px;
margin-bottom:16px;
">

<div style="
width:24px;
height:24px;
border-radius:50%;
background:{product["Hex"]};
border:1px solid #DDD;
">
</div>

<span style="
font-size:15px;
color:#666;
">
Shade Preview
</span>

</div>
"""

                        st.markdown(
                            f"""
<div class="rec-card">

<div class="rec-badge {badge_class}">
{tier}
</div>

<div class="rec-brand">
{product["Brand"]}
</div>

<div class="rec-product">
{product["Product"]}
</div>

<hr style="
border:none;
border-top:1px solid #F2D9DF;
margin:22px 0;
">

<div class="rec-label">
Shade
</div>

<div class="rec-value">
{shade}
</div>

{shade_preview}

{finish}

<div class="rec-label">
Price
</div>

<div class="rec-price">
₹{product["Price"]}
</div>

<div class="rec-reason">

<b>💡 Why we recommend it</b>

<br><br>

{product["Reason"]}

</div>

</div>
""",
                            unsafe_allow_html=True
                        )

                st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Footer
# ==========================================================

st.divider()

st.markdown(
    """
<div style="
text-align:center;
padding:25px;
color:#888;
">

<h3 style="color:#444;">
GlowGuide AI
</h3>

<p>
AI Powered Beauty Analysis
</p>

<p>
Made with ❤️ by <b>Aarushi Singh</b>
</p>

</div>
""",
    unsafe_allow_html=True
)