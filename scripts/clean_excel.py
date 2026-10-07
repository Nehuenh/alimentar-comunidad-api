import pandas as pd

print("=== Simulando limpieza de Excel real Alimentar Comunidad ===")
print("Trabajo original RENACOM: 100% manual, sin IA disponible en area")

df = pd.read_csv("data/sample_anonimo.csv")
print(f"\nTotal registros sample: {len(df)}")

# 1. Detectar duplicados como hacias en RENACOM
duplicados = df[df.duplicated(subset=["provincia", "barrio_anonimo", "tipo_comedor", "capacidad_viandas"], keep=False)]
print(f"Duplicados detectados por multiples inscripciones/falla web: {len(duplicados)}")
print(duplicados[["id", "provincia", "barrio_anonimo"]])

# 2. Detectar inconsistencias ratio > 1000
inconsistentes = df[df["ratio"] > 1000]
print(f"\nRegistros con ratio viandas/voluntarios > 1000 (inconsistencia RENACOM): {len(inconsistentes)}")
print(inconsistentes[["id", "capacidad_viandas", "voluntarios", "ratio"]])

# 3. Limpiar
df_clean = df.drop_duplicates(subset=["provincia", "barrio_anonimo", "tipo_comedor", "capacidad_viandas"])
df_clean = df_clean[df_clean["ratio"] <= 1000]

print(f"\nRegistros limpios finales: {len(df_clean)}")
df_clean.to_csv("data/clean.csv", index=False)
print("Guardado en data/clean.csv")