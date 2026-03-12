# 🏦 Audit Engine - Motor Predictivo de Riesgo Crediticio

## 🌟 Visión General
**Audit Engine** es un sistema inteligente de evaluación crediticia *end-to-end* diseñado bajo estándares de banca corporativa. Combina la precisión técnica de una **Red Neuronal Multicapa (MLP)** con la capacidad explicativa de la **IA Generativa Local**, proporcionando dictámenes de riesgo transparentes, rápidos y 100% privados.

![Audit Engine UI](https://raw.githubusercontent.com/asistenteainikola/LoanDefault.UI/main/screenshot.png)

## 🛠️ Innovaciones Técnicas (Fase 7 - Luminous Bank)

### 1. Inferencia Local de Alta Precisión
- **Engine:** Implementación nativa en Python/NumPy de una red neuronal exportada desde PMML (RapidMiner).
- **Normalización Simplemax:** Implementación exacta de la función de activación de salida según la especificación del modelo original, garantizando probabilidades precisas del 0% al 100%.
- **Preprocesamiento Robusto:** Gestión automática de valores atípicos mediante Z-Score y escalamiento lineal `[-3, 3]`. Imputación inteligente de datos faltantes (especialmente en la variable crítica `DEBTINC`).

### 2. Explicabilidad con IA (LLM Core)
Integración fluida con modelos de lenguaje locales (ej. **Gemma 3 12B**) para transformar los *logits* de la red neuronal en informes de fundamentos técnicos comprensibles para auditores humanos.

### 3. Interfaz "Luminous Bank"
UI premium diseñada en Streamlit con:
- Estética limpia, luminosa y corporativa.
- **Trazabilidad Técnica:** Etiquetas de parámetros que incluyen las siglas originales del modelo (YOJ, LOAN, CLAGE) para facilitar la auditoría.
- Diseño responsivo y navegación integrada en el header.

## 🏗️ Arquitectura del Sistema

El ecosistema opera localmente en tres capas:

1.  **Capa de Datos:** Basada en el dataset estándar **HMEQ (Home Equity)**.
2.  **Motor de Inferencia (`brain.py`):** Servidor FastAPI que encapsula la lógica de la red neuronal y los parámetros de normalización.
3.  **Capa de Presentación (`interface.py`):** Consola de auditoría construida en Streamlit que gestiona la interacción y la comunicación con el LLM.

## 📊 Diccionario de Variables (HMEQ Standard)

| Sigla | Atributo Descriptive | Definición |
|---|---|---|
| **LOAN** | Capital Solicitado | Monto del préstamo solicitado. |
| **MORTDUE** | Saldo Hipotecario | Monto adeudado en la hipoteca existente. |
| **VALUE** | Valor de Garantía | Valor de mercado de la propiedad. |
| **YOJ** | Estabilidad | Años de antigüedad en el empleo actual. |
| **DEROG** | Derogatorios | Número de informes derogatorios importantes. |
| **DELINQ** | Líneas en Mora | Número de líneas de crédito en estado de morosidad. |
| **CLAGE** | Madurez | Antigüedad de la línea de crédito más antigua (meses). |
| **NINQ** | Consultas | Número de solicitudes de crédito recientes. |
| **DEBTINC** | Ratio DTI | Relación entre deuda total e ingresos del solicitante. |

## 🚀 Instalación y Despliegue

### Requisitos Previos
- Python 3.10+
- **LM Studio** configurado con un modelo compatible (puerto `1234`).

### Paso a Paso

1. **Clonar Repo e Instalar Dependencias:**
   ```bash
   git clone https://github.com/asistenteainikola/LoanDefault.UI.git
   cd LoanDefault.UI
   pip install -r requirements.txt
   ```
   *(Si no existe requirements.txt, instalar: `pip install fastapi uvicorn streamlit numpy pandas requests`)*

2. **Iniciar el Servidor de Inferencia:**
   ```bash
   python brain.py
   ```

3. **Lanzar la Consola de Auditoría:**
   ```bash
   streamlit run interface.py
   ```

---
**Desarrollado para la excelencia en el análisis de riesgo crédito inteligente.**
© 2026 Audit Engine Project.
