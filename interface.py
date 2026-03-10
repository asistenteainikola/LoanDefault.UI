"""
interface.py — Interfaz de Usuario (Fase 4)
Sistema Predictivo de Crédito Bancario con IA Explicativa
Puerto: 8501
"""

import streamlit as st
import requests
import json

# ─────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Motor Predictivo de Crédito | IA Local",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CSS Personalizado — diseño premium oscuro
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; }

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0a0e1a;
    color: #e2e8f0;
  }

  /* Fondo general */
  .stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1527 50%, #0a0e1a 100%);
    min-height: 100vh;
  }

  /* Header */
  .hero-header {
    text-align: center;
    padding: 3rem 1rem 2rem 1rem;
    background: linear-gradient(180deg, rgba(99,102,241,0.08) 0%, transparent 100%);
    border-bottom: 1px solid rgba(99,102,241,0.15);
    margin-bottom: 2.5rem;
  }
  .hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin: 0;
  }
  .hero-subtitle {
    font-size: 1.1rem;
    color: #64748b;
    margin-top: 0.6rem;
    font-weight: 400;
  }
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #818cf8;
    margin-top: 1rem;
    font-weight: 500;
  }
  .badge-dot {
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
  }

  /* Panel de inputs */
  .section-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #64748b;
    margin-bottom: 1rem;
    margin-top: 0.5rem;
  }

  /* Inputs de Streamlit */
  .stNumberInput > div > div > input,
  .stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    transition: border-color 0.2s ease;
  }
  .stNumberInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
  }

  /* Labels */
  .stNumberInput label, .stSelectbox label, .stCheckbox label {
    color: #e2e8f0 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
  }

  /* Badge de atributo HMEQ */
  .attr-tag {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 5px;
    padding: 1px 7px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    color: #818cf8;
    letter-spacing: 0.5px;
    margin-right: 6px;
    vertical-align: middle;
  }
  .attr-desc {
    font-size: 0.82rem;
    color: #64748b;
    font-weight: 400;
    vertical-align: middle;
  }

  /* Botón principal */
  .stButton > button {
    width: 100%;
    padding: 0.9rem 2rem;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 24px rgba(99,102,241,0.35);
    letter-spacing: 0.3px;
  }
  .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99,102,241,0.5);
    background: linear-gradient(135deg, #7c7ff7 0%, #9f75ff 100%);
  }
  .stButton > button:active {
    transform: translateY(0px);
  }

  /* Tarjeta de resultado */
  .result-card {
    border-radius: 20px;
    padding: 2.2rem 2rem;
    margin: 1.5rem 0;
    text-align: center;
    animation: fadeInUp 0.5s ease both;
  }
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .result-card.approved {
    background: linear-gradient(135deg, rgba(34,197,94,0.1) 0%, rgba(16,185,129,0.05) 100%);
    border: 1px solid rgba(34,197,94,0.3);
    box-shadow: 0 8px 40px rgba(34,197,94,0.1);
  }
  .result-card.rejected {
    background: linear-gradient(135deg, rgba(239,68,68,0.1) 0%, rgba(220,38,38,0.05) 100%);
    border: 1px solid rgba(239,68,68,0.3);
    box-shadow: 0 8px 40px rgba(239,68,68,0.1);
  }
  .result-icon { font-size: 3.5rem; margin-bottom: 0.5rem; }
  .result-label {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
  }
  .result-label.approved { color: #22c55e; }
  .result-label.rejected { color: #ef4444; }
  .result-sub { font-size: 0.9rem; color: #64748b; margin-top: 0.4rem; }

  /* Barras de probabilidad */
  .prob-bar-wrapper {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
    margin: 6px 0 2px 0;
  }
  .prob-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 1s ease;
  }
  .prob-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 500;
  }

  /* Panel de explicación IA */
  .ia-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1.5rem;
  }
  .ia-panel-title {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #c084fc;
    margin-bottom: 0.8rem;
  }
  .ia-panel p {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin: 0;
  }

  /* Divisor */
  hr { border-color: rgba(255,255,255,0.07) !important; }

  /* Sidebar */
  .css-1d391kg { background: #0d1527; }

  /* Info boxes */
  .stInfo { background: rgba(99,102,241,0.08) !important; border: 1px solid rgba(99,102,241,0.2) !important; }
  .stWarning { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.2) !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0e1a; }
  ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# URLs de servicios locales
