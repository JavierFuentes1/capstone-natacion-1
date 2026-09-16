# Capstone — Natación: ¿es equivalente la exigencia para clasificar según la piscina?

**Pregunta.** ¿Es constante el factor de conversión entre piscina de 25 y 50 m, o
depende del estilo, la distancia y el sexo? ¿Y coincide con la equivalencia implícita
en las marcas mínimas vigentes de World Aquatics?

Felipe Leiva y Javier Fuentes · Diplomado en Ciencia de Datos Aplicada, UTFSM.

---

## Entrega — evaluación 2, primer análisis exploratorio (martes 15 de septiembre)

**El entregable es [`03_eda_capstone.ipynb`](03_eda_capstone.ipynb)**, ejecutado de
principio a fin, con una sección por criterio de la rúbrica. Su primera celda trae la
declaración de uso de IA, la nota sobre los datos que no se pueden compartir y el
orden en que se ejecutan los archivos.

Para correrlo hacen falta dos archivos: `datos/comparacion_wa.csv`, que está en el
repositorio, y `datos/nados.csv`, que **no** está y se regenera con
`uv run python capstone/descargar.py` (ver más abajo). Los demás `.py` de esta carpeta
sirven para reproducir esos insumos; el notebook no los importa.

---

## Estado

| Entrega | Cuándo | Estado |
|---|---|---|
| Formulación (30%) | lu 7-sep | `Formulacion_Capstone_Leiva_Fuentes.pdf`, entregada |
| Análisis exploratorio (40%) | **ma 15-sep** | `03_eda_capstone.ipynb`, ejecutado y revisado contra la rúbrica. Listo |
| Presentación oral del avance | ma 22-sep | Por armar |
| Informe de avance (25%) | vi 25-sep | Por escribir. Entra la regresión `diferencia_s ~ vueltas_extra` |

## Los resultados hasta ahora

- El factor **no es constante**: va de 1,0145 (100 mariposa femenino) a 1,0521
  (200 espalda masculino). El orden de estilos —mariposa < libre < combinado < pecho
  < espalda— se repite idéntico en ambos sexos.
- **Los hombres se benefician más de la piscina corta que las mujeres en las 12
  pruebas comparables**, entre 0,6 y 1,2 puntos porcentuales, significativo en todas.
  Contradice a Iglesias García et al. (2025).
- La equivalencia implícita en las marcas mínimas **captura la tendencia**
  (correlación 0,767) pero se desvía en un subconjunto de pruebas: hasta 3,66 s en
  400 combinado femenino, y 13 pruebas salen más baratas en 25 m contra 11 en 50 m.
- El efecto del nivel del nadador sobre el factor es un **artefacto de selección**:
  definir "élite" por uno de los dos tiempos mueve la mediana casi un punto
  porcentual sin cambiar ningún nadador.

## Cómo correr esto

El entorno se maneja con `uv` desde la raíz del proyecto (`~/diplomado-cdd`), no
activando el `.venv` a mano. Todos los comandos van desde ahí:

```
uv run python capstone/descargar.py --prueba     # verifica que la API responda
uv run python capstone/descarga_temporada.py --femenino              # baja la muestra de mujeres (unos minutos)
uv run python capstone/descarga_temporada.py --masculino              # baja la muestra de hombres (unos minutos)
uv run python capstone/factor_implicito_wa.py    # marcas mínimas vs. factor medido
uv run python capstone/formulacion.py            # regenera el PDF de la formulación
uv run python capstone/entrega_eda.py            # regenera el PDF con el link al repo
```

El notebook se abre en VS Code eligiendo el kernel `.venv`. Requiere **scipy**
(`uv add scipy`); `formulacion.py` requiere **reportlab** (`uv add reportlab`).

## Los datos no están en el repositorio

Los términos de uso de World Aquatics prohíben redistribuir los datos crudos, así que
`datos/nados.csv`, `datos/pares_lcm_scm.csv` y `datos/cache/` están en `.gitignore`.
Se regeneran corriendo `descargar.py` y luego el notebook. Sí están versionados los
agregados: `factores_por_prueba.csv`, `comparacion_wa.csv`, `factor_por_nivel.csv` y
`metadatos.md`, que son estadísticas por prueba y no contienen marcas individuales.

