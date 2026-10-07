import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Intestinal Release Simulator - Disarma Bio",
    page_icon="🧬",
    layout="centered"
)

# --- CUSTOM CSS STYLES ---
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
        font-weight: bold;
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
*Interactive model of bioencapsulated VHH delivery using microalgal biomass (*Spirulina* / *Arthrospira platensis*). 
Visualizing gastric protection and pH-triggered intestinal release.*
""")

# --- SIMULATION CONTROLS (SIDEBAR) ---
st.sidebar.header("🎛️ Digestive Tract Parameters")
region = st.sidebar.selectbox(
    "Select anatomical region:",
    ["Stomach (Neonatal / Buffer)", "Stomach (Acid / Fasting)", "Duodenum / Jejunum (Small Intestine)", "Ileum / Colon"]
)

# Assign parameters based on selected region
if region == "Stomach (Neonatal / Buffer)":
    ph_val = 5.5
    desc = "Colostrum buffer effect. Moderate pH (~5-6) protects structural integrity."
    status_icon = "🟢"
    status_title = "STABLE CHASSIS (Buffer Phase)"
    status_color = "#20472f" # Green/Dark
elif region == "Stomach (Acid / Fasting)":
    ph_val = 2.5
    desc = "Highly acidic environment (pH ~3). The cell wall shields VHH against pepsin."
    status_icon = "🛡️"
    status_title = "FULL GASTRIC PROTECTION (Intact Alga)"
    status_color = "#20472f"
elif region == "Duodenum / Jejunum (Small Intestine)":
    ph_val = 6.8
    desc = "Key release site. Rise in pH and enzymes degrade the cell wall, releasing active VHH."
    status_icon = "💥"
    status_title = "ACTIVE RELEASE & TARGETING (Wall Rupture)"
    status_color = "#ef3e93" # Pink
else:
    ph_val = 7.4
    desc = "Complete release of active VHH in the lumen for competitive pathogen blocking."
    status_icon = "🎯"
    status_title = "COMPLETE UNLOAD (Pathogen Neutralization)"
    status_color = "#ef3e93"

# Interactive slider for fine-tuning pH
ph_slider = st.sidebar.slider("Manual pH adjustment:", min_value=1.0, max_value=9.0, value=float(ph_val), step=0.1)

# Kinetic calculation of theoretical release
release_calculated = min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (ph_slider - 5.5)))))

# --- DYNAMIC VISUAL STATUS (The Algae Transformation) ---
st.markdown("---")
col1, col2 = st.columns([1, 1.2])

with col1:
    st.metric(label="Environment pH", value=f"{ph_slider:.1f}")
    st.metric(label="Released VHH Protein", value=f"{release_calculated:.1f} %")

with col2:
    st.markdown("### 🦠 Biocapsule State")
    if ph_slider < 4.0:
        st.info("🛡️ **Intact Alga:** Cell wall completely sealed. Core proteins are safely isolated from gastric juices.")
    elif 4.0 <= ph_slider < 6.0:
        st.warning("🔄 **Transition Phase:** Mild structural swelling. Microalga preparing for enzymatic breakdown.")
    else:
        st.success("💥 **Ruptured Alga & Release:** Cell wall degraded. Active VHH deployed to block ETEC fimbriae!")

st.markdown(f"**Anatomical context:** *{desc}*")

# --- RELEASE PROFILE CHART ---
st.markdown("---")
st.subheader("📈 Release Kinetics vs. pH Gradient")

# Generate curve data and color split
df_curve = pd.DataFrame({
    'pH': np.linspace(1, 9, 100),
    'Release_%': [min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (p - 5.5))))) for p in np.linspace(1, 9, 100)]
})

# Display line chart with branding
st.line_chart(df_curve, x='pH', y='Release_%')
st.caption("Model calibrated with microalgal biomass solubilization parameters (Jester et al., 2022).")
