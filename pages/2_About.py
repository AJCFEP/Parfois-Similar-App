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
st.set_page_config(page_title="PARFOIS – About", layout="wide")

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
        About this project
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Overview")
st.write(
    """
    This app displays image–based product similarity for PARFOIS items.
    The similarity matrix and the file `result_df.csv` were computed offline
    in a Jupyter notebook and are only *visualised* here.  
    Below is a high–level description of that pipeline.
    """
)

st.markdown("### 1. Input data")
st.write(
    """
    The notebook starts from two main datasets:

    - **`df_product.csv`** – product catalogue:
      - product reference (`PROD_REF`)
      - color equivalence (`PROD_CLR_EQUIV` / similar field)
      - hierarchical categories (L3, L4, etc.)
      - text descriptions and concatenated description (`DES_CONC`)
      - image identifier (`image_name`).
    - **`df_sales.csv`** – transactional/sales data:
      - quantities and values sold per product/color
      - used to estimate an average **price** per product color equivalence.
    """
)

st.markdown("### 2. Image embeddings with CLIP")
st.write(
    """
    1. Each product image is loaded using the `image_name` field.
    2. A **CLIP** model (image encoder) transforms every image into a fixed–length
       feature vector, typically 512 dimensions.
    3. All embedding vectors are stored in a table, e.g. columns `0`–`511`,
       together with the `image_name`.

    At this point, every product image is represented in a high–dimensional
    vector space that captures its visual characteristics (color, shape, style,…).
    """
)

st.markdown("### 3. Merge with product catalogue")
st.write(
    """
    The embedding table is then merged with `df_product` so that each row contains:

    - `image_name`
    - `PROD_REF`
    - `DES_CONC` (concatenated description from L3/L4 or similar)
    - other attributes such as `Color`, `Sizes`, etc.
    - the full CLIP embedding vector.

    Duplicate rows (same image/name) are removed at this stage.
    """
)

st.markdown("### 4. Price estimation from sales")
st.write(
    """
    To attach a price to each image:

    1. `df_sales` is grouped by a product identifier (e.g. `PROD_CLR_EQUIV`).
    2. For each group, the notebook computes an **average unit price** from the
       sales values and quantities.
    3. This price is mapped back to each `image_name`, giving a `Price` column.
    4. Optionally, the notebook also computes an `Avg_Similar_Price` per product,
       based on the prices of its neighbours.
    """
)

st.markdown("### 5. Similarity computation")
st.write(
    """
    Using the CLIP embeddings, the notebook computes similarity between images:

    1. All embedding vectors are L2-normalised.
    2. **Cosine similarity** is computed between each pair of products:
       \\( \\text{sim}(i,j) = \\frac{v_i \\cdot v_j}{\\|v_i\\| \\; \\|v_j\\|} \\).
    3. For every product *i*, the notebook ranks all other products by similarity
       score and keeps only the top *N* neighbours (e.g. 4, 10, 20,…).

    The result for each product includes fields like:

    - `similar_image_1`, `similarity_score_1`
    - `similar_image_2`, `similarity_score_2`
    - …
    """
)

st.markdown("### 6. Building `result_df.csv`")
st.write(
    """
    Finally, the notebook assembles everything into a single table:

    - One row per **original image** (`image_name`).
    - Columns with product metadata: `PROD_REF`, `DES_CONC`, `Color`, `Sizes`.
    - `Price` (from the sales–based estimation).
    - For each of the top neighbours:
      - `similar_image_k`
      - `similarity_score_k`.

    This table is exported as **`result_df.csv`**, which is the main data source
    used by this Streamlit app.
    """
)

st.markdown("### 7. What the Streamlit app does")
st.write(
    """
    The current app does **not** recompute any embeddings or similarities.
    Instead it:

    1. Loads `result_df.csv`.
    2. Lets the user select a product by `image_name`, `PROD_REF` or description.
    3. Shows the original product image and metadata.
    4. Displays the **top 4 most similar** products, using the neighbour
       information pre-computed in the notebook.

    This separation keeps the heavy model computation offline, while the web app
    remains lightweight and fast for interactive exploration.
    """
)

# -------------------- Team Members --------------------
st.markdown(
    """
    ### Team Members

    This project was developed by a group of MADSAD students from FEP – UP:

    - **André Costa** – *up199401247@edu.fep.up.pt*  
    - **Catarina Monteiro** – *up202107961@edu.fep.up.pt*  
    - **João Monteiro** – *up202006793@edu.fep.up.pt*  
    - **Luis Ferreira** – *up202107032@edu.fep.up.pt*  
    - **Rodrigo Soares** – *up201602617@edu.fep.up.pt*  
    - **Telmo Barbosa** – *up201200195@edu.fep.up.pt*  
    """
)
