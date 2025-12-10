import streamlit as st
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "parfois.png"

# Explainability + process images (must be in repo root)
FLUXO_IMG = BASE_DIR / "fluxogram.png"
SEMANTIC_IMG = BASE_DIR / "Semantic Consistency (Top-1 Accuracy).png"
REL_DOG_IMG = BASE_DIR / "relevance-dog.png"
REL_FAN_IMG = BASE_DIR / "relevance-fan.png"

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
# Title + Global process figure
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



# -------------------- 1. Overview --------------------
st.markdown("### 1. Overview")
st.write(
    """
    This app displays image–based product similarity for PARFOIS items.
    The similarity matrix and the file `result_df.csv` were computed offline
    in Jupyter notebooks and are only *visualised* here.  
    Below is a high–level description of the data pipeline, the similarity
    model, explainability analysis, and the web application architecture
    (Python → GitHub → Streamlit Cloud → Supabase → user feedback).
    """
)

# -------------------- 2. Input data --------------------
st.markdown("### 2. Input data")
st.write(
    """
    The main notebook starts from two core datasets:

    - **`df_product.csv`** – product catalogue:
      - product reference (`PROD_REF`)
      - image path (`PROG_IMAGE`), from which we extract `image_name`
      - hierarchical categories (`L3_DES`, `L4_DES`)
      - size description (`SZ_DES`)
      - color description (`CLR_DES`).
    - **`df_sales.csv`** – transactional/sales data:
      - quantities and values sold per product/color
      - used to estimate an average **unit price** per color equivalence
        (`PROD_CLR_EQUIV`).
    """
)

# -------------------- 3. Image embeddings with CLIP --------------------
st.markdown("### 3. Image embeddings with CLIP")
st.write(
    """
    1. Each product image is loaded using its `image_name` (stem of the file name).
    2. An OpenAI **CLIP ViT-B/32** model (`clip.load("ViT-B/32")`) transforms every
       image into a **512-dimensional** feature vector.
    3. All embedding vectors are L2-normalised and stored in a table with columns:

       - `image_name`
       - embedding dimensions `0` to `511`.

    At this point, every product image is represented in a high–dimensional
    vector space that captures its visual characteristics (color, shape, style,…).
    """
)

# -------------------- 4. Merge with product catalogue --------------------
st.markdown("### 4. Merge with product catalogue")
st.write(
    """
    The embedding table is then merged with `df_product` so that each row contains:

    - `image_name`
    - `PROD_REF`
    - category descriptors combined as  
      **`L4_DES`**
    - and later, aggregated attributes:

      - **`Sizes`** – concatenation of distinct `SZ_DES` per `PROD_REF`
      - **`Color`** – concatenation of distinct `CLR_DES` per `PROD_REF`.


    Duplicate rows (same image/name) are removed at this stage.
    """
)

# -------------------- 5. Price estimation from sales --------------------
st.markdown("### 5. Price estimation from sales")
st.write(
    """
    To attach a price to each image, the notebook proceeds as follows:

    1. In `df_sales`, an **average unit price** per line is computed as  
       `price = SALES_AMT_FX_RATE / SALES_QTY`.
    2. These prices are aggregated by **`PROD_CLR_EQUIV`** (color equivalence),
       producing a mean unit price per color equivalence code.
    3. Using `df_product`, each `image_name` is mapped to a `PROD_CLR_EQUIV`
       and the corresponding average price, building a dictionary
       `image_to_price[image_name]`.
    4. This yields a **`Price`** column in `result_df`.
    5. Finally, an **`Avg_Similar_Price`** is computed for each product as the
       mean price of its similar neighbours (`similar_image_k`), whenever those
       neighbours have a defined price.
    """
)

# -------------------- 6. Similarity computation --------------------
st.markdown("### 6. Similarity computation")
st.write(
    """
    Using the CLIP embeddings, the notebook computes image–image similarity in
    several steps:

    1. All embeddings are L2-normalised (already done at extraction time).
    2. **Cosine similarity** is computed between embeddings:
       \\( \\text{sim}(i,j) = \\frac{v_i \\cdot v_j}{\\|v_i\\| \\; \\|v_j\\|} \\).
    3. To keep recommendations semantically coherent, products are first
       compared **within the same `DES_CONC` group**:
       - For each `DES_CONC`, a cosine similarity matrix is built.
       - For a given image, neighbours with **similarity ≥ 0.90** and a
         **different `PROD_REF`** are kept as high-confidence candidates.
    4. If fewer than 4 such neighbours exist within the group, the algorithm:
       - Adds all candidates above 0.90 in that group.
       - Fills the remaining slots with the most similar items in the group
         (still excluding the same `PROD_REF`).
    5. If it still has fewer than 4 neighbours, it searches **globally** over
       all images:
       - First, it takes items with global similarity ≥ 0.90,
         excluding the same `PROD_REF` and already selected images.
       - If needed, it finally fills the remaining slots with the
         most similar items globally (still respecting the exclusions).

    The result for each product includes columns like:

    - `similar_image_1`, `similarity_score_1`
    - `similar_image_2`, `similarity_score_2`
    - `similar_image_3`, `similarity_score_3`
    - `similar_image_4`, `similarity_score_4`.
    """
)

