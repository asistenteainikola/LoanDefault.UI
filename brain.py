#!/usr/bin/env python3
"""
brain.py — Servidor de Inferencia PMML (implementación nativa Python/NumPy)
Fase 1 del Laboratorio Local
Puerto: 8000

ARQUITECTURA DE PREPROCESAMIENTO (replicado de RapidMiner):
  Paso 1: Z-score de cada variable usando los parámetros del training data
          z = (x - mean) / std
  Paso 2: LinearNorm del PMML mapea esos z-scores a [-1, 1]
          norm = 2*(z - orig_low)/(orig_high - orig_low) - 1
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import xml.etree.ElementTree as ET
import os

# ─────────────────────────────────────────────
# Configuración del servidor
# ─────────────────────────────────────────────
app = FastAPI(
    title="Motor Predictivo de Crédito",
    description="Servidor de inferencia nativa para el modelo PMML de Red Neuronal.",
    version="3.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Parámetros Z-score (derivados del hmeq.csv con la misma imputación de RapidMiner)
# Validados contra los LinearNorm orig del PMML para los atributos dummy (coincidencia exacta).
# ─────────────────────────────────────────────
ZSCORE_PARAMS = {
    # (mean, std)  — calculados sobre el dataset completo tras imputar NA con la media
    "JOB_Other":      (0.400671,    0.490076),
    "JOB_Office":     (0.159060,    0.365763),
    "JOB_Sales":      (0.018289,    0.134004),
    "JOB_Mgr":        (0.128691,    0.334886),
    "JOB_ProfExe":    (0.214094,    0.410227),
    "JOB_Self":       (0.032383,    0.177029),
    "REASON_HomeImp": (0.298658,    0.457708),
    "REASON_DebtCon": (0.659060,    0.474065),
    "DEROG":          (0.254570,    0.846047),   # std original (no-nulos) = 0.846
    "DELINQ":         (0.449442,    1.127266),   # std original = 1.127
    "NINQ":           (1.186055,    1.728675),   # std original = 1.729
    "LOAN":           (18607.9698,  11207.4804),
    "MORTDUE":        (73760.8172,  44457.6095), # std original (no-nulos)
    "VALUE":          (101776.0487, 57385.7753), # std original (no-nulos)
    "YOJ":            (8.922268,    7.573982),   # std original (no-nulos)
    "CLAGE":          (179.766275,  85.810092),  # std original (no-nulos)
    "CLNO":           (21.296096,   10.138933),  # std original (no-nulos)
    "DEBTINC":        (33.779915,   8.601746),   # std original (no-nulos)
    "DEBTINC_Flag":   (0.0,         1.0),        # binario: min=0, max=1 → no z-score necesario
}

# ─────────────────────────────────────────────
# Parsear el PMML y extraer la red neuronal
# ─────────────────────────────────────────────
PMML_PATH = os.path.join(os.path.dirname(__file__), "BASIC NEURAL NETWORK CREADA POR MI.pmml")
NS = {"pmml": "http://www.dmg.org/PMML-3_1"}

print(f"[brain.py] Cargando modelo desde: {PMML_PATH}")
if not os.path.exists(PMML_PATH):
    raise FileNotFoundError(f"No se encontró el archivo PMML: {PMML_PATH}")
tree = ET.parse(PMML_PATH)
root = tree.getroot()
nn_el = root.find("pmml:NeuralNetwork", NS)
if nn_el is None:
    raise ValueError("No se encontró el elemento NeuralNetwork en el PMML. Revisa que el archivo esté completo y use el namespace correcto.")
inputs_el = nn_el.find("pmml:NeuralInputs", NS)
if inputs_el is None:
    raise ValueError("No se encontró NeuralInputs en el PMML. Revisa la estructura del archivo.")

# ── Orden de entradas y LinearNorm params ─────────────────────────────────────
INPUT_ORDER  = []
LINEAR_NORMS = {}   # field -> (orig_low, orig_high) para mapear z-score a [-1,1]

for ni in inputs_el.findall("pmml:NeuralInput", NS):
    fid = ni.get("id")
    INPUT_ORDER.append(fid)
    nc = ni.find(".//pmml:NormContinuous", NS)
    if nc is not None:
        norms = nc.findall("pmml:LinearNorm", NS)
        orig_vals = [float(n.get("orig")) for n in norms]
        LINEAR_NORMS[fid] = (orig_vals[0], orig_vals[1])

def preprocess(field: str, raw_value: float) -> float:
    """
    Aplica el preprocesamiento completo de RapidMiner:
      1. Z-score:    z = (raw - mean) / std
      2. LinearNorm: norm = 2*(z - orig_low)/(orig_high - orig_low) - 1
    Luego clampea a [-3, 3] para evitar saturación extrema del sigmoid.
    """
    if field not in ZSCORE_PARAMS:
        z = raw_value
    else:
        mean, std = ZSCORE_PARAMS[field]
        z = (raw_value - mean) / std if std != 0 else 0.0

    if field in LINEAR_NORMS:
        lo, hi = LINEAR_NORMS[field]
        denom = (hi - lo)
        norm = 2.0 * (z - lo) / denom - 1.0 if denom != 0 else 0.0
    else:
        norm = z

    # Clamp a [-3, 3] para evitar saturación extrema del sigmoid
    norm = max(-3.0, min(3.0, norm))
    return float(norm)


# ── Matrices de la red neuronal ────────────────────────────────────────────────
layers_el = nn_el.findall("pmml:NeuralLayer", NS)
if len(layers_el) < 2:
    raise ValueError(f"Se esperaban al menos 2 NeuralLayer en el PMML, se encontraron {len(layers_el)}.")

def parse_layer(layer_el):
    neurons = layer_el.findall("pmml:Neuron", NS)
    ids, biases, weights_list = [], [], []
    for neuron in neurons:
        ids.append(neuron.get("id"))
        biases.append(float(neuron.get("bias")))
        weights_list.append({
            con.get("from"): float(con.get("weight"))
            for con in neuron.findall("pmml:Con", NS)
        })
    return ids, biases, weights_list

hidden_ids, hidden_biases, hidden_weights_raw = parse_layer(layers_el[0])
output_ids, output_biases, output_weights_raw = parse_layer(layers_el[1])

hidden_B = np.array(hidden_biases)
hidden_W = np.zeros((len(hidden_ids), len(INPUT_ORDER)))
for i, w_dict in enumerate(hidden_weights_raw):
    for j, field in enumerate(INPUT_ORDER):
        hidden_W[i, j] = w_dict.get(field, 0.0)

output_B = np.array(output_biases)
output_W = np.zeros((len(output_ids), len(hidden_ids)))
for i, w_dict in enumerate(output_weights_raw):
    for j, hid in enumerate(hidden_ids):
        output_W[i, j] = w_dict.get(hid, 0.0)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

def run_nn(input_vector: np.ndarray) -> dict:
    # Capa Oculta: Activación Logística (Sigmoid)
    hidden_out  = sigmoid(hidden_W @ input_vector + hidden_B)
    
    # Capa de Salida: Activación Logística + Normalización Simplemax
    # Simplemax: prob_i = activation_i / sum(activations)
    output_vals = sigmoid(output_W @ hidden_out + output_B)
    sum_vals = np.sum(output_vals)
    output_prob = output_vals / sum_vals if sum_vals != 0 else output_vals
    
    prob_bad  = float(output_prob[0])
    prob_good = float(output_prob[1])
    return {
        "prediction": "Bad" if prob_bad > prob_good else "Good",
        "prob_bad":    prob_bad,
        "prob_good":   prob_good,
    }

print(f"[brain.py] ✅ Red Neuronal cargada — {len(INPUT_ORDER)} entradas, "
      f"{len(hidden_ids)} neuronas ocultas, {len(output_ids)} salidas.")

# ─────────────────────────────────────────────
# Mapeo JOB y REASON → dummies
# ─────────────────────────────────────────────
JOB_OPCIONES = {
    "Other":   {"JOB_Other":1,"JOB_Office":0,"JOB_Sales":0,"JOB_Mgr":0,"JOB_ProfExe":0,"JOB_Self":0},
    "Office":  {"JOB_Other":0,"JOB_Office":1,"JOB_Sales":0,"JOB_Mgr":0,"JOB_ProfExe":0,"JOB_Self":0},
    "Sales":   {"JOB_Other":0,"JOB_Office":0,"JOB_Sales":1,"JOB_Mgr":0,"JOB_ProfExe":0,"JOB_Self":0},
    "Mgr":     {"JOB_Other":0,"JOB_Office":0,"JOB_Sales":0,"JOB_Mgr":1,"JOB_ProfExe":0,"JOB_Self":0},
    "ProfExe": {"JOB_Other":0,"JOB_Office":0,"JOB_Sales":0,"JOB_Mgr":0,"JOB_ProfExe":1,"JOB_Self":0},
    "Self":    {"JOB_Other":0,"JOB_Office":0,"JOB_Sales":0,"JOB_Mgr":0,"JOB_ProfExe":0,"JOB_Self":1},
}
REASON_OPCIONES = {
    "HomeImp": {"REASON_HomeImp":1,"REASON_DebtCon":0},
    "DebtCon": {"REASON_HomeImp":0,"REASON_DebtCon":1},
}

# ─────────────────────────────────────────────
# Esquema de entrada
# ─────────────────────────────────────────────
class SolicitudCredito(BaseModel):
    job: str          = "Other"
    reason: str       = "DebtCon"
    loan: float       = 10000.0
    mortdue: float    = 50000.0
    value: float      = 100000.0
    yoj: float        = 5.0
    derog: float      = 0.0
    delinq: float     = 0.0
    clage: float      = 100.0
    ninq: float       = 1.0
    clno: float       = 20.0
    debtinc: float    = 30.0
    debtinc_flag: float = 0.0

# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────
@app.get("/")
def raiz():
    return {"status": "activo", "mensaje": "Motor Predictivo v3 en línea. Usa POST /predict"}

@app.post("/predict")
def predecir(datos: SolicitudCredito):
    job_cols    = JOB_OPCIONES.get(datos.job,    JOB_OPCIONES["Other"])
    reason_cols = REASON_OPCIONES.get(datos.reason, REASON_OPCIONES["DebtCon"])

    raw_features = {
        **job_cols,
        **reason_cols,
        "DEROG":        datos.derog,
        "DELINQ":       datos.delinq,
        "NINQ":         datos.ninq,
        "LOAN":         datos.loan,
        "MORTDUE":      datos.mortdue,
        "VALUE":        datos.value,
        "YOJ":          datos.yoj,
        "CLAGE":        datos.clage,
        "CLNO":         datos.clno,
        "DEBTINC":      datos.debtinc,
        "DEBTINC_Flag": datos.debtinc_flag,
    }

    # Aplicar z-score + LinearNorm en el orden exacto del PMML
    input_vector = np.array([
        preprocess(field, raw_features.get(field, 0.0))
        for field in INPUT_ORDER
    ])

    resultado_nn = run_nn(input_vector)
    aprobado = 1 if resultado_nn["prediction"] == "Good" else 0

    return {
        "aprobado":                aprobado,
        "decision":                "APROBADO" if aprobado == 1 else "RECHAZADO",
        "probabilidad_aprobacion": round(resultado_nn["prob_good"], 4),
        "probabilidad_rechazo":    round(resultado_nn["prob_bad"],  4),
        "datos_enviados":          raw_features,
        "_debug_vector":           [round(float(v), 4) for v in input_vector],
    }

@app.get("/health")
def health():
    return {"status": "ok", "modelo_cargado": True, "motor": "Python/NumPy + Z-score correcto"}

# ─────────────────────────────────────────────
# Arranque directo
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("brain:app", host="0.0.0.0", port=8000, reload=False)
