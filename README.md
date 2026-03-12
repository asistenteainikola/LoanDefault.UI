# 🏦 Audit Engine - Sistema Predictivo de Riesgo Crediticio

![Audit Engine UI Premium](https://raw.githubusercontent.com/asistenteainikola/LoanDefault.UI/main/screenshot.png)

## 🌟 Visión del Proyecto
**Audit Engine** es un ecosistema de evaluación crediticia *end-to-end* diseñado bajo estándares de banca corporativa internacional. El sistema trasciende la simple predicción mediante un enfoque **híbrido de IA**: combina la precisión matemática de una **Red Neuronal Multicapa (MLP)** nativa con la capacidad explicativa de **IA Generativa Local**, proporcionando dictámenes de riesgo transparentes, rápidos y con privacidad de datos total.

---

## 🚀 Innovaciones Técnicas (Phase 7 - Luminous Bank)

### 1. Inferencia Nativa de Alto Rendimiento
*   **Engine:** Core desarrollado en Python/NumPy que decodifica y ejecuta una red neuronal exportada desde PMML (RapidMiner).
*   **Pipeline de Datos:** Replicación exacta del preprocesamiento de RapidMiner:
    *   **Normalización Z-Score:** Basada en parámetros precisos del dataset HMEQ.
    *   **LinearNorm Mapper:** Transformación de características al espacio exacto `[-1, 1]` requerido por el modelo.
    *   **Simplemax Output:** Implementación de la función de activación de salida para garantizar probabilidades de aprobación coherentes con la especificación original.

### 2. Explicabilidad con IA (LLM Hybrid Core)
Integración fluida con modelos de lenguaje locales (ej. **Gemma 3 12B**) que actúan como un **Auditor Senior virtual**. Este componente transforma los *logits* y probabilidades de la red neuronal en informes de fundamentos técnicos estructurados, permitiendo a los analistas humanos comprender el "porqué" detrás de cada decisión.

### 3. Interfaz "Luminous Bank"
Una consola de auditoría premium construida en Streamlit con:
*   **Estética Corporativa:** Diseño luminoso, tipografía *Plus Jakarta Sans* y paleta de colores institucional.
*   **Integración de Trazabilidad:** Los campos de entrada conservan la nomenclatura técnica original (YOJ, LOAN, CLAGE, DEBTINC) para facilitar la auditoría cruzada con sistemas legados.
*   **Arquitectura Separada:** Consola de diagnóstico y visor de especificaciones técnicas.

---

## 🏗️ Arquitectura del Sistema

El ecosistema opera localmente en tres capas desacopladas:

1.  **Capa de Datos:** Basada en el dataset estándar **HMEQ (Home Equity)** — 5,960 registros de préstamos garantizados por equidad de vivienda.
2.  **Motor de Inferencia (`brain.py`):** Servidor FastAPI que encapsula la lógica de la red neuronal, manejando latencias inferiores a **15ms**.
3.  **Capa de Presentación (`interface.py`):** Interfaz táctica que orquesta la comunicación entre el usuario, el motor predictivo y el LLM local.

---

## 📊 Diccionario de Variables (HMEQ Standard)

| Atributo | Significado | Descripción Técnica |
| :--- | :--- | :--- |
| **LOAN** | Capital Solicitado | Monto del préstamo solicitado por el cliente. |
| **MORTDUE** | Saldo Hipotecario | Monto adeudado en la hipoteca existente. |
| **VALUE** | Valor de Garantía | Valor de tasación del inmueble en garantía. |
| **YOJ** | Estabilidad Laboral | Años de antigüedad en el empleo actual. |
| **DEROG** | Derogatorios | Número de informes derogatorios en el historial. |
| **DELINQ** | Líneas en Mora | Número de líneas de crédito con morosidad actual. |
| **CLAGE** | Madurez Crediticia | Antigüedad del crédito más antiguo (meses). |
| **NINQ** | Consultas Recientes | Número de solicitudes de crédito en los últimos 6 meses. |
| **DEBTINC** | Ratio DTI | Relación Deuda/Ingresos (El factor más crítico del modelo). |

---

## 🛠️ Instalación y Despliegue

### Requisitos Técnicos
*   Python 3.10 o superior.
*   **LM Studio** (Opcional, para explicaciones) configurado en el puerto `1234`.

### Pasos de Ejecución

1.  **Preparar el entorno:**
    ```bash
    git clone https://github.com/asistenteainikola/LoanDefault.UI.git
    cd LoanDefault.UI
    pip install -r requirements.txt
    ```

2.  **Iniciar el Motor Predictivo (API):**
    ```bash
    python brain.py
    ```

3.  **Lanzar la Consola de Auditoría (UI):**
    ```bash
    streamlit run interface.py
    ```

---

**Audit Engine Project** - *Potenciando la toma de decisiones financieras mediante Inteligencia Artificial Local de alto impacto.*

© 2026 Audit Engine Project. Corporate Distribution.
