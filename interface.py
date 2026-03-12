"""
interface.py — Rediseño 'Luminous Bank' Refinado (Fase 7)
Enfoque en Claridad, Header Vibrante y Navegación Integrada
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

# ── Paleta de Colores Luminous (Banking Premium)
COLORS = {
    "primary": "#2563EB",     # Azul Vibrante (Moderno)
    "secondary": "#1E40AF",   # Azul Institucional
    "header_bg": "#1E3A8A",   # Azul Profundo
    "bg_page": "#F8FAFC",     # Gris casi blanco
    "text_main": "#0F172A",   # Texto principal
    "text_light": "#64748B",  # Texto secundario
    "white": "#FFFFFF",
    "success": "#10B981",    # Verde
    "danger": "#EF4444"       # Rojo
}

# ─────────────────────────────────────────────
# SISTEMA DE ESTILOS (Luminous & Professional)
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Force Light Theme Variables */
    :root {{
        --primary-color: {COLORS['primary']};
        --background-color: {COLORS['bg_page']};
        --secondary-background-color: {COLORS['white']};
        --text-color: {COLORS['text_main']};
        --font: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Global Base */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: {COLORS['bg_page']} !important;
        color: {COLORS['text_main']} !important;
    }}

    /* Inputs Focus & Style */
    input, select, textarea {{
        color: {COLORS['text_main']} !important;
        background-color: {COLORS['white']} !important;
    }}
    
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: {COLORS['white']} !important;
        color: {COLORS['text_main']} !important;
    }}

    /* Fix for Labels */
    label p {{
        color: {COLORS['text_main']} !important;
        font-weight: 600 !important;
    }}

    /* Solid Vibrant Header */
    .header-container {{
        background: {COLORS['header_bg']};
        padding: 2.5rem 2rem 1.5rem 2rem;
        margin: -5rem -5rem 0rem -5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .header-title {{
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }}
    .header-subtitle {{
        font-size: 0.85rem;
        opacity: 0.8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}

    /* Tab Customization - Integrated into Header */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {COLORS['header_bg']} !important;
        justify-content: center;
        gap: 3rem;
        padding-top: 1rem;
        margin: 0rem -5rem 0rem -5rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px !important;
        background-color: transparent !important;
        border: none !important;
        font-weight: 700 !important;
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.9rem !important;
        padding: 0 1rem !important;
        transition: all 0.2s ease;
    }}
    .stTabs [aria-selected="true"] {{
        color: white !important;
        border-bottom: 4px solid {COLORS['primary']} !important;
    }}

    /* Cards - Luminous White */
    .luminous-card {{
        background: {COLORS['white']};
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-top: 0.5rem;
    }}

    /* Section Headers */
    .section-title {{
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {COLORS['primary']};
        margin-bottom: 1.5rem;
        display: block;
        border-left: 4px solid {COLORS['primary']};
        padding-left: 12px;
    }}

    /* Result Panel */
    .result-panel {{
        background: #F8FAFC;
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #E2E8F0;
    }}
    .prob-val {{
        font-size: 4.5rem;
        font-weight: 900;
        color: {COLORS['secondary']};
        line-height: 1;
        margin-bottom: 0.5rem;
    }}
    .prob-label {{
        font-size: 0.8rem;
        color: {COLORS['text_light']};
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }}

    /* Button - Modern Vibrant Blue */
    .stButton button {{
        width: 100% !important;
        background-color: {COLORS['primary']} !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .stButton button:hover {{
        background-color: {COLORS['secondary']} !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.2) !important;
        transform: translateY(-1px);
    }}

    /* Hide UI default junk */
    header[data-testid="stHeader"], div[data-testid="stToolbar"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ── LOGICA ──────────────────────────────────
BACKEND_URL = "http://localhost:8000/predict"
LM_URL      = "http://localhost:1234/v1/chat/completions"

# ── Header Expansivo
st.markdown(f"""
<div class="header-container">
    <div class="header-title">AUDIT ENGINE</div>
    <div class="header-subtitle">Intelligence Layer for Credit Evaluation</div>
