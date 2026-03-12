"""
interface.py — Rediseño Completo (Fase 5 - Minimalista & Bancario)
Sistema Predictivo de Crédito Bancario con Estilo Institucional
"""

import streamlit as st
import requests
import json

# ─────────────────────────────────────────────
# Configuración Superior de Página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Audit System | Credit Risk Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Paleta de Colores Soberia (Estilo Bancario Premium)
COLORS = {
    "primary": "#0F172A",    # Navy profundo (Casi negro)
    "accent": "#1E40AF",     # Azul Institucional
    "bg_light": "#F8FAFC",   # Fondo suave
    "text_main": "#1E293B",  # Texto principal
    "text_sub": "#64748B",   # Texto secundario
    "border": "#E2E8F0",     # Bordes limpios
    "white": "#FFFFFF",
    "success": "#059669",    # Verde esmeralda (Aprobación)
    "danger": "#DC2626"      # Rojo corporativo (Rechazo)
}

# ─────────────────────────────────────────────
# SISTEMA DE ESTILOS (Sencillo, Ordenado, Moderno)
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {COLORS['bg_light']};
        color: {COLORS['text_main']};
    }}

    /* Header & Branding */
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: {COLORS['white']};
        border-bottom: 1px solid {COLORS['border']};
        margin-bottom: 2rem;
    }}
    .logo-text {{
        font-weight: 800;
        letter-spacing: -0.5px;
        font-size: 1.25rem;
        color: {COLORS['primary']};
    }}
    .logo-text span {{
        color: {COLORS['accent']};
        font-weight: 400;
    }}

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        border-bottom: 2px solid {COLORS['border']};
        margin-bottom: 2rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px !important;
        background-color: transparent !important;
        border: none !important;
        font-weight: 600 !important;
        color: {COLORS['text_sub']} !important;
        font-size: 0.95rem !important;
        padding: 0 0.5rem !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {COLORS['accent']} !important;
        border-bottom: 2px solid {COLORS['accent']} !important;
    }}

    /* Card Styling */
    .console-card {{
        background: {COLORS['white']};
        padding: 2.5rem;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }}

    /* Section Headers */
    .section-header {{
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {COLORS['text_sub']};
        margin-bottom: 1.5rem;
        border-left: 3px solid {COLORS['accent']};
        padding-left: 10px;
    }}

    /* Form Fields */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div {{
        border-radius: 8px !important;
        border: 1px solid {COLORS['border']} !important;
        background-color: {COLORS['bg_light']} !important;
    }}

    /* Action Button */
    .stButton button {{
        width: 100% !important;
        background-color: {COLORS['primary']} !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }}
    .stButton button:hover {{
        background-color: {COLORS['accent']} !important;
        transform: translateY(-1px);
    }}

    /* Results */
    .result-badge {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.8rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }}
    .approved-badge {{ background: #D1FAE5; color: {COLORS['success']}; }}
    .rejected-badge {{ background: #FEE2E2; color: {COLORS['danger']}; }}

    .prob-text {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {COLORS['primary']};
        margin-bottom: 0.5rem;
    }}

    /* Audit Panel */
    .audit-panel {{
        background-color: #F1F5F9;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid {COLORS['border']};
        line-height: 1.7;
    }}
    .audit-label {{
        color: {COLORS['accent']};
        font-weight: 700;
        font-size: 0.7rem;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: block;
    }}

    /* Hide Streamlit elements */
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGICA Y SERVICIOS
# ─────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000/predict"
LM_URL      = "http://localhost:1234/v1/chat/completions"

# ── Header de Marca
st.markdown(f"""
<div class="top-bar">
    <div class="logo-text">AUDIT<span>ENGINE</span></div>
    <div style="font-size: 0.8rem; color: {COLORS['text_sub']}; font-weight: 500;">
        SISTEMA DE AUDITORÍA DE RIESGO DE CRÉDITO © 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTRUCTURA DE PESTAÑAS
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["DIAGNÓSTICO DE RIESGO", "ESPECIFICACIONES DEL MODELO"])

# --- TAB 1: DIAGNÓSTICO ---
with tab1:
    col_entry, col_analysis = st.columns([1.2, 0.8], gap="large")

    with col_entry:
        st.markdown('<div class="console-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Entrada de Parámetros</div>', unsafe_allow_html=True)
        
        # Grid 1: Identidad Financiera
        c1, c2 = st.columns(2)
        with c1:
            job = st.selectbox("Categoría Laboral (JOB)", 
                             ["Other", "Office", "Sales", "Mgr", "ProfExe", "Self"])
        with c2:
            reason = st.selectbox("Propósito del Préstamo (REASON)", ["DebtCon", "HomeImp"])
        
        # Grid 2: Valores del Préstamo
        c3, c4 = st.columns(2)
        with c3:
            loan = st.number_input("Monto del Préstamo ($)", min_value=100.0, value=15000.0)
        with c4:
            mortdue = st.number_input("Deuda Hipotecaria ($)", min_value=0.0, value=65000.0)
        
        # Grid 3: Atributos de solvencia
        c5, c6, c7 = st.columns(3)
        with c5:
            value = st.number_input("Valor Propiedad ($)", min_value=100.0, value=120000.0)
        with c6:
            yoj = st.number_input("Antigüedad Laboral (Años)", min_value=0.0, value=7.0)
        with c7:
            debtinc_desconocido = st.checkbox("DEBTINC desconocido", value=False)
            debtinc_val = st.number_input("Ratio Deuda/Ingreso (%)", 0.0, 100.0, 32.5, disabled=debtinc_desconocido)

        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Historial Crediticio</div>', unsafe_allow_html=True)
        
        c8, c9, c10 = st.columns(3)
        with c8:
            clage = st.number_input("Edad Cuenta (meses)", 0.0, value=150.0)
        with c9:
            ninq = st.number_input("Consultas Recientes", 0, value=1)
        with c10:
            clno = st.number_input("Líneas de Crédito", 0, value=18)
            
        c11, c12 = st.columns(2)
        with c11:
            derog = st.number_input("Informes Derogatorios", 0, value=0)
        with c12:
            delinq = st.number_input("Líneas en Mora", 0, value=0)

        st.markdown('<div style="margin: 2.5rem 0;"></div>', unsafe_allow_html=True)
        analizar = st.button("EJECUTAR ANÁLISIS PREDICTIVO")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_analysis:
        if analizar:
            # Imputación
            final_debtinc = 33.7799 if (debtinc_desconocido or debtinc_val is None) else debtinc_val
            payload = {
                "job": job, "reason": reason, "loan": loan, "mortdue": mortdue,
                "value": value, "yoj": yoj, "derog": derog, "delinq": delinq,
                "clage": clage, "ninq": ninq, "clno": clno, "debtinc": final_debtinc,
                "debtinc_flag": 1.0 if (debtinc_desconocido or debtinc_val is None) else 0.0
            }

            with st.spinner("Procesando Dictamen..."):
                try:
                    r = requests.post(BACKEND_URL, json=payload, timeout=10)
                    res = r.json()
                    prob = res["probabilidad_aprobacion"]
                    aprobado = res["aprobado"] == 1

                    st.markdown('<div class="console-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-header">Dictamen del Auditor</div>', unsafe_allow_html=True)
                    
                    if aprobado:
                        st.markdown('<span class="result-badge approved-badge">✓ CRÉDITO APROBADO</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="result-badge rejected-badge">✗ CRÉDITO RECHAZADO</span>', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="prob-text">{prob*100:.1f}%</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:{COLORS["text_sub"]}; font-size: 0.9rem; margin-bottom: 2rem;">Índice de Confianza del Modelo</div>', unsafe_allow_html=True)
                    
                    # LLM Explanation
                    prompt_sistema = (
                        "Eres un Auditor Senior de Riesgos. Expón EXCLUSIVAMENTE los fundamentos técnicos "
                        "de la decisión. No incluyas formalidades. Español directo y profesional."
                    )
                    prompt_usuario = f"Decisión: {res['decision']}\nProbabilidad: {prob*100:.1f}%\nEntrada: {json.dumps(payload)}"

                    try:
                        lm_resp = requests.post(
                            LM_URL,
                            headers={"Content-Type": "application/json"},
                            json={
                                "model": "google/gemma-3-12b",
                                "messages": [
                                    {"role": "system", "content": prompt_sistema},
                                    {"role": "user",   "content": prompt_usuario},
                                ],
                                "temperature": 0.5,
                            },
                            timeout=60
                        )
                        explicacion = lm_resp.json()["choices"][0]["message"]["content"].strip()
                        
                        st.markdown(f"""
                        <div class="audit-panel">
                            <span class="audit-label">Informe de Fundamentos Técnicos</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(explicacion)

                    except Exception as e:
                        st.error("No se pudo conectar con el motor de explicación IA.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error de conexión con el motor predictivo: {e}")
        else:
            st.markdown(f"""
            <div style="text-align:center; padding: 5rem 2rem; border: 2px dashed {COLORS['border']}; border-radius: 12px; opacity:0.6;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚖️</div>
                <div style="font-weight: 600; color: {COLORS['text_sub']};">Esperando Datos de Solicitante</div>
                <p style="font-size: 0.85rem; color: {COLORS['text_sub']};">Ingrese la información en el panel izquierdo para generar el dictamen.</p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: ARQUITECTURA ---
with tab2:
    st.markdown('<div class="console-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Especificaciones de Ingeniería</div>', unsafe_allow_html=True)
    
    col_info, col_flow = st.columns([1, 1], gap="large")
    
    with col_info:
        st.markdown(f"""
        <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 1rem;">Modelo Red Neuronal MLP</h3>
        <p style="color: {COLORS['text_sub']}; line-height: 1.7; margin-bottom: 2rem;">
            El motor predictivo está basado en un Perceptrón Multicapa (MLP) optimizado mediante <b>Búsqueda en Rejilla (Grid Search)</b> para maximizar la precisión en el dataset HMEQ.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="padding: 1rem; border: 1px solid {COLORS['border']}; border-radius: 8px;">
                <div style="font-size: 0.7rem; font-weight: 700; color: {COLORS['text_sub']};">NEURONAS OCULTAS</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: {COLORS['accent']};">10 Unidades</div>
            </div>
            <div style="padding: 1rem; border: 1px solid {COLORS['border']}; border-radius: 8px;">
                <div style="font-size: 0.7rem; font-weight: 700; color: {COLORS['text_sub']};">FUNCIÓN ACTIVACIÓN</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: {COLORS['accent']};">Sigmoide</div>
            </div>
            <div style="padding: 1rem; border: 1px solid {COLORS['border']}; border-radius: 8px;">
                <div style="font-size: 0.7rem; font-weight: 700; color: {COLORS['text_sub']};">VARIABLES ENTRADA</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: {COLORS['accent']};">19 Atributos</div>
            </div>
            <div style="padding: 1rem; border: 1px solid {COLORS['border']}; border-radius: 8px;">
                <div style="font-size: 0.7rem; font-weight: 700; color: {COLORS['text_sub']};">MOTOR INFERENCIA</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: {COLORS['accent']};">NumPy / Python</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_flow:
        st.markdown(f"""
        <div style="background: {COLORS['bg_light']}; padding: 2rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 0.8rem; font-weight: 700; color: {COLORS['text_sub']}; margin-bottom: 1rem;">FLUJO DE PROCESAMIENTO</div>
            <div style="font-weight: 600; padding: 0.75rem; border: 1px solid {COLORS['border']}; border-radius: 8px; background: white;">Entrada de Datos</div>
            <div style="margin: 10px;">↓</div>
            <div style="font-weight: 600; padding: 0.75rem; border: 1px solid {COLORS['accent']}; border-radius: 8px; background: {COLORS['accent']}10; color: {COLORS['accent']};">Capa Oculta (10 neuronas)</div>
            <div style="margin: 10px;">↓</div>
            <div style="font-weight: 600; padding: 0.75rem; border: 1px solid {COLORS['primary']}; border-radius: 8px; background: {COLORS['primary']}; color: white;">Clasificación Final (Softmax)</div>
            <div style="margin-top: 2rem; font-size: 0.8rem; color: {COLORS['success']}; font-weight: 700;">● SISTEMA OPERATIVO Y VALIDADO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer
st.markdown(f"""
<div style="text-align: center; margin-top: 4rem; padding-bottom: 2rem;">
    <p style="color: {COLORS['text_sub']}; font-size: 0.75rem;">AUDIT ENGINE | PHASE 5 STANDARDS | CORPORATE BANKING EDITION</p>
</div>
""", unsafe_allow_html=True)