# -------------------- 7. Building result_df.csv --------------------
st.markdown("### 7. Building `result_df.csv`")
st.write(
    """
    Finally, the notebook assembles everything into a single table:

    - One row per **original image** (`image_name`).
    - Columns with product metadata: `PROD_REF`, `DES_CONC`, `Sizes`, `Color`.
    - `Price` (from the sales–based estimation).
    - `Avg_Similar_Price` (average price of the selected neighbours).
    - For each of the top neighbours:
      - `similar_image_k`
      - `similarity_score_k`.

    This table is exported as **`result_df.csv`**, which is the main data source
    used by this Streamlit app.
    """
)

# -------------------- 8. Explainability and validation --------------------
st.markdown("### 8. Explainability and validation")

st.write(
    """
    Beyond computing similarities, an additional **Explainability notebook**
    was developed to understand and validate the behaviour of the CLIP-based
    model and the similarity selection.
    """
)

# ---- 8.1 Visual explainability: saliency maps ----
st.markdown("#### 8.1 Visual explainability – CLIP relevance maps")
st.write(
    """
    Using CLIP's image–text capabilities, we generate **relevance (saliency) maps**
    that highlight which regions of an image support a given text concept.
    For a test image, we ask questions such as *“Do you see a dog?”* or
    *“Do you see a fan?”* and visualise where the model focuses.
    """
)

cols_rel = st.columns(2)

with cols_rel[0]:
    if REL_DOG_IMG.exists():
        st.image(
            str(REL_DOG_IMG),
            use_container_width=True,
            caption="Relevance map for the prompt 'dog'"
        )
    else:
        st.info("Relevance image for 'dog' not found in the app folder.")

with cols_rel[1]:
    if REL_FAN_IMG.exists():
        st.image(
            str(REL_FAN_IMG),
            use_container_width=True,
            caption="Relevance map for the prompt 'fan'"
        )
    else:
        st.info("Relevance image for 'fan' not found in the app folder.")

st.write(
    """
    When the text matches the object in the image, the highlighted regions are
    focused and coherent; when the text does **not** match, the heatmap becomes
    noisier or less structured.  
    This provides a **local, visual explanation** of what the CLIP model has
    actually “seen” in each product image.
    """
)

# ---- 8.2 Quantitative explainability: latent space & semantic consistency ----
st.markdown("#### 8.2 Quantitative explainability – latent space and semantic consistency")
st.write(
    """
    On the quantitative side, the explainability notebook performs two analyses:

    1. **Latent space visualisation (PCA)**  
       - The 512-dimensional CLIP embeddings are projected into 2D using PCA.  
       - Points are coloured by product category (e.g. `L4_DES` in an earlier
         version of the dataset).  
       - The resulting scatter plot shows that items from the same category form
         coherent clusters, while related categories are located nearby.

    2. **Semantic consistency (Top-1 accuracy)**  
       - For each product, we compare its category with that of its **most
         similar neighbour** (`similar_image_1`).  
       - The proportion of cases where both share the same category is reported
         as a **Semantic Consistency (Top-1 Accuracy)** metric.
       - A high value indicates that the similarity model is not only visually
         coherent but also semantically aligned with the original catalogue
         labels.
    """
)

if SEMANTIC_IMG.exists():
    st.image(
        str(SEMANTIC_IMG),
        use_container_width=True,
        caption="Semantic Consistency (Top-1 Accuracy) – explainability metric"
    )
else:
    st.info("Semantic consistency figure not found in the app folder.")

# -------------------- 9. Web application architecture and deployment --------------------
st.markdown("### 9. Web application architecture and deployment")

st.write(
    """
    After the offline modelling and explainability work, the project is exposed
    to end users as a **multi-page Streamlit web application**, deployed from
    GitHub to Streamlit Cloud, with **Supabase** integration for
    collecting user feedback about similarity quality.
    """
)

# ---- 9.1 Local Python app: structure and pages ----
st.markdown("#### 9.1 Local Python app – structure and pages")
st.write(
    """
    The core of the web application is implemented in Python using Streamlit:

    - **`Parfois_Similar.py`** – main page:
      - Loads `result_df.csv` and resolves image paths.
      - Builds a selector listing products by `image_name`, `PROD_REF`
        and `DES_CONC`.
      - Displays the selected product with metadata and price.
      - Shows the **top 4 similar products** side by side, including images,
        prices and similarity scores.
    - **`pages/2_About.py`** – this About page:
      - Reuses the PARFOIS header and layout.
      - Documents the full data pipeline, modelling and deployment.
    """
)

# ---- 9.2 Version control with Git and GitHub ----
st.markdown("#### 9.2 Version control with Git and GitHub")
st.write(
    """
    All code, configuration and static assets are versioned with `git` and
    published to a public GitHub repository:

    1. A local folder `Parfois_Similar_App` contains:
       - the Python scripts (`Parfois_Similar.py`, `pages/*.py`)
       - data files (`data/result_df.csv`, `df_product.csv`, `df_sales.csv`)
       - images (`Files/file1`, `Files/file2`, `Files/file3`)
       - explainability figures and the global `fluxogram.png`.
    2. GitHub Desktop (or the git CLI) is used to:
       - detect local changes,
       - create commits with descriptive messages,
       - push everything to the remote repository
         `AJCFEP/Parfois-Similar-App` on GitHub.
    3. GitHub provides:
       - a backup of the project,
       - a complete history of changes,
       - the integration point for Streamlit Cloud deployment.
    """
)

# ---- 9.3 Deployment on Streamlit Cloud ----
st.markdown("#### 9.3 Deployment on Streamlit Cloud")
st.write(
    """
    The public web app is hosted on **Streamlit Cloud**, following these steps:

    1. On https://share.streamlit.io, a new app is configured with:
       - **Repository:** `AJCFEP/Parfois-Similar-App`
       - **Branch:** `main`
       - **Main file:** `Parfois_Similar.py`.
    2. Streamlit Cloud:
       - pulls the latest code from GitHub,
       - installs dependencies from `requirements.txt`
         (e.g. `streamlit`, `pandas`, `numpy`, `Pillow`),
       - runs `Parfois_Similar.py` and serves the app at a public URL.
    3. Any new commit pushed to the GitHub repository triggers an
       **automatic redeploy**, keeping the deployed app aligned with the
       latest academic work.
    """
)

# ---- 9.4 Supabase and user feedback for similarity quality ----
st.markdown("#### 9.4 Supabase and user feedback on similarity quality")
st.write(
    """
    To evaluate and improve the similarity model from real user interactions,
    the application includs a **feedback form** connected to
    a Supabase backend:

    1. **Feedback UI in Streamlit**  
       - For a given reference product and its 4 neighbours, the app show:
         - a dropdown or radio button to select the *best* neighbour,
         - sliders or rating widgets (e.g. 1–5) to score similarity quality,
         - a free-text field for optional comments.
       - A button (e.g. *“Save your input”*) sends this information to the
         backend only when the user explicitly confirms.
    2. **Supabase as a cloud database**  
       - Supabase (PostgreSQL + REST API) is configured with a table such as
         `feedback` containing:
           - `timestamp`
           - `original_image_name`
           - `neighbour_image_name`
           - `similarity_score`
           - `user_rating` (numeric)
           - `user_comment` (text).
       - Streamlit uses the Supabase Python client to `INSERT` rows into this
         table when the feedback button is pressed, maintaining all previous inputs from other users.
    3. **From raw feedback to model refinement**  
       - The `feedback` table can be downloaded and analysed offline
         (in a new notebook) together with `result_df.csv`.
       - Analysts can identify:
         - which categories tend to be over- or under-estimated,
         - whether the 0.90 cosine similarity threshold is too strict or too
           permissive for some product types,
         - patterns in user comments (e.g. recurring “color mismatch”).
       - In future iterations, these insights can guide:
         - adjustments to thresholds,
         - re-weighting of signals (e.g. putting more emphasis on `DES_CONC`
           coherence or price proximity),
         - and even fine-tuning or replacement of the CLIP model, closing a
           **human-in-the-loop** improvement cycle.
    """
)

# -------------------- Team Members --------------------
st.markdown("### Team Members")
st.write(
    """
    This project was developed by a group of MADSAD students from FEP – UP at "Quantitative Case Studies" course:

    - **André Costa** – *up199401247@edu.fep.up.pt*  
    - **Catarina Monteiro** – *up202107961@edu.fep.up.pt*  
    - **João Monteiro** – *up202006793@edu.fep.up.pt*  
    - **Luis Ferreira** – *up202107032@edu.fep.up.pt*  
    - **Rodrigo Soares** – *up201602617@edu.fep.up.pt*  
    - **Telmo Barbosa** – *up201200195@edu.fep.up.pt*  
    """
)
