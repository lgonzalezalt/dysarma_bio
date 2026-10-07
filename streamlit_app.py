import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Intestinal Release Simulator - Disarma Bio",
    page_icon="🧬",
    layout="centered"
)

# --- CUSTOM CSS STYLES (Applying Outfit & Poppins fonts and Disarma Bio branding) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&family=Poppins:wght@300;400;500&display=swap');

    .stApp {
        background-color: #f1f0e9;
        color: #20472f;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #e5e3da;
        color: #20472f;
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #20472f !important;
        font-family: 'Outfit', sans-serif !important;
    }

    p, label, span, div {
        font-family: 'Poppins', sans-serif;
        color: #20472f;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
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
*Interactive kinetic model of VHH release using microalgal biomass (*Spirulina* / *Arthrospira platensis*). 
Real-time simulation of gastric protection and pH-triggered intestinal delivery.*
""")

# --- SIMULATION CONTROLS (SIDEBAR) ---
st.sidebar.header("🎛️ Digestive Tract Parameters")
region = st.sidebar.selectbox(
    "Select anatomical region:",
    ["Stomach (Neonatal / Buffer)", "Stomach (Acid / Fasting)", "Duodenum / Jejunum (Small Intestine)", "Ileum / Colon"]
)

# Preset default values based on selected region
if region == "Stomach (Neonatal / Buffer)":
    default_ph = 5.5
elif region == "Stomach (Acid / Fasting)":
    default_ph = 2.5
elif region == "Duodenum / Jejunum (Small Intestine)":
    default_ph = 6.8
else:
    default_ph = 7.4

# Interactive slider that updates everything in real-time
ph_slider = st.sidebar.slider("Manual pH adjustment (Real-time):", min_value=1.0, max_value=9.0, value=float(default_ph), step=0.1)

# Kinetic calculation of theoretical release (sigmoid profile)
release_calculated = min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (ph_slider - 5.5)))))

# --- REAL-TIME METRICS & DYNAMIC VISUAL STATE ---
st.markdown("---")
col1, col2 = st.columns([1, 1.3])

with col1:
    st.metric(label="Environment pH", value=f"{ph_slider:.1f}")
    st.metric(label="Released VHH Protein", value=f"{release_calculated:.1f} %")

with col2:
    st.subheader("🦠 Biocapsule Real-Time Status")
    if ph_slider < 4.0:
        st.error("🛡️ **Intact Alga (Gastric Protection):** Cell wall tightly sealed. Active VHH proteins are completely protected against pepsin and acidity.")
    elif 4.0 <= ph_slider < 6.0:
        st.warning("🔄 **Transition Phase:** Mild structural swelling. The microalgal biomass is preparing for enzymatic breakdown.")
    else:
        st.success("💥 **Ruptured Alga & Active Release:** Cell wall degraded. VHH deployed into the lumen to block ETEC fimbriae!")

# Dynamic anatomical context description based on exact slider value
if ph_slider < 4.0:
    desc = "Physiological context: Highly acidic gastric environment (pH ~2.5–3). The cyanobacterial cell wall acts as a natural enteric shield."
elif 4.0 <= ph_slider < 6.0:
    desc = "Physiological context: Neonatal buffer window or transition zone. Moderate pH (~5-6) protects integrity and prevents early degradation."
elif 6.0 <= ph_slider < 7.2:
    desc = "Physiological context: Duodenum / Jejunum (Small Intestine). Rise in pH and enzymatic activity trigger wall degradation and target release."
else:
    desc = "Physiological context: Ileum / Colon. Complete structural collapse of the chassis for full local pathogen neutralization."

st.markdown(f"*{desc}*")

# --- INTERACTIVE DYNAMIC CHART ---
st.markdown("---")
st.subheader("📈 Real-Time Release Kinetics vs. pH Gradient")

# Generate curve data
df_curve = pd.DataFrame({
    'pH': np.linspace(1, 9, 100),
    'Release_%': [min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (p - 5.5))))) for p in np.linspace(1, 9, 100)]
})

# Display line chart
st.line_chart(df_curve, x='pH', y='Release_%')
st.caption("Model calibrated with microalgal biomass solubilization parameters (Jester et al., 2022).")
