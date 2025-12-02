import streamlit as st
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "parfois.png"

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="PARFOIS – EDA", layout="wide")

# -------------------------------------------------
# Header (same style as main page)
# -------------------------------------------------
col_logo, col_title = st.columns([2, 3])

with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.write("PARFOIS")

with col_title:
    st.markdown(
        """
        <div style="
            font-family:Arial;
            font-size:26px;
            color:#555;
            margin-top:2.2rem;
            margin-bottom:0.2rem;
        ">
            Similarity Detection for Fashion Retail Products
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# -------------------------------------------------
# Content
# -------------------------------------------------
st.markdown(
    """
    <div style="font-size:32px; font-weight:600;
                margin-top:4px; margin-bottom:4px;">
        Exploratory Data Analysis (EDA)
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("This section is **in development**. Future work will include EDA for products, sales and similarity scores.")
