import os
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
#---------------------------------------
# INPUT FROM THE USER
#______________________________________

from supabase import create_client
import streamlit as st

# Ler as keys do st.secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Criar o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


#--------
# recebe um dicionário com os dados e faz o insert na tabela
#--------


import datetime

def guardar_feedback(
    artigo_escolhido,
    artigos_recomendados,  # lista com 4 IDs
    avaliacoes,            # lista com 4 textos ("mau", "razoável", "bom")
    comentario=None        # texto opcional
):
    row = {
        "artigo_escolhido": str(artigo_escolhido),
        "artigo_1": str(artigos_recomendados[0]),
        "avaliacao_1": str(avaliacoes[0]),
        "artigo_2": str(artigos_recomendados[1]),
        "avaliacao_2": str(avaliacoes[1]),
        "artigo_3": str(artigos_recomendados[2]),
        "avaliacao_3": str(avaliacoes[2]),
        "artigo_4": str(artigos_recomendados[3]),
        "avaliacao_4": str(avaliacoes[3]),
        "comentario": comentario,
    }

    resposta = supabase.table("feedback").insert(row).execute()
    return resposta


    # inserir na tabela "feedback"
    resposta = supabase.table("feedback").insert(row).execute()
    return resposta

#-------------------
# Botão de descarregar dados de comentários
#-------------------

def carregar_feedback_df():
    """Lê a tabela 'feedback' do Supabase e devolve um DataFrame."""
    try:
        resp = supabase.table("feedback").select("*").execute()
        data = resp.data  # lista de dicionários
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao carregar feedback: {e}")
        return pd.DataFrame()




# -------------------------------------------------
# Paths (relative to this file)
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FILES_DIR = BASE_DIR / "Files"
IMAGE_DIRS = [FILES_DIR / "file1", FILES_DIR / "file2", FILES_DIR / "file3"]
LOGO_PATH = BASE_DIR / "parfois.png"

RESULT_CSV = DATA_DIR / "result_df.csv"

# -------------------------------------------------
# Streamlit page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="PARFOIS – Similarity",
    layout="wide"
)

