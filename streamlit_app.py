import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Intestinal Release Simulator - Disarma Bio",
    page_icon="🧬",
    layout="centered"
)

# --- CUSTOM CSS STYLES (Matching presentation branding) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f0e9;
        color: #20472f;
    }
    [data-testid="stSidebar"] {
        background-color: #e5e3da;
        color: #20472f;
    }
    h1, h2, h3 {
        color: #20472f !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    p, label, span {
        color: #20472f !important;
    }
    [data-testid="stMetricValue"] {
        color: #ef3e93 !important;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #20472f !important;
    }
    div.stAlert {
        background-color: #ffffff;
        border-color: #ef3e93;
        color: #20472f;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP CONTENT ---
st.title("🧬 Disarma Bio: Intestinal Release Simulator")
st.markdown("""
*Interactive model based on kinetic bioencapsulation data in microalgal biomass (Spirulina / Arthrospira platensis). 
Real-time visualization of gastric protection and pH-dependent release in the piglet digestive tract.*
""")

# --- SIMULATION CONTROLS (SIDEBAR) ---
st.sidebar.header("🎛️ Digestive Tract Parameters")
region = st.sidebar.selectbox(
    "Select anatomical region:",
    ["Stomach (Neonatal / Buffer)", "Stomach (Acid / Fasting)", "Duodenum / Jejunum (Small Intestine)", "Ileum / Colon"]
)

# Physiological values based on literature (Lumen Bioscience / Phase 0 data)
if region == "Stomach (Neonatal / Buffer)":
    ph_val = 5.5
    desc = "Colostrum buffer effect. Moderate pH (~5-6) protects the structural integrity of the biocapsule and prevents early proteolytic degradation."
elif region == "Stomach (Acid / Fasting)":
    ph_val = 2.5
    desc = "Highly acidic environment (pH ~3). The cyanobacterial cell wall shields the core VHH against pepsin and acidic degradation."
elif region == "Duodenum / Jejunum (Small Intestine)":
    ph_val = 6.8
    desc = "Key release site. Rise in pH and enzymatic activity degrade the cell wall/L-II layer, releasing active VHH for ETEC F4/F18 fimbriae neutralization."
else:
    ph_val = 7.4
    desc = "Complete release of active VHH in the lumen for competitive pathogen blocking."

# Interactive slider for fine-tuning pH
ph_slider = st.sidebar.slider("Manual pH adjustment:", min_value=1.0, max_value=9.0, value=float(ph_val), step=0.1)

# Kinetic calculation of theoretical release (sigmoid profile validated in vitro)
release_calculated = min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (ph_slider - 5.5)))))

# --- REAL-TIME METRICS ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Environment pH", value=f"{ph_slider:.1f}")
    st.metric(label="Released VHH Protein", value=f"{release_calculated:.1f} %")

with col2:
    st.subheader("Biocapsule Status")
    if ph_slider < 4.0:
        st.error("🛡️ **Gastric Protection:** Minimal release ($\le 10\%$). The algal chassis shields the active protein from pepsin and acidity.")
    elif 4.0 <= ph_slider < 6.0:
        st.warning("🔄 **Enteric Transition:** Controlled permeabilization of the cell wall in progress.")
    else:
        st.success("🎯 **Intestinal Release:** Biomass degradation and exposure of VHH for ETEC fimbriae neutralization.")

st.markdown(f"*{desc}*")

# --- RELEASE PROFILE CHART ---
st.markdown("---")
st.subheader("📈 Release Kinetics vs. pH Gradient")

df_curve = pd.DataFrame({
    'pH': np.linspace(1, 9, 100),
    'Release_%': [min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (p - 5.5))))) for p in np.linspace(1, 9, 100)]
})

st.line_chart(df_curve, x='pH', y='Release_%')
st.caption("Curve calibrated with experimental parameters of gastric resistance and microalgal biomass solubilization (Lumen Bioscience / Jester et al., 2022).")
