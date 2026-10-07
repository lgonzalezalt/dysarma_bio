import streamlit as st
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Disarma Bio - Interactive Simulator",
    page_icon="🧬",
    layout="centered"
)

# --- CUSTOM CSS STYLES (Agrandir y Poppins sin cursivas, sin barra lateral fija) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;700&display=swap');

    .stApp {
        background-color: #f1f0e9;
        color: #20472f;
        font-family: 'Poppins', sans-serif;
        font-style: normal !important;
    }
    
    /* Ocultamos la barra lateral para que todo quede en la página principal */
    [data-testid="stSidebar"] {
        display: none;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #20472f !important;
        font-family: 'Agrandir', 'Outfit', sans-serif !important;
        font-style: normal !important;
        font-weight: 700 !important;
    }

    p, label, span, div, em, i {
        font-family: 'Poppins', sans-serif !important;
        color: #20472f;
        font-style: normal !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Agrandir', 'Outfit', sans-serif !important;
        font-weight: 700;
        color: #ef3e93 !important;
        font-style: normal !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.title("Disarma Bio: Intestinal Release Simulator")
st.markdown(
    "Move the pH slider below to see in real time how the microalga protects and releases the active ingredient in the piglet digestive tract."
)

st.markdown("---")

# --- SELECTOR DE pH INTEGRADO EN LA PÁGINA PRINCIPAL ---
st.subheader("Interactive Digestive Parameters")
ph_val = st.slider(
    "Select pH Gradient (Gastric & Intestinal):", 
    min_value=1.0, max_value=9.0, value=6.8, step=0.1
)

# Cálculo cinético de liberación (sigmoideo)
release_pct = min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (ph_val - 5.5)))))

# --- VISUAL STATE LOGIC ---
if ph_val < 4.0:
    estado_texto = "Stomach (Gastric Phase): Intact and sealed microalga. Zero premature leakage of the active ingredient."
    color_badge = "#20472f"
elif 4.0 <= ph_val < 6.0:
    estado_texto = "Neonatal Buffer Window: Stable microalgal structure protected by colostrum."
    color_badge = "#20472f"
elif 6.0 <= ph_val < 7.2:
    estado_texto = "Duodenum / Jejunum (Target Zone!): Wall rupture and active deployment of the active ingredient."
    color_badge = "#ef3e93"
else:
    estado_texto = "Ileum / Colon: Complete biomass breakdown for local active ingredient release."
    color_badge = "#ef3e93"

# --- MÉTRICAS ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Environment pH", value=f"{ph_val:.1f}")
with col2:
    st.metric(label="Active Ingredient Released", value=f"{release_pct:.1f} %")

st.markdown("<br>", unsafe_allow_html=True)

# --- DYNAMIC STATUS BLOCK ---
st.markdown(f"""
<div style="background-color: #ffffff; padding: 16px; border-radius: 10px; border-left: 6px solid {color_badge}; margin-bottom: 25px;">
    <h4 style="margin: 0 0 5px 0; color: {color_badge}; font-style: normal;">Current Biocapsule Status</h4>
    <p style="margin: 0; font-size: 15px; font-style: normal;"><b>{estado_texto}</b></p>
</div>
""", unsafe_allow_html=True)

# --- ANATOMICAL MAP CARDS ---
st.subheader("Live Biocapsule Journey")

estilo_estomago = "border: 3px solid #ef3e93; background-color: #fce4ec;" if ph_val < 4.0 else "border: 1px solid #20472f; background-color: #ffffff;"
estilo_duodeno = "border: 3px solid #ef3e93; background-color: #fce4ec;" if (4.0 <= ph_val < 7.2) else "border: 1px solid #20472f; background-color: #ffffff;"
estilo_colon = "border: 3px solid #ef3e93; background-color: #fce4ec;" if ph_val >= 7.2 else "border: 1px solid #20472f; background-color: #ffffff;"

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""
    <div style="{estilo_estomago} padding: 15px; border-radius: 10px; text-align: center; height: 160px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="margin-bottom: 5px; font-size: 16px; font-style: normal;">1. Stomach</h4>
        <p style="font-size: 12px; margin: 0; font-style: normal;"><b>pH 1.0 - 4.0</b><br>Protective microalga shield against gastric acids.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div style="{estilo_duodeno} padding: 15px; border-radius: 10px; text-align: center; height: 160px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="margin-bottom: 5px; font-size: 16px; font-style: normal;">2. Duodenum / Jejunum</h4>
        <p style="font-size: 12px; margin: 0; font-style: normal;"><b>pH 6.0 - 7.0</b><br><b>Active Release</b> of the ingredient against target pathogens.</p>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
    <div style="{estilo_colon} padding: 15px; border-radius: 10px; text-align: center; height: 160px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="margin-bottom: 5px; font-size: 16px; font-style: normal;">3. Ileum / Colon</h4>
        <p style="font-size: 12px; margin: 0; font-style: normal;"><b>pH 7.2 - 8.0</b><br>Complete unload and local mucosal action.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Natural bioencapsulation platform inspired by porcine physiology. Ready for presentation.")