# ─────────────────────────────────────────────
BRAIN_URL   = "http://localhost:8000/predict"
LM_URL      = "http://localhost:1234/v1/chat/completions"

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <h1 class="hero-title">Motor Predictivo de Crédito</h1>
  <p class="hero-subtitle">Red Neuronal + Explicación con LLM Local · 100% privado · sin internet</p>
  <span class="hero-badge"><span class="badge-dot"></span>Sistema en línea</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
col_form, col_sep, col_result = st.columns([5, 0.3, 5])

with col_form:
    # ── Sección 1: Perfil del Solicitante
    st.markdown('<div class="section-title">👤 Perfil del Solicitante</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        job = st.selectbox(
            "JOB — Categoría laboral del solicitante",
            options=["Other", "Office", "Sales", "Mgr", "ProfExe", "Self"],
            format_func=lambda x: {
                "Other":   "Other  · Otros oficios",
                "Office":  "Office · Administrativo",
                "Sales":   "Sales  · Ventas",
                "Mgr":     "Mgr    · Gerente",
                "ProfExe": "ProfExe· Prof. Ejecutivo",
                "Self":    "Self   · Independiente",
            }[x],
            help="Atributo JOB en hmeq.csv — Ocupación del solicitante"
        )
    with c2:
        reason = st.selectbox(
            "REASON — Propósito del préstamo",
            options=["DebtCon", "HomeImp"],
            format_func=lambda x: (
                "DebtCon · Consolidación de deuda" if x == "DebtCon"
                else "HomeImp · Mejora del hogar"
            ),
            help="Atributo REASON en hmeq.csv"
        )

    c3, c4 = st.columns(2)
    with c3:
        yoj = st.number_input(
            "YOJ — Años en el trabajo actual",
            min_value=0.0, max_value=40.0, value=5.0, step=0.5,
            help="Years On Job — Atributo YOJ en hmeq.csv"
        )
    with c4:
        debtinc = st.number_input(
            "DEBTINC — Ratio Deuda / Ingreso (%)",
            min_value=0.0, max_value=100.0, value=30.0, step=0.5,
            help="Debt-to-Income ratio — Atributo DEBTINC en hmeq.csv. Si se desconoce, marcar la casilla de abajo."
        )

    debtinc_desconocido = st.checkbox(
        "DEBTINC desconocido — será imputado por el modelo (activa DEBTINC_Flag = 1)",
        value=False
    )
    debtinc_flag = 1.0 if debtinc_desconocido else 0.0

    st.markdown("---")

    # ── Sección 2: Datos Financieros
    st.markdown('<div class="section-title">💰 Datos Financieros</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        loan = st.number_input(
            "LOAN — Monto del préstamo solicitado ($)",
            min_value=100.0, max_value=500000.0, value=10000.0, step=500.0,
            help="Amount of the loan request — Atributo LOAN en hmeq.csv"
        )
    with c6:
        mortdue = st.number_input(
            "MORTDUE — Deuda hipotecaria pendiente ($)",
            min_value=0.0, max_value=1000000.0, value=50000.0, step=1000.0,
            help="Amount due on existing mortgage — Atributo MORTDUE en hmeq.csv"
        )

    c7, c8 = st.columns(2)
    with c7:
        value = st.number_input(
            "VALUE — Valor actual de la propiedad ($)",
            min_value=0.0, max_value=2000000.0, value=100000.0, step=1000.0,
            help="Value of current property — Atributo VALUE en hmeq.csv"
        )
    with c8:
        clno = st.number_input(
            "CLNO — Número de líneas de crédito existentes",
            min_value=0, max_value=100, value=20,
            help="Number of existing credit lines — Atributo CLNO en hmeq.csv"
        )

    c9, c10 = st.columns(2)
    with c9:
        clage = st.number_input(
            "CLAGE — Antigüedad de la cuenta más vieja (meses)",
            min_value=0.0, max_value=600.0, value=100.0, step=5.0,
            help="Age of oldest credit line in months — Atributo CLAGE en hmeq.csv"
        )
    with c10:
        ninq = st.number_input(
            "NINQ — Consultas crediticias recientes",
            min_value=0, max_value=20, value=1,
            help="Number of recent credit inquiries — Atributo NINQ en hmeq.csv"
        )

    st.markdown("---")

    # ── Sección 3: Historial Negativo
    st.markdown('<div class="section-title">⚠️ Historial Negativo</div>', unsafe_allow_html=True)
    c11, c12 = st.columns(2)
    with c11:
        derog = st.number_input(
            "DEROG — Informes derogatorios (negativos graves)",
            min_value=0, max_value=20, value=0,
            help="Number of major derogatory reports — Atributo DEROG en hmeq.csv"
        )
    with c12:
        delinq = st.number_input(
            "DELINQ — Líneas de crédito en mora",
            min_value=0, max_value=20, value=0,
            help="Number of delinquent credit lines — Atributo DELINQ en hmeq.csv"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    analizar = st.button("🧠 Analizar Solicitud", use_container_width=True)

# Separador visual
with col_sep:
    st.markdown("""
    <div style="height:100%;display:flex;align-items:center;justify-content:center;padding-top:12rem;">
      <div style="width:1px;height:250px;background:linear-gradient(to bottom,transparent,rgba(99,102,241,0.3),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PANEL DE RESULTADOS
# ─────────────────────────────────────────────
with col_result:

    if analizar:
        payload = {
            "job": job, "reason": reason,
            "loan": loan, "mortdue": mortdue, "value": value,
            "yoj": yoj, "derog": derog, "delinq": delinq,
            "clage": clage, "ninq": ninq, "clno": clno,
            "debtinc": debtinc, "debtinc_flag": debtinc_flag
        }

        # ── Llamada a brain.py
        with st.spinner("Evaluando con la Red Neuronal..."):
            try:
                resp = requests.post(BRAIN_URL, json=payload, timeout=10)
                resp.raise_for_status()
                resultado = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("❌ No se puede conectar con **brain.py**. Asegúrate de tenerlo corriendo con:\n\n`python3 brain.py`")
                st.stop()
            except Exception as e:
                st.error(f"❌ Error inesperado: {e}")
                st.stop()

        aprobado  = resultado["aprobado"]
        decision  = resultado["decision"]
        prob_ok   = resultado["probabilidad_aprobacion"]
        prob_bad  = resultado["probabilidad_rechazo"]

        # ── Tarjeta de decisión
        if aprobado == 1:
            st.markdown(f"""
            <div class="result-card approved">
              <div class="result-icon">✅</div>
              <p class="result-label approved">APROBADO</p>
              <p class="result-sub">El modelo predice bajo riesgo de impago</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card rejected">
              <div class="result-icon">🚫</div>
              <p class="result-label rejected">RECHAZADO</p>
              <p class="result-sub">El modelo detecta alto riesgo crediticio</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Barras de probabilidad
        st.markdown('<div class="section-title" style="margin-top:1.5rem;">📊 Probabilidades</div>', unsafe_allow_html=True)

        pct_ok  = int(prob_ok * 100)
        pct_bad = int(prob_bad * 100)

        st.markdown(f"""
        <div>
          <div class="prob-label"><span>✅ Aprobación</span><span>{pct_ok}%</span></div>
          <div class="prob-bar-wrapper">
            <div class="prob-bar-fill" style="width:{pct_ok}%;background:linear-gradient(90deg,#22c55e,#4ade80);"></div>
          </div>
        </div>
        <div style="margin-top:0.8rem;">
          <div class="prob-label"><span>🚫 Rechazo</span><span>{pct_bad}%</span></div>
          <div class="prob-bar-wrapper">
            <div class="prob-bar-fill" style="width:{pct_bad}%;background:linear-gradient(90deg,#ef4444,#f87171);"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Explicación con LM Studio
        st.markdown('<div class="section-title" style="margin-top:2rem;">🤖 Explicación con IA (LM Studio)</div>', unsafe_allow_html=True)

        with st.spinner("Generando explicación narrativa..."):
            prompt_sistema = (
                "Eres un analista financiero experto en riesgo crediticio bancario. "
                "Tu tarea es explicar la decisión de un modelo de red neuronal al cliente de forma clara, empática y accesible. "
                "Identifica los 2 o 3 factores más importantes que influyeron en la decisión. "
                "Usa un tono profesional pero humano. "
                "Responde SIEMPRE en español. Máximo 4 oraciones."
            )
            prompt_usuario = (
                f"El modelo predictivo tomó la decisión: {decision}.\n"
                f"Atributos del cliente (base de datos hmeq.csv):\n"
                f"  JOB={job}, REASON={reason}, LOAN={loan:,.0f}, MORTDUE={mortdue:,.0f}, "
                f"VALUE={value:,.0f}, YOJ={yoj}, DEROG={derog}, DELINQ={delinq}, "
                f"NINQ={ninq}, CLAGE={clage}, CLNO={clno}, DEBTINC={debtinc}%, "
                f"DEBTINC_Flag={int(debtinc_flag)}.\n"
                f"Explica brevemente por qué se tomó esta decisión, mencionando los atributos más influyentes por su nombre técnico (DEBTINC, DEROG, DELINQ, etc.)."
            )

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
                        "temperature": 0.6,
                        "max_tokens": 250,
                        "stream": False,
                    },
                    timeout=60,
                )
                lm_resp.raise_for_status()
                explicacion = lm_resp.json()["choices"][0]["message"]["content"].strip()
                st.markdown(f"""
                <div class="ia-panel">
                  <div class="ia-panel-title">💬 Análisis del Asistente IA</div>
                  <p>{explicacion}</p>
                </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.warning("⚠️ LM Studio no está activo en el puerto 1234. El resultado del modelo ya está disponible arriba. Activa LM Studio para obtener la explicación narrativa.")
            except Exception as e:
                st.warning(f"⚠️ No se pudo obtener la explicación de IA: {e}")

        # ── Datos técnicos (expandible)
        with st.expander("🔬 Ver datos técnicos enviados al modelo"):
            st.json(resultado)

    else:
        # Estado vacío (aún no se analiza)
        st.markdown("""
        <div style="
          display:flex; flex-direction:column; align-items:center; justify-content:center;
          height:500px; opacity:0.35;
          border: 1px dashed rgba(99,102,241,0.3);
          border-radius: 20px;
          margin-top: 1rem;
        ">
          <div style="font-size:4rem; margin-bottom:1rem;">🧠</div>
          <p style="font-size:1rem; color:#64748b; text-align:center;">
            Completa el formulario y haz clic en<br><strong style="color:#818cf8;">Analizar Solicitud</strong>
          </p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-size:0.78rem; color:#334155; padding: 0.5rem 0 1.5rem 0;">
  Motor Predictivo · Red Neuronal entrenada en RapidMiner · Infraestructura 100% local<br>
  <span style="color:#4f46e5;">brain.py</span> :8000 &nbsp;·&nbsp;
  <span style="color:#7c3aed;">LM Studio</span> :1234 &nbsp;·&nbsp;
  <span style="color:#0ea5e9;">Streamlit</span> :8501
</div>
""", unsafe_allow_html=True)
