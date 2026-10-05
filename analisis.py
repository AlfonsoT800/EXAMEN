"""Análisis de sensores industriales (datos simulados)."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
CSV = BASE / "data" / "sensores.csv"          # <- ajusta al nombre real del CSV
SALIDA = BASE / "outputs" / "alertas_temperatura.csv"  # <- ajusta si el examen pide otro nombre
UMBRAL = 85

# Ajusta estos nombres a los encabezados reales del CSV
C_ID, C_FECHA, C_SENSOR, C_PLANTA, C_TEMP, C_VIB = (
    "id_medicion", "fecha_hora", "id_sensor", "planta", "temperatura_c", "vibracion_mm_s")

df = pd.read_csv(CSV)

print(f"Registros: {len(df)}")
print(f"Sensores distintos: {df[C_SENSOR].nunique()}")

print("\nTemperatura promedio por planta:")
print(df.groupby(C_PLANTA)[C_TEMP].mean().round(2).to_string())

tmax = df[C_TEMP].max()
print(f"\nTemperatura máxima: {tmax}")
print(df[df[C_TEMP] == tmax][[C_SENSOR, C_FECHA, C_PLANTA, C_TEMP]].to_string(index=False))

alertas = df[df[C_TEMP] > UMBRAL]
print(f"\nLecturas con temperatura > {UMBRAL} °C: {len(alertas)}")

conteo = alertas.groupby(C_PLANTA).size()
if conteo.empty:
    print("No hay alertas.")
else:
    top = conteo[conteo == conteo.max()]
    print(f"Planta(s) con más alertas ({conteo.max()}): {', '.join(map(str, top.index))}")

SALIDA.parent.mkdir(exist_ok=True)
alertas.to_csv(SALIDA, index=False)
print(f"\nAlertas exportadas a {SALIDA.relative_to(BASE)}")
