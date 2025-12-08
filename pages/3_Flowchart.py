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

if FLUXO_IMG.exists():
    st.image(str(FLUXO_IMG), use_container_width=True)
else:
    st.info(
        "A imagem do fluxograma (`Fluxograma.drawio.mermaid.png`) "
        "não foi encontrada na pasta raiz da aplicação."
    )
