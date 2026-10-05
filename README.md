# Análisis de sensores industriales

**Los datos son simulados** (100,000 mediciones de sensores en cuatro plantas). No corresponden a una empresa real.

## Objetivo
Analizar con Python las lecturas de temperatura y vibración: promedios por planta, máximo, alertas (> 85 °C, regla didáctica del examen) y exportación de las alertas.

## Datos (`data/sensores.csv`)
| Columna | Significado |
|---|---|
| id_medicion | Identificador de la medición |
| fecha_hora | Fecha y hora de la lectura |
| id_sensor | Identificador del sensor |
| planta | Planta donde está instalado |
| temperatura_c | Temperatura (°C) |
| vibracion_mm_s | Vibración (mm/s) |

## Instalación y ejecución
```bash
git clone <URL_DEL_REPO>
cd <carpeta>
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analisis.py
```
Resultado: se imprime el resumen y se crea `outputs/alertas_temperatura.csv`.

## Estructura
`analisis.py`, `data/`, `outputs/`, `respuestas.md`, `requirements.txt`, `docs/captura_reproducibilidad.png`
