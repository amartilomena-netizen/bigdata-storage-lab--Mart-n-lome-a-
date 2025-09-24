import pandas as pd
from pandas import DataFrame
from typing import Dict

def normalize_columns(df: DataFrame, mapping: Dict[str, str]) -> DataFrame:
    """
    Normaliza columnas de un DataFrame según un mapping origen→canónico.
    - Renombra columnas (date, partner, amount).
    - Convierte 'date' a datetime (ISO).
    - Limpia 'partner' (espacios).
    - Normaliza 'amount' (elimina símbolos €, reemplaza comas europeas).
    """
    # Renombrar columnas
    df = df.rename(columns=mapping)

    # Normalizar fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%Y-%m-%d")

    # Limpiar partner
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip()

    # Normalizar amount
    if "amount" in df.columns:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df


def to_silver(bronze: DataFrame) -> DataFrame:
    """
    Agrega datos de la capa bronze a nivel partner y mes.
    - Crea columna 'month' (primer día del mes como timestamp).
    - Suma 'amount' por partner y month.
    """
    df = bronze.copy()

    if "date" not in df.columns or "amount" not in df.columns or "partner" not in df.columns:
        raise ValueError("El DataFrame bronze debe contener columnas: date, partner, amount")

    # Derivar columna mes
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Agregar por partner + month
    silver = (
        df.groupby(["partner", "month"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_amount"})
    )

    return silver