# -------------------------------------------------
# Global style – compact spacing
# -------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.8rem;
        }
        .stApp [data-testid="stImage"] img {
            margin-bottom: 0.1rem;
        }
        h1, h2, h3 {
            margin-top: 0.2rem !important;
            margin-bottom: 0.2rem !important;
        }
        hr {
            margin-top: 0.2rem !important;
            margin-bottom: 0.2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Data helpers
# -------------------------------------------------
@st.cache_data
def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Drop useless index column if present
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Ensure some important columns exist (will warn if missing)
    expected_cols = [
        "image_name", "PROD_REF", "DES_CONC", "Color", "Sizes", "Price",
        "similar_image_1", "similarity_score_1",
        "similar_image_2", "similarity_score_2",
        "similar_image_3", "similarity_score_3",
        "similar_image_4", "similarity_score_4",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        st.warning(f"Warning: missing columns in result_df.csv: {missing}")

    # Format PROD_REF as clean string (no .0 for integers)
    def format_prod_ref(x):
        if pd.isna(x):
            return ""
        try:
            val = float(x)
            if val.is_integer():
                return str(int(val))
            return str(val)
        except Exception:
            return str(x)

    df["PROD_REF_STR"] = df["PROD_REF"].apply(format_prod_ref)

    # Create display label for the selector
    def make_label(row):
        ref = row["PROD_REF_STR"]
        desc = str(row.get("DES_CONC", ""))
        img = str(row["image_name"])
        parts = [img]
        if ref:
            parts.append(ref)
        if desc:
            parts.append(desc)
        return " | ".join(parts)

    df["display_label"] = df.apply(make_label, axis=1)

    return df


def find_image_path(image_name: str) -> Optional[Path]:
    """
    Try to find an image file for the given image_name
    under Files/file1, file2, file3 with common extensions.
    """
    extensions = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".PNG"]

    for folder in IMAGE_DIRS:
        for ext in extensions:
            candidate = folder / f"{image_name}{ext}"
            if candidate.exists():
                return candidate

    return None


def show_product_card(
    row: pd.Series,
    similarity_score: Optional[float] = None,
    compact: bool = False,
    image_scale: float = 0.50,
):
    """
    Show a product card with INFO on the LEFT and IMAGE on the RIGHT.

    Parameters
    ----------
    compact : bool
        If True, show reduced information (for bottom 4 products).
        If False, show full information (for main product).
    image_scale : float
        Factor to resize the image (1.0 = original size).
    """
    info_col, img_col = st.columns([1.2, 1])

    # --- IMAGE ---
    with img_col:
        img_path = find_image_path(str(row["image_name"]))

        if img_path is not None:
            try:
                image = Image.open(img_path)
                w, h = 0.5
                image = image.resize((int(w * image_scale), int(h * image_scale)))
                st.image(image)
            except Exception:
                st.write("Image could not be opened.")
        else:
            st.write("Image not found.")

    # --- TEXT INFO ---
    with info_col:
        if compact:
            # Smaller, lighter text for neighbours
            st.caption(f"ID: {row['image_name']}")
        else:
            st.markdown(f"**Image ID:** `{row['image_name']}`")

        if not compact:
            # Original product – full info
            if not pd.isna(row.get("PROD_REF")) and row.get("PROD_REF_STR"):
                st.write(f"**PROD_REF:** {row['PROD_REF_STR']}")

            if "DES_CONC" in row and not pd.isna(row["DES_CONC"]):
                st.write(f"**Description:** {row['DES_CONC']}")

            if "Color" in row and not pd.isna(row["Color"]):
                st.write(f"**Color:** {row['Color']}")

            if "Sizes" in row and not pd.isna(row["Sizes"]):
                st.write(f"**Sizes:** {row['Sizes']}")

        # In both modes we keep Price (if available)
        if "Price" in row and not pd.isna(row["Price"]):
            try:
                st.write(f"**Price:** {float(row['Price']):.2f} €")
            except Exception:
                st.write(f"**Price:** {row['Price']}")

        # Similarity only when provided
        if similarity_score is not None:
            if compact:
                st.write(f"Sim: {similarity_score:.3f}")
            else:
                st.write(f"**Similarity:** {similarity_score:.3f}")


# -------------------------------------------------
# HEADER (logo + subtitle + section title)
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
            font-size:22px;
            color:#555;
            margin-top:1.5rem;
            margin-bottom:0.2rem;
        ">
            Similarity Detection for Fashion Retail Products - V2.0
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="font-size:32px; font-weight:600;
                margin-top:1px; margin-bottom:1px;">
        Explore product similarities
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Load data
# -------------------------------------------------
if not RESULT_CSV.exists():
    st.error(f"result_df.csv not found at: {RESULT_CSV}")
    st.stop()

df = load_data(RESULT_CSV)

# -------------------------------------------------
# Layout: selector (left) + original product preview (right)
# -------------------------------------------------
left_col, right_col = st.columns([1.3, 2])

with left_col:
    st.subheader("1. Choose a product")

    labels = df["display_label"].sort_values().tolist()

    selected_label = st.selectbox(
        "Search or select by image ID, PROD_REF or description:",
        options=labels,
        index=0 if labels else None
    )

with right_col:
    st.subheader("2. Original product")

    if selected_label:
        selected_row = df.loc[df["display_label"] == selected_label].iloc[0]
        # Original product: full info, normal size
        show_product_card(selected_row, compact=False, image_scale=0.50)

st.markdown("---")
st.subheader("3. Top 4 similar products")

# -------------------------------------------------
# Show neighbours + preparar dados para feedback
# -------------------------------------------------
if selected_label:
    selected_row = df.loc[df["display_label"] == selected_label].iloc[0]

    # Vamos usar o image_name do produto selecionado como "artigo_escolhido"
    artigo_escolhido = selected_row["image_name"]

    similar_entries = []

    for k in range(1, 5):
        img_col = f"similar_image_{k}"
        score_col = f"similarity_score_{k}"

        if img_col not in df.columns or score_col not in df.columns:
            continue

        similar_name = selected_row.get(img_col)
        sim_score = selected_row.get(score_col)

        if pd.isna(similar_name):
            continue

        neighbour_rows = df.loc[df["image_name"] == similar_name]
        if neighbour_rows.empty:
            continue

        neighbour_row = neighbour_rows.iloc[0]
        similar_entries.append((neighbour_row, sim_score))

    if not similar_entries:
        st.info("No similar products found for this item.")
    else:
        cols = st.columns(4)

        # Listas onde vamos guardar os IDs dos artigos recomendados e as avaliações
        artigos_recomendados = []
        avaliacoes = []

        for idx, (col, (row, score)) in enumerate(zip(cols, similar_entries)):
            with col:
                # Neighbours: very compact info, slightly larger image
                show_product_card(
                    row,
                    similarity_score=score,
                    compact=True,
                    image_scale=0.65,  # bigger images for neighbours
                )

                # Usamos o image_name como identificador do artigo recomendado
                artigo_id = row["image_name"]
                artigos_recomendados.append(artigo_id)

                # Radio para avaliação deste artigo
                avaliacao = st.radio(
                    "Rating",
                    ["Bad", "Medium", "Good"],
                    key=f"avaliacao_{artigo_escolhido}_{artigo_id}_{idx}"
                )
                avaliacoes.append(avaliacao)

        # Caixa de comentários do utilizador (opcional)
        comentario = st.text_area(
            "User comments (optional)",
            value="",
            placeholder="Write here your comments or observations..."
        )

        # Botão para guardar o feedback no Supabase
        if len(artigos_recomendados) == 4 and len(avaliacoes) == 4:
            if st.button("Save your input"):
                try:
                    guardar_feedback(
                        artigo_escolhido=artigo_escolhido,
                        artigos_recomendados=artigos_recomendados,
                        avaliacoes=avaliacoes,
                        comentario=comentario  # <-- novo argumento
                    )
                    st.success("Successfully saved. Thanks!")
                except Exception as e:
                    st.error(f"Error while saving: {e}")
        else:
            st.warning("It was not possible to prepare the recommended 4 articles.")


else:
    st.info("Select a product above to see its similar neighbours.")
# -------------------------------------------------
# Secção opcional: descarregar feedback em CSV
# -------------------------------------------------
st.markdown("---")
st.subheader("4. Donwload csv ratings database")

feedback_df = carregar_feedback_df()

if feedback_df.empty:
    st.info("There is still no saved feedback or it was not possible to load the data.")
else:
    csv_bytes = feedback_df.to_csv(index=False, sep=";").encode("utf-8-sig")
    st.download_button(
        label="Download CSV feedback",
        data=csv_bytes,
        file_name="feedback_parfois.csv",
        mime="text/csv",
        key="download_feedback_csv",
    )