</div>
""", unsafe_allow_html=True)

# ── Pestañas
tab1, tab2 = st.tabs(["DIAGNÓSTICO", "ARQUITECTURA"])

with tab1:
    c_left, c_right = st.columns([1.1, 0.9], gap="large")

    with c_left:
        # Se abre la tarjeta y el primer título en el mismo bloque para evitar cierre prematuro del div por el navegador
        st.markdown('<div class="luminous-card"><span class="section-title">Perfil Financiero</span>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            job = st.selectbox("Categoría Profesional — JOB", ["Other", "Office", "Sales", "Mgr", "ProfExe", "Self"])
        with c2:
            reason = st.selectbox("Finalidad — REASON", ["DebtCon", "HomeImp"])
        
        c3, c4 = st.columns(2)
        with c3:
            loan = st.number_input("Capital Solicitado — LOAN ($)", min_value=100.0, value=15000.0)
        with c4:
            mortdue = st.number_input("Saldo Hipotecario — MORTDUE ($)", min_value=0.0, value=65000.0)
        
        c5, c6 = st.columns(2)
        with c5:
            value = st.number_input("Valor de Garantía — VALUE ($)", min_value=100.0, value=120000.0)
        with c6:
            yoj = st.number_input("Estabilidad — YOJ (Años)", min_value=0.0, value=7.0)

        debtinc_desconocido = st.checkbox("DEBTINC desconocido (Imputar media)", value=False)
        debtinc_val = st.number_input("Ratio DTI — DEBTINC (%)", 0.0, 100.0, 32.5, disabled=debtinc_desconocido)

        st.markdown('<span class="section-title" style="margin-top:2.5rem">Comportamiento Crediticio</span>', unsafe_allow_html=True)
        c7, c8, c9 = st.columns(3)
        with c7:
            clage = st.number_input("Madurez — CLAGE (Meses)", 0.0, value=150.0)
        with c8:
            ninq = st.number_input("Consultas — NINQ (6m)", 0, value=1)
        with c9:
            clno = st.number_input("Cuentas Totales — CLNO", 0, value=18)
            
        c10, c11 = st.columns(2)
        with c10:
            derog = st.number_input("Alertas Derogatorias — DEROG", 0, value=0)
        with c11:
            delinq = st.number_input("Líneas en Mora — DELINQ", 0, value=0)

        st.markdown('<div style="margin: 2.5rem 0 1rem 0;"></div>', unsafe_allow_html=True)
        analizar = st.button("EJECUTAR AUDITORÍA")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        if analizar:
            final_debtinc = 33.7799 if (debtinc_desconocido or debtinc_val is None) else debtinc_val
            payload = {
                "job": job, "reason": reason, "loan": loan, "mortdue": mortdue,
                "value": value, "yoj": yoj, "derog": derog, "delinq": delinq,
                "clage": clage, "ninq": ninq, "clno": clno, "debtinc": final_debtinc,
                "debtinc_flag": 1.0 if (debtinc_desconocido or debtinc_val is None) else 0.0
            }

            with st.spinner("Generando Análisis..."):
                try:
                    r = requests.post(BACKEND_URL, json=payload, timeout=10)
                    res = r.json()
                    prob = res["probabilidad_aprobacion"]
                    aprobado = res["aprobado"] == 1

                    st.markdown('<div class="luminous-card">', unsafe_allow_html=True)
                    st.markdown('<span class="section-title">Dictamen Final</span>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="result-panel">
                        <div class="prob-val">{prob*100:.1f}%</div>
                        <div class="prob-label">Probabilidad de Aprobación</div>
                        <div style="font-size: 1rem; font-weight: 800; color:{COLORS['success'] if aprobado else COLORS['danger']}">
                            {'● ACEPTADO' if aprobado else '● RECHAZADO'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # LLM Explanation
                    prompt_sistema = "Eres un Auditor Senior de Riesgos. Expón los fundamentos técnicos de la decisión. Directo, profesional, en bulletpoints."
                    prompt_usuario = f"Resultado: {res['decision']}, Confianza: {prob*100:.1f}%, Datos: {json.dumps(payload)}"

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
                                "temperature": 0.3,
                            },
                            timeout=60
                        )
                        explicacion = lm_resp.json()["choices"][0]["message"]["content"].strip()
                        st.markdown(f'<div style="background:#FFF; padding:1.5rem; border-radius:8px; border:1px solid #F1F5F9; font-size:0.9rem; line-height:1.7;">{explicacion}</div>', unsafe_allow_html=True)
                    except:
                        st.info("Nota: Fundamentos técnicos offline. Verifique parámetros manualmente.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error de conexión con el motor: {e}")
        else:
            st.markdown(f"""
            <div style="text-align:center; padding: 7rem 2rem; border-radius: 12px; border: 2px dashed #E2E8F0; opacity:0.7; margin-top:2rem">
                <div style="font-size: 4rem; margin-bottom: 1rem;">⚖️</div>
                <h4 style="font-weight: 700;">Auditoría Pendiente</h4>
                <p style="font-size:0.9rem">Configure los parámetros del solicitante para obtener el dictamen del modelo.</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="luminous-card"><span class="section-title">Especificaciones de Inferencia</span>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="padding:1.5rem; background:#F8FAFC; border-radius:8px;">
            <p style="font-size:0.85rem; line-height:1.8">
                <b>Arquitectura:</b> ANN Multicapa (MLP)<br>
                <b>Capas:</b> 1 Hidden Layer (10 neuronas)<br>
                <b>Variables:</b> 19 campos normalizados (Z-Score + PMML Norm)<br>
                <b>Activación:</b> Sigmoide + Simplemax Normalization
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding:1.5rem; border:1px solid #F1F5F9; border-radius:8px;">
            <div style="font-size:0.75rem; color:{COLORS['success']}; font-weight:800;">● MOTOR ONLINE</div>
            <p style="font-size:0.85rem; margin-top:0.5rem">Latencia promedio: < 15ms</p>
            <p style="font-size:0.7rem; color:{COLORS['text_light']}">Build 6.2.0 - corporate distribution</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center; color:#CBD5E1; font-size:0.7rem; margin-top:4rem">AUDIT ENGINE | PHASE 7 STANDARDS | CORPORATE LICENSING 2026</p>', unsafe_allow_html=True)
