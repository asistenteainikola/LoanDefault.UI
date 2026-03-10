# 🏦 LoanDefault.UI - Motor Predictivo de Crédito Local

Sistema end-to-end para la predicción de riesgos crediticios, combinando una **Red Neuronal nativa** y explicación impulsada por **IA Local (LLM)**. Este proyecto implementa un laboratorio de análisis de datos completo, desde la inferencia técnica hasta la interpretación humana.

![Interfaz de Usuario](https://raw.githubusercontent.com/asistenteainikola/LoanDefault.UI/main/screenshot.png) *(Nota: Imagen referencial)*

## 🚀 Características Principales

-   **⚙️ Motor de Inferencia Nativo:** Implementación en Python/NumPy de una red neuronal exportada desde PMML (RapidMiner), eliminando dependencias pesadas como Java.
-   **🧠 Explicación con IA Local:** Integración con **Gemma 3 12B** (vía LM Studio) para transformar probabilidades técnicas en razones de negocio comprensibles.
-   **🎨 Interfaz Streamlit Premium:** UI moderna con soporte para modo oscuro, visualizaciones de probabilidad y campos de entrada alineados con el dataset estándar `HMEQ`.
-   **🔒 100% Privado y Local:** Todo el procesamiento ocurre en tu máquina. Sin APIs externas, sin filtrado de datos.

## 🏗️ Arquitectura del Sistema

El proyecto se divide en tres capas principales:

1.  **Backend (FastAPI):** `brain.py` carga el modelo y gestiona el preprocesamiento (Z-score + Normalización) y la ejecución de la red neuronal.
2.  **Frontend (Streamlit):** `interface.py` recolecta los datos del usuario y presenta los resultados.
3.  **LLM Layer (LM Studio):** Procesa el resultado de la predicción para generar un informe explicativo.

## 📋 Requisitos

-   Python 3.9+
-   [LM Studio](https://lmstudio.ai/) con el modelo `google/gemma-3-12b` corriendo en el puerto `1234`.
-   Librerías principales: `fastapi`, `uvicorn`, `streamlit`, `numpy`, `pandas`, `requests`.

## 🛠️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/asistenteainikola/LoanDefault.UI.git
   cd LoanDefault.UI
   ```

2. **Instalar dependencias:**
   ```bash
   pip install fastapi uvicorn streamlit numpy pandas requests
   ```

3. **Ejecutar el Motor Predictivo (Backend):**
   ```bash
   python brain.py
   ```

4. **Ejecutar la Interfaz (Frontend):**
   ```bash
   streamlit run interface.py
   ```

## 📊 Sobre el Dataset HMEQ

El modelo utiliza el dataset **Home Equity (HMEQ)**, que contiene información sobre préstamos hipotecarios. Los atributos clave incluyen:
- `LOAN`: Monto solicitado.
- `DEBTINC`: Ratio Deuda/Ingreso.
- `DEROG`: Informes derogatorios graves.
- `DELINQ`: Cuentas morosas.
- `CLAGE`: Antigüedad de la línea de crédito.

---
**Desarrollado con ❤️ para el análisis de riesgo crediticio inteligente.**
