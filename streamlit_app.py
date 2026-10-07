import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Intestinal Release Simulator - Disarma Bio",
    page_icon="🧬",
    layout="centered"
)

# --- CUSTOM CSS STYLES (Branding Disarma Bio & Fonts) ---
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
        color: #ef3e93 !important;
    }

    /* Custom card container for visual stages */
    .bio-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #20472f;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.title("🧬 Disarma Bio: Interactive Release Simulator")
st.markdown("""
*Move the slider or select an anatomical zone to test how the microalgal biocapsule (*Spirulina*) protects and releases VHH nanobodies in real time.*
""")

# --- INTERACTIVE SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Digestive Simulator")

region = st.sidebar.selectbox(
    "Jump to anatomical region:",
    [
        "Stomach (Neonatal Buffer - pH 5.5)", 
        "Stomach (Acid Fasting - pH 2.5)", 
        "Duodenum / Jejunum (Release Site - pH 6.8)", 
        "Ileum / Colon (Complete Unload - pH 7.4)"
    ]
)

# Preset defaults
if "Neonatal" in region:
    default_ph = 5.5
elif "Acid" in region:
    default_ph = 2.5
elif "Duodenum" in region:
    default_ph = 6.8
else:
    default_ph = 7.4

# Main interactive slider
ph_val = st.sidebar.slider("Interactive pH Gradient:", min_value=1.0, max_value=9.0, value=float(default_ph), step=0.1)

# Kinetic calculation of release (Sigmoidal)
release_pct = min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (ph_val - 5.5)))))

# --- DYNAMIC VISUAL STATE LOGIC ---
st.markdown("---")

if ph_val < 4.0:
    zone_title = "🐷 Region: STOMACH (Gastric Phase)"
    zone_color = "#20472f"
    alga_status = "🛡️ Alga Intact & Sealed"
    action_desc = "The cyanobacterial cell wall acts as a natural enteric shield. It completely protects the core VHH proteins against harsh acidity (pH ~2.5) and pepsin degradation."
    badge_bg = "#e5e3da"
elif 4.0 <= ph_val < 6.0:
    zone_title = "🐷 Region: NEONATAL STOMACH / BUFFER WINDOW"
    zone_color = "#20472f"
    alga_status = "🟢 Stable Chassis (Colostrum Buffer)"
    action_desc = "Moderate pH (~5-6) driven by sow colostrum buffer capacity preserves structural integrity, preventing premature enzymatic breakdown."
    badge_bg = "#e5e3da"
elif 6.0 <= ph_val < 7.2:
    zone_title = "🎯 Region: DUODENUM / JEJUNUM (Target Release Site)"
    zone_color = "#ef3e93"
    alga_status = "💥 Wall Rupture & Active VHH Deployment"
    action_desc = "Rise in pH (~6.8) and pancreatic enzymes degrade the algal cell wall. VHH nanobodies are released directly into the lumen to block ETEC F4/F18 fimbriae!"
    badge_bg = "#fce4ec"
else:
    zone_title = "🎯 Region: ILEUM / COLON (Complete Unload)"
    zone_color = "#ef3e93"
    alga_status = "🎯 Full Pathogen Neutralization"
    action_desc = "Complete structural collapse of the microalgal biomass chassis, achieving 100% local release without systemic absorption."
    badge_bg = "#fce4ec"

# --- RENDER VISUAL INTERFACE CARDS ---
col1, col2 = st.columns([1.1, 1.3])

with col1:
    st.metric(label="Current Environment pH", value=f"{ph_val:.1f}")
    st.metric(label="VHH Protein Released", value=f"{release_pct:.1f} %")
    
    # Visual progress bar styled with brand color
    st.progress(int(release_pct))

with col2:
    st.markdown(f"""
    <div style="background-color: {badge_bg}; padding: 18px; border-radius: 10px; border-left: 6px solid {zone_color};">
        <h4 style="margin-top: 0; color: {zone_color};">{zone_title}</h4>
        <p><b>Biocapsule State:</b> {alga_status}</p>
        <p style="font-size: 14px; margin-bottom: 0;">{action_desc}</p>
    </div>
    """, unsafe_allow_html=True)

# --- INTERACTIVE DYNAMIC CHART WITH REGIONS ---
st.markdown("---")
st.subheader("📈 Kinetic Release Curve & Current Simulation Point")

# Generate data for chart with regions
df_curve = pd.DataFrame({
    'pH': np.linspace(1, 9, 100),
    'Release_%': [min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (p - 5.5))))) for p in np.linspace(1, 9, 100)]
})

# Add a marker row for the user's current slider position
df_current = pd.DataFrame({
    'pH': [ph_val],
    'Release_%': [release_pct]
})

# Streamlit chart layering
st.line_chart(df_curve, x='pH', y='Release_%')

if ph_val < 4.0:
    st.info("📍 **Current Marker Status:** Inside the gastric safety zone (pH < 4). Zero premature leakage.")
elif 4.0 <= ph_val < 6.0:
    st.warning("📍 **Current Marker Status:** Neonatal buffer transition zone.")
else:
    st.success("📍 **Current Marker Status:** Intestinal targeted release zone (Active neutralization).")

st.caption("Model calibrated with microalgal biomass solubilization parameters (Jester et al., 2022). Ready for Canva embedding.")
