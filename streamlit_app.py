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
st.title("Dysarma Bio: Post-Weaning Intestinal Simulator")
st.markdown(
    "Move the pH slider below to see in real time how the microalga protects and releases the active ingredient along the post-weaning piglet digestive tract."
)

st.markdown("---")

# --- SELECTOR DE pH INTEGRADO EN LA PÁGINA PRINCIPAL ---
st.subheader("Interactive Post-Weaning Parameters")
ph_val = st.slider(
    "Select pH Gradient (Post-Weaning Transition):", 
    min_value=1.0, max_value=9.0, value=6.8, step=0.1
)

# Cálculo cinético de liberación (sigmoideo)
release_pct = min(100.0, max(0.0, 100 / (1 + np.exp(-1.8 * (ph_val - 5.5)))))

# --- VISUAL STATE LOGIC POST-DESTETE ---
if ph_val < 4.0:
    estado_texto = "Stomach (Post-Weaning Acid Phase): Intact and sealed microalga protecting the active ingredient against solid feed stress and gastric acid."
    color_badge = "#20472f"
    posicion_actual = 1
elif 4.0 <= ph_val < 6.0:
    estado_texto = "Transition Window: Stable vehicle structure during the delicate shift from liquid milk to solid vegetable diets."
    color_badge = "#20472f"
    posicion_actual = 1
elif 6.0 <= ph_val < 7.2:
    estado_texto = "Duodenum / Jejunum (Target Zone!): Wall breakdown triggered by rising pH and active deployment of the active ingredient against post-weaning challenges."
    color_badge = "#ef3e93"
    posicion_actual = 2
else:
    estado_texto = "Ileum / Colon: Complete biomass breakdown for local mucosal action."
    color_badge = "#ef3e93"
    posicion_actual = 3

# --- MÉTRICAS ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Environment pH", value=f"{ph_val:.1f}")
with col2:
    st.metric(label="Active Ingredient Released", value=f"{release_pct:.1f} %")

st.markdown("<br>", unsafe_allow_html=True)

# --- DIAGRAMA VISUAL DEL TRACTO DIGESTIVO ---
st.subheader("Digestive Tract Visual Map")

estilo_estomago = "border: 3px solid #ef3e93; background-color: #fce4ec; box-shadow: 0 6px 12px rgba(239,62,147,0.2);" if posicion_actual == 1 else "border: 1px solid #20472f; background-color: #ffffff; opacity: 0.7;"
estilo_duodeno = "border: 3px solid #ef3e93; background-color: #fce4ec; box-shadow: 0 6px 12px rgba(239,62,147,0.2);" if posicion_actual == 2 else "border: 1px solid #20472f; background-color: #ffffff; opacity: 0.7;"
estilo_colon = "border: 3px solid #ef3e93; background-color: #fce4ec; box-shadow: 0 6px 12px rgba(239,62,147,0.2);" if posicion_actual == 3 else "border: 1px solid #20472f; background-color: #ffffff; opacity: 0.7;"

badge_st = "📍 [CAPSULE IN STOMACH / TRANSITION]" if posicion_actual == 1 else "1. Stomach & Solid Feed Transition"
badge_du = "📍 [TARGET ZONE: ACTIVE RELEASE]" if posicion_actual == 2 else "2. Duodenum / Jejunum"
badge_co = "📍 [COMPLETE UNLOAD]" if posicion_actual == 3 else "3. Ileum / Colon"

# HTML sin indentación para evitar que Streamlit lo interprete como bloque de código
html_diagram = f"""<div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 25px;">
<div style="{estilo_estomago} padding: 16px; border-radius: 12px; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
<h4 style="margin: 0; font-size: 16px;">{badge_st}</h4>
<span style="font-size: 12px; font-weight: 700; color: #20472f;">pH 1.0 - 6.0</span>
</div>
<p style="margin: 0; font-size: 13px;">Protective vehicle shield during the post-weaning solid feed adaptation phase. Zero premature leakage.</p>
</div>
<div style="text-align: center; color: #ef3e93; font-weight: bold; font-size: 18px; margin: -4px 0;">↓</div>
<div style="{estilo_duodeno} padding: 16px; border-radius: 12px; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
<h4 style="margin: 0; font-size: 16px;">{badge_du}</h4>
<span style="font-size: 12px; font-weight: 700; color: #ef3e93;">pH 6.0 - 7.0</span>
</div>
<p style="margin: 0; font-size: 13px;"><b>Active Release:</b> Biomass breakdown and deployment of the active ingredient where post-weaning challenges occur.</p>
</div>
<div style="text-align: center; color: #ef3e93; font-weight: bold; font-size: 18px; margin: -4px 0;">↓</div>
<div style="{estilo_colon} padding: 16px; border-radius: 12px; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
<h4 style="margin: 0; font-size: 16px;">{badge_co}</h4>
<span style="font-size: 12px; font-weight: 700; color: #20472f;">pH 7.2 - 8.0</span>
</div>
<p style="margin: 0; font-size: 13px;">Complete unload of remaining biomass and local mucosal action in the lower intestinal tract.</p>
</div>
</div>"""

st.markdown(html_diagram, unsafe_allow_html=True)

# --- DYNAMIC STATUS BLOCK ---
st.markdown(f"""
<div style="background-color: #ffffff; padding: 16px; border-radius: 10px; border-left: 6px solid {color_badge}; margin-bottom: 25px;">
    <h4 style="margin: 0 0 5px 0; color: {color_badge}; font-style: normal;">Current Biocapsule Status</h4>
    <p style="margin: 0; font-size: 15px; font-style: normal;"><b>{estado_texto}</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Natural bioencapsulation platform tailored for post-weaning swine production. Ready for presentation.")