## Qué hay en cada archivo

### Lo que se entrega, y el orden en que se ejecuta

| Orden | Archivo | Qué es |
|---|---|---|
| 1 | `descargar.py` | Baja los tiempos de la API de World Aquatics: 48 consultas, con caché y pausa entre peticiones → `datos/nados.csv` (no versionado) |
| 2 | `factor_implicito_wa.py` | Transcribe las marcas mínimas de Beijing 2026, calcula el factor implícito de la federación y su brecha contra el medido → `datos/comparacion_wa.csv` |
| 3 | **`03_eda_capstone.ipynb`** | **La entrega del martes 15-sep.** 69 celdas, una sección por criterio de la rúbrica. Lee los dos archivos anteriores y calcula todo lo demás |

El notebook no importa ningún otro `.py` de esta carpeta.

### Los datos versionados

| Archivo | Qué es |
|---|---|
| `datos/comparacion_wa.csv` | Marcas mínimas oficiales, factor implícito y brecha, por prueba. Lo lee el notebook |
| `datos/factores_por_prueba.csv` | Factor mediano por prueba, con 5 decimales |
| `datos/factor_por_nivel.csv` | El chequeo del sesgo de selección, por nivel de marca |
| `datos/metadatos.md` | Diccionario de las 25 variables del archivo crudo |

### Respaldo de lo que se afirma en el texto

| Archivo | Qué es |
|---|---|
| `nivel_y_factor.py` | El chequeo del sesgo de selección de la sección 3.2, con una segunda definición de nivel (por marca mínima en vez de percentil) → `datos/factor_por_nivel.csv` |
| `metadatos.py` | Genera el diccionario de las 25 variables → `datos/metadatos.md` |
| `probar_paginacion.py` | Sonda: cómo pedirle a la API más de 1.000 filas. Documenta que `page` se ignora y que `pageSize` topa en 5.000 |
| `probar_profundidad.py` | Sonda: cuántos nadadores distintos hay a cada profundidad del ranking. Es la que justifica usar `BEST_TIMES` |

### Entregas anteriores y material de trabajo

| Archivo | Qué es |
|---|---|
| `Entrega_EDA_Leiva_Fuentes.pdf` | El PDF con el link a este repositorio, que es lo que se sube al aula virtual el martes 15 |
| `entrega_eda.py` | Genera ese PDF con reportlab. **El texto se edita acá, no en el PDF** |
| `Formulacion_Capstone_Leiva_Fuentes.pdf` | La entrega del 7-sep. 3 páginas |
| `formulacion.py` | Genera ese PDF con reportlab. **El texto se edita acá, no en el PDF** |
| `Presentacion_idea_Capstone.pptx` | Las 3 láminas del 3-sep, ya presentadas |
| `Guion_presentacion_Capstone.pdf` | El guion de esa presentación |
| `Capstone_natacion_avance.pdf` | Borrador del 2-sep, previo a la formulación. Se conserva por historia |
| `figuras_eda/` | Las 5 figuras del EDA. Son las salidas inline del notebook, no hay `savefig` |
| `grafico_comparacion.py`, `figura_comparacion.png` | La figura de la presentación del 3-sep: exigencia oficial contra factor medido |
| `grafico_dispersion.py`, `figura_dispersion.png` | La otra figura de esa presentación: boxplot del factor por estilo |
| `01_exploracion.ipynb` | La exploración original. El EDA la reemplaza como entregable |
| `02_explorando.ipynb` | Cuaderno didáctico de pandas, no es entregable |

## Dos cuidados al editar

1. **El PDF no se edita, se genera.** Cualquier cambio hecho sobre el PDF se pierde
   la próxima vez que corra `formulacion.py`. El texto vive en los strings del script.
   Nada de subíndices Unicode (t₅₀): Helvetica los dibuja como cuadrados negros.
2. **Al re-ejecutar el notebook**, no usar el backend `Agg` de matplotlib: borra las
   imágenes inline del `.ipynb`. Y después de re-ejecutarlo hay que volver a extraer
   los PNG de `figuras_eda/` desde las salidas, o quedan desfasados.
