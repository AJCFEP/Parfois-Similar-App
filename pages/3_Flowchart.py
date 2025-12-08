import streamlit as st
from pathlib import Path
import base64
import streamlit.components.v1 as components

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "parfois.png"

# Main file for display (SVG – vector, best quality)
FLUXO_SVG = BASE_DIR / "Fluxograma.drawio.mermaid.svg"

# Optional export variants for download
FLUXO_PNG = BASE_DIR / "Fluxograma.drawio.mermaid.png"
FLUXO_JPG = BASE_DIR / "Fluxograma.drawio.mermaid.jpg"   # or .jpeg if you prefer
FLUXO_PDF = BASE_DIR / "Fluxograma.drawio.mermaid.pdf"

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="PARFOIS – Flowchart", layout="wide")

# -------------------------------------------------
# Header (same as other pages)
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

# Make this page use full screen width
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 100%;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Intro text
# -------------------------------------------------
st.markdown(
    """
    <div style="font-size:32px; font-weight:600;
                margin-top:4px; margin-bottom:8px;">
        Global flowchart of the project
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    """
    This flowchart summarizes the complete pipeline of the project, from raw data 
    and Jupyter modeling to the Streamlit web application and the user feedback 
    loop stored in Supabase.
    """
)

st.write(
    """
    It shows how data preparation, CLIP embeddings, the construction of 
    `result_df.csv`, explainability analyses, deployment via GitHub and 
    Streamlit Cloud, and feedback collection are all connected in a single workflow.
    """
)

# -------------------------------------------------
# Flowchart (SVG) with zoom/pan and multiple download buttons
# -------------------------------------------------
if FLUXO_SVG.exists():
    # -----------------------------
    # Download buttons (SVG / PNG / JPG / PDF)
    # -----------------------------
    st.markdown("**Download flowchart:**")

    col1, col2, col3, col4 = st.columns(4)

    # SVG download (always available, since FLUXO_SVG exists)
    with col1:
        svg_bytes = FLUXO_SVG.read_bytes()
        st.download_button(
            label="SVG",
            data=svg_bytes,
            file_name="Parfois_Flowchart.svg",
            mime="image/svg+xml",
        )

    # PNG download (if file exists)
    with col2:
        if FLUXO_PNG.exists():
            png_bytes = FLUXO_PNG.read_bytes()
            st.download_button(
                label="PNG",
                data=png_bytes,
                file_name="Parfois_Flowchart.png",
                mime="image/png",
            )
        else:
            st.caption("PNG not found")

    # JPG download (if file exists)
    with col3:
        if FLUXO_JPG.exists():
            jpg_bytes = FLUXO_JPG.read_bytes()
            st.download_button(
                label="JPEG",
                data=jpg_bytes,
                file_name="Parfois_Flowchart.jpg",
                mime="image/jpeg",
            )
        else:
            st.caption("JPEG not found")

    # PDF download (if file exists)
    with col4:
        if FLUXO_PDF.exists():
            pdf_bytes = FLUXO_PDF.read_bytes()
            st.download_button(
                label="PDF",
                data=pdf_bytes,
                file_name="Parfois_Flowchart.pdf",
                mime="application/pdf",
            )
        else:
            st.caption("PDF not found")

    # -----------------------------
    # Zoomable / pannable viewer (using SVG)
    # -----------------------------
    svg_bytes_for_view = FLUXO_SVG.read_bytes()
    svg_b64 = base64.b64encode(svg_bytes_for_view).decode("utf-8")

    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <style>
          body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
          }}
          #toolbar {{
            margin-top: 16px;
            margin-bottom: 8px;
          }}
          #toolbar button {{
            margin-right: 8px;
          }}
          #img-container {{
            width: 100%;
            height: 80vh;
            border: 1px solid #ddd;
            overflow: hidden;
            position: relative;
            background-color: #f9f9f9;
          }}
          #zoom-img {{
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: top left;
            cursor: grab;
          }}
        </style>
      </head>
      <body>
        <div id="toolbar">
          <button id="zoom-in">+</button>
          <button id="zoom-out">-</button>
          <button id="zoom-reset">Reset</button>
          <span style="margin-left:1rem; color:#666; font-size:0.9rem;">
            Drag to pan. Use mouse wheel or buttons to zoom.
          </span>
        </div>

        <div id="img-container">
          <img id="zoom-img"
               src="data:image/svg+xml;base64,{svg_b64}"
               alt="Project flowchart" />
        </div>

        <script>
          const img = document.getElementById('zoom-img');
          const container = document.getElementById('img-container');
          const btnIn = document.getElementById('zoom-in');
          const btnOut = document.getElementById('zoom-out');
          const btnReset = document.getElementById('zoom-reset');

          let scale = 1.0;
          let minScale = 0.2;
          let maxScale = 5.0;
          let isPanning = false;
          let startX = 0;
          let startY = 0;
          let translateX = 0;
          let translateY = 0;

          function updateTransform() {{
            img.style.transform =
              "translate(" + translateX + "px, " + translateY + "px) scale(" + scale + ")";
          }}

          // Fit image inside container on load (show 100% inside window)
          img.addEventListener('load', function() {{
            const cw = container.clientWidth;
            const ch = container.clientHeight;
            const iw = img.naturalWidth;
            const ih = img.naturalHeight;

            if (iw > 0 && ih > 0) {{
              const s = Math.min(cw / iw, ch / ih);
              scale = s;

              // center image
              translateX = (cw - iw * scale) / 2;
              translateY = (ch - ih * scale) / 2;

              updateTransform();
            }}
          }});

          // Zoom buttons
          btnIn.addEventListener('click', function() {{
            scale = Math.min(maxScale, scale + 0.2);
            updateTransform();
          }});

          btnOut.addEventListener('click', function() {{
            scale = Math.max(minScale, scale - 0.2);
            updateTransform();
          }});

          btnReset.addEventListener('click', function() {{
            // Reset and refit
            const cw = container.clientWidth;
            const ch = container.clientHeight;
            const iw = img.naturalWidth;
            const ih = img.naturalHeight;

            if (iw > 0 && ih > 0) {{
              const s = Math.min(cw / iw, ch / ih);
              scale = s;
              translateX = (cw - iw * scale) / 2;
              translateY = (ch - ih * scale) / 2;
            }} else {{
              scale = 1.0;
              translateX = 0;
              translateY = 0;
            }}
            updateTransform();
          }});

          // Mouse wheel zoom
          container.addEventListener('wheel', function(e) {{
            e.preventDefault();
            const delta = e.deltaY < 0 ? 0.1 : -0.1;
            scale = Math.min(maxScale, Math.max(minScale, scale + delta));
            updateTransform();
          }}, {{ passive: false }});

          // Pan (drag)
          img.addEventListener('mousedown', function(e) {{
            isPanning = true;
            img.style.cursor = 'grabbing';
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
          }});

          window.addEventListener('mousemove', function(e) {{
            if (!isPanning) return;
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateTransform();
          }});

          window.addEventListener('mouseup', function(e) {{
            isPanning = false;
            img.style.cursor = 'grab';
          }});
        </script>
      </body>
    </html>
    """

    components.html(html, height=750, scrolling=False)

else:
    st.info(
        "The flowchart SVG file (`Fluxograma.drawio.mermaid.svg`) "
        "was not found in the app root folder."
    )
