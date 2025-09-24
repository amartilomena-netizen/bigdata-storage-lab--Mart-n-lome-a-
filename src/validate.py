import pandas as pd
from pandas import DataFrame
from typing import List

def basic_checks(df: DataFrame) -> List[str]:
    """
    Realiza validaciones básicas sobre un DataFrame canónico.
    Retorna lista de errores encontrados.
    - Columnas requeridas: date, partner, amount.
    - 'date' debe ser datetime.
    - 'amount' debe ser numérico y >= 0.
    """
    errors: List[str] = []

    # Verificar columnas canónicas
    required_cols = {"date", "partner", "amount"}
    missing = required_cols - set(df.columns)
    if missing:
        errors.append(f"Faltan columnas: {', '.join(missing)}")

    # Verificar tipos y valores si columnas existen
    if "date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df["date"]):
            errors.append("Columna 'date' no es datetime")

    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("Columna 'amount' no es numérica")
        elif (df["amount"] < 0).any():
            errors.append("Existen valores negativos en 'amount'")

    return errors
