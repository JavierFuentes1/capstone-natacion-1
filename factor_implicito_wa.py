"""
Factor de conversión implícito en las marcas mínimas de World Aquatics.

World Aquatics no publica un factor de conversión entre piscina de 25 m y de 50 m.
Publica dos tablas de marcas mínimas, una por tipo de piscina, y acepta tiempos
hechos en cualquiera de las dos ("Entry times will only be accepted if they have
been achieved at a World Aquatics-approved qualification event, either in a 25m
pool or a 50m pool").

Si ambas exigencias dan derecho al mismo cupo, la razón entre ellas es la
equivalencia que la federación está aplicando de hecho:

        factor_implicito = tiempo_exigido_en_50m / tiempo_exigido_en_25m

Este script calcula ese factor y lo compara con el que medimos nosotros a partir
de 30.257 nadadores que compitieron en ambas piscinas durante la temporada 2024.

FUENTE de las marcas mínimas (transcritas a mano el 2-sep-2026):
  "Qualification - World Aquatics Swimming Championships (25m) Beijing 2026"
  https://resources.fina.org/fina/document/2026/02/16/2bee1e7b-bb50-4d97-855a-650661073eb0/Qualification-World-Aquatics-Swiming-Championships-25m-Beijing-2026.pdf
  Período de clasificación: 27 julio 2025 - 15 noviembre 2026.

  >>> VERIFICAR contra el PDF antes de citar estos números en un entregable. <<<

Salida: datos/comparacion_wa.csv
"""

import pandas as pd
from pathlib import Path

AQUI = Path(__file__).parent
DATOS = AQUI / "datos"

# ---------------------------------------------------------------------------
# Marcas mínimas Beijing 2026, tal como aparecen en el PDF.
# Formato: (sexo, estilo, distancia): (25m_A, 25m_B, 50m_A, 50m_B)
# ---------------------------------------------------------------------------
MARCAS = {
    ("M", "FREESTYLE",    50):  ("21.19",   "21.93",   "22.05",   "22.82"),
    ("M", "FREESTYLE",   100):  ("46.89",   "48.53",   "48.34",   "50.03"),
    ("M", "FREESTYLE",   200):  ("1:43.48", "1:47.10", "1:46.70", "1:50.43"),
    ("M", "FREESTYLE",   400):  ("3:42.18", "3:49.96", "3:48.15", "3:56.14"),
    ("M", "BACKSTROKE",  100):  ("50.81",   "52.59",   "53.94",   "55.83"),
    ("M", "BACKSTROKE",  200):  ("1:52.11", "1:56.03", "1:58.07", "2:02.20"),
    ("M", "BREASTSTROKE",100):  ("57.38",   "59.39",   "59.75",   "1:01.84"),
    ("M", "BREASTSTROKE",200):  ("2:06.23", "2:10.65", "2:10.32", "2:14.88"),
    ("M", "BUTTERFLY",   100):  ("50.15",   "51.91",   "51.77",   "53.58"),
    ("M", "BUTTERFLY",   200):  ("1:53.19", "1:57.15", "1:56.51", "2:00.59"),
    ("M", "MEDLEY",      200):  ("1:55.25", "1:59.28", "1:59.05", "2:03.22"),
    ("M", "MEDLEY",      400):  ("4:08.87", "4:17.58", "4:17.48", "4:26.49"),

    ("F", "FREESTYLE",    50):  ("24.33",   "25.18",   "24.86",   "25.73"),
    ("F", "FREESTYLE",   100):  ("53.02",   "54.88",   "54.25",   "56.15"),
    ("F", "FREESTYLE",   200):  ("1:55.60", "1:59.65", "1:58.23", "2:02.37"),
    ("F", "FREESTYLE",   400):  ("4:06.27", "4:14.89", "4:10.23", "4:18.99"),
    ("F", "BACKSTROKE",  100):  ("57.52",   "59.53",   "1:00.46", "1:02.58"),
    ("F", "BACKSTROKE",  200):  ("2:05.54", "2:09.93", "2:11.08", "2:15.67"),
    ("F", "BREASTSTROKE",100):  ("1:04.97", "1:07.24", "1:06.87", "1:09.21"),
    ("F", "BREASTSTROKE",200):  ("2:21.91", "2:26.88", "2:25.91", "2:31.02"),
    ("F", "BUTTERFLY",   100):  ("57.40",   "59.41",   "58.33",   "1:00.37"),
    ("F", "BUTTERFLY",   200):  ("2:08.85", "2:13.36", "2:09.21", "2:13.73"),
    ("F", "MEDLEY",      200):  ("2:09.37", "2:13.90", "2:12.83", "2:17.48"),
    ("F", "MEDLEY",      400):  ("4:37.46", "4:47.17", "4:43.06", "4:52.97"),
}

NOMBRE = {"FREESTYLE": "Libre", "BACKSTROKE": "Espalda", "BREASTSTROKE": "Pecho",
          "BUTTERFLY": "Mariposa", "MEDLEY": "Combinado"}


