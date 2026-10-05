# Parte II — Aplicación al caso de Big Data

> Reemplaza los valores marcados con ⟦ ⟧ por los que imprime tu `analisis.py`.

## 5. Las 5 V

| V | Relación con el sistema | Ejemplo concreto | ¿CSV actual o ampliación? |
|---|---|---|---|
| Volumen | Cantidad de datos generados por los sensores | 100,000 lecturas hoy; miles de sensores × 1 lectura/min ≈ millones al día | CSV actual (100,000); crecimiento = ampliación |
| Velocidad | Rapidez con que llegan y deben procesarse | Lecturas cada segundo y alerta en pocos segundos | Ampliación (el CSV tiene 1 lectura/min, ya almacenada) |
| Variedad | Diversidad de formatos y fuentes | Fotos de máquinas, reportes de mantenimiento, JSON de sensores | Ampliación (el CSV solo es tabular) |
| Veracidad | Calidad y confiabilidad de los datos | Un sensor descalibrado o una lectura faltante o atípica | Ampliación/por verificar: el CSV es simulado; habría que validar nulos y outliers en datos reales |
| Valor | Utilidad de los datos para decidir | Detectar la planta con más alertas (⟦planta⟧, ⟦n⟧ alertas) para priorizar mantenimiento | CSV actual |

## 6. Tipos de datos y escala

- CSV de sensores: **estructurado** (filas y columnas fijas).
- Mensaje JSON de un sensor: **semiestructurado** (campos etiquetados, esquema flexible).
- Fotografía de una máquina: **no estructurado**.
- Texto libre de un reporte de mantenimiento: **no estructurado**.

**Por qué 100,000 registros no son Big Data:** el archivo cabe en la memoria de una laptop y se procesa en segundos con una sola máquina y herramientas tradicionales. Big Data se define por las características de los datos (volumen, velocidad, variedad…) y porque el procesamiento tradicional deja de bastar, no por un número fijo de filas.

**Limitaciones al escalar:** la memoria RAM de una sola máquina se agota al cargar todo el archivo; el procesamiento secuencial tarda demasiado; un CSV no sirve para fotos/JSON/texto; no hay tolerancia a fallos ni procesamiento en tiempo real; hace falta almacenamiento y cómputo distribuido.

## 7. Batch y Streaming

- Mi programa realiza **procesamiento por lotes (batch)**: lee un archivo ya guardado y completo, y produce resultados al terminar. Los datos están acotados y no se necesita respuesta inmediata.
- **Alerta en pocos segundos:** **streaming**, procesando cada evento al llegar (p. ej. Kafka + Spark Structured Streaming o Flink) con una regla `temperatura > 85`. La latencia necesaria es de segundos.
- **Resumen diario:** **batch** programado al cierre del día sobre los datos acumulados; el resultado se necesita hasta el final del día, por lo que no se justifica el costo del tiempo real.
- Criterio: elegir según *cuándo* se necesita el resultado (segundos → streaming; horas → batch).

## 8. Lambda y Kappa

**Escenario A → Lambda.** Combina una capa batch (recalcula el historial completo, más exacta) y una capa de velocidad (datos recientes, baja latencia), unidas en una capa de servicio. Justificación: el escenario pide explícitamente dos rutas.

```
            ┌──► [Capa Batch: recalcula historial] ──┐
Sensores ──►[Ingesta]                                  ├──► [Capa de servicio / consultas]
            └──► [Capa de Velocidad: lecturas recientes] ─┘
```

**Escenario B → Kappa.** Una sola lógica de streaming; los eventos se conservan en un log inmutable y, si cambia la lógica o hay errores, se reprocesan reproduciendo el log. Justificación: una sola base de código y reprocesamiento desde el registro.

```
Sensores ──► [Log de eventos (inmutable, conservado)] ──► [Procesamiento de streaming único] ──► [Servicio / consultas]
                         ▲                                              │
                         └────────── reprocesar desde el log ◄──────────┘
```

## 9. Analítica

- **Descriptiva (hallazgos reales):**
  1. La temperatura máxima fue ⟦valor⟧ °C, del sensor ⟦id⟧ el ⟦fecha⟧.
  2. Hubo ⟦n⟧ lecturas > 85 °C; la planta con más alertas fue ⟦planta⟧ con ⟦n⟧.
- **Predictiva:** ¿Qué máquinas tienen mayor probabilidad de fallar en los próximos 7 días? Datos adicionales: historial de fallas y paros, mantenimientos previos, edad y modelo de la máquina, carga de trabajo, tendencia de vibración, condiciones ambientales.
- **Prescriptiva:** si el modelo prevé riesgo alto en una máquina, programar una inspección preventiva antes de que falle. Antes de decidir revisaría: si las alertas son sostenidas o puntuales, el estado del sensor (descalibración), el historial de mantenimiento, el costo de detener la máquina frente al costo de la falla, y la disponibilidad de técnicos y refacciones. Una lectura > 85 °C es solo una alerta del ejercicio; por sí sola no demuestra que la máquina vaya a fallar.
