import streamlit as st
from pathlib import Path

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

###-----

import base64

if FLUXO_IMG.exists():
    # Read image and encode as base64
    img_bytes = FLUXO_IMG.read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    # HTML + JS with pan/zoom
    html = f"""
    <div id="img-container" style="
        width: 100%;
        max-height: 80vh;
        border: 1px solid #ddd;
        overflow: hidden;
        margin-top: 1rem;
    ">
        <img id="zoom-img"
             src="data:image/png;base64,{img_b64}"
             style="width: 100%; display: block;" />
    </div>

    <!-- Panzoom library -->
    <script src="https://cdn.jsdelivr.net/npm/@panzoom/panzoom@9.4.0/dist/panzoom.min.js"></script>
    <script>
        const elem = document.getElementById('zoom-img');
        const parent = document.getElementById('img-container');

        if (elem && parent) {{
            const panzoom = Panzoom(elem, {{
                maxScale: 5,
                minScale: 1,
                contain: 'outside'
            }});

            parent.addEventListener('wheel', panzoom.zoomWithWheel);
        }}
    </script>
    """

    st.markdown(html, unsafe_allow_html=True)

else:
    st.info(
        "The flowchart image (`Fluxograma.drawio.mermaid.png`) "
        "was not found in the app root folder."
    )