def a_segundos(t: str) -> float:
    """'4:37.46' -> 277.46 ; '21.19' -> 21.19"""
    if ":" in t:
        minutos, resto = t.split(":")
        return int(minutos) * 60 + float(resto)
    return float(t)


def main():
    # --- 1. Las marcas mínimas, pasadas a segundos --------------------------
    filas = []
    for (sexo, estilo, dist), (sc_a, sc_b, lc_a, lc_b) in MARCAS.items():
        filas.append({
            "sexo": sexo, "estilo": estilo, "distancia": dist,
            "qt25_A_s": a_segundos(sc_a), "qt50_A_s": a_segundos(lc_a),
            "qt25_B_s": a_segundos(sc_b), "qt50_B_s": a_segundos(lc_b),
        })
    wa = pd.DataFrame(filas)

    # El factor implícito: cuánto más lento exige la federación en piscina larga
    wa["factor_wa_A"] = wa["qt50_A_s"] / wa["qt25_A_s"]
    wa["factor_wa_B"] = wa["qt50_B_s"] / wa["qt25_B_s"]

    # --- 2. Nuestro factor medido ------------------------------------------
    # La mediana se recalcula aqui desde los pares, a precision completa.
    # No se lee de factores_por_prueba.csv: ese archivo guardaba el factor
    # redondeado, y con 3 decimales el redondeo mueve la brecha hasta 0,1 s
    # (100 libre masculino pasaba de -0,02 a -0,04 s).
    pares = pd.read_csv(DATOS / "pares_lcm_scm.csv",
                        usecols=["sexo", "estilo", "distancia", "factor_tiempo_mediana"])

    pares = pares.rename(columns = {"factor_tiempo_mediana":"factor"})

    nuestro = (pares.groupby(["sexo", "estilo", "distancia"])["factor"]
                    .agg(n_pares="size", factor_real="median")
                    .reset_index())

    comp = wa.merge(nuestro, on=["sexo", "estilo", "distancia"], how="left",
                    validate="one_to_one", indicator=True)
    assert (comp["_merge"] == "both").all(), "Hay pruebas sin factor medido"
    comp = comp.drop(columns="_merge")

    # --- 3. La brecha, en segundos -----------------------------------------
    # Tomamos la marca exigida en 25 m y le aplicamos el factor REAL: ese sería
    # el tiempo equivalente en 50 m. La diferencia con lo que la federación pide
    # es cuánto se aparta la exigencia de la equivalencia observada.
    comp["qt50_equivalente_s"] = comp["qt25_A_s"] * comp["factor_real"]
    comp["brecha_s"] = comp["qt50_equivalente_s"] - comp["qt50_A_s"]
    comp["mas_facil_en"] = comp["brecha_s"].apply(
        lambda b: "25 m" if b > 0 else "50 m")

    comp["prueba"] = comp["distancia"].astype(str) + " " + comp["estilo"].map(NOMBRE)
    comp = comp.sort_values("brecha_s", ascending=False)

    salida = DATOS / "comparacion_wa.csv"
    comp.to_csv(salida, index=False)

    # --- 4. Mostrarlo ------------------------------------------------------
    print(f"Marcas mínimas Beijing 2026 (marca A) vs. factor medido en 2024\n")
    print(f"{'sx':3}{'prueba':15}{'QT25':>8}{'QT50':>8}"
          f"{'f.WA':>9}{'f.real':>8}{'n':>6}{'brecha':>8}  fácil")
    print("-" * 70)
    for _, f in comp.iterrows():
        print(f"{f.sexo:3}{f.prueba:15}{f.qt25_A_s:8.2f}{f.qt50_A_s:8.2f}"
              f"{f.factor_wa_A:9.4f}{f.factor_real:8.4f}{int(f.n_pares):6d}"
              f"{f.brecha_s:+8.2f}  {f.mas_facil_en.replace(' ','')}")

    print(f"\nRango del factor implícito de World Aquatics: "
          f"{comp.factor_wa_A.min():.4f} a {comp.factor_wa_A.max():.4f}")
    print(f"Rango del factor medido por nosotros:          "
          f"{comp.factor_real.min():.4f} a {comp.factor_real.max():.4f}")
    print(f"Brecha absoluta mediana: {comp.brecha_s.abs().median():.2f} s  |  "
          f"máxima: {comp.brecha_s.abs().max():.2f} s")
    print(f"Pruebas donde es más fácil clasificar en 25 m: "
          f"{(comp.brecha_s > 0).sum()} de {len(comp)}")
    print(f"\nCorrelación entre ambos factores: "
          f"{comp.factor_wa_A.corr(comp.factor_real):.3f}")
    print(f"\nGuardado en {salida}")

    # Chequeo de la advertencia 1: ¿la marca B da lo mismo que la A?
    dif_ab = (comp.factor_wa_A - comp.factor_wa_B).abs()
    print(f"Diferencia entre usar la marca A o la B: máximo {dif_ab.max():.4f} "
          f"(mediana {dif_ab.median():.4f})")


if __name__ == "__main__":
    main()
