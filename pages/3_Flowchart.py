import streamlit as st
from pathlib import Path
import base64
import streamlit.components.v1 as components



# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "parfois.png"
FLUXO_IMG = BASE_DIR / "Fluxograma.drawio.mermaid.png"

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="PARFOIS – Fluxograma do Processo", layout="wide")

# -------------------------------------------------
# Header (igual às outras páginas)
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
# Conteúdo: título, descrição e imagem do fluxograma
# -------------------------------------------------
st.markdown(
    """
    <div style="font-size:32px; font-weight:600;
                margin-top:4px; margin-bottom:8px;">
        Fluxograma global do projeto
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    """
    Este fluxograma resume todas as etapas do projeto, desde os dados brutos e 
    a modelização em Jupyter, até à aplicação web em Streamlit e ao ciclo de 
    feedback com Supabase para melhoria contínua do modelo de similaridade.
    """
)

st.write(
    """
    A figura mostra como os diferentes blocos se ligam: preparação dos dados,
    cálculo dos embeddings CLIP, construção do `result_df.csv`, explicabilidade,
    deployment via GitHub e Streamlit Cloud, e recolha de feedback dos utilizadores.
    """
)


'''
if FLUXO_IMG.exists():
    st.image(str(FLUXO_IMG), use_container_width=True)
else:
    st.info(
        "A imagem do fluxograma (`Fluxograma.drawio.mermaid.png`) "
        "não foi encontrada na pasta raiz da aplicação."
    )
import base64
'''

import base64

if FLUXO_IMG.exists():
    # Lê a imagem e codifica em base64
    img_bytes = FLUXO_IMG.read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    html = f"""
    <html>
      <head>
        <meta charset="UTF-8" />
        <script src="https://cdn.jsdelivr.net/npm/@panzoom/panzoom@9.4.0/dist/panzoom.min.js"></script>
      </head>
      <body>
        <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
            <button id="zoom-in" style="margin

else:
    st.info(
        "The flowchart image (`Fluxograma.drawio.mermaid.png`) "
        "was not found in the app root folder."
    )
