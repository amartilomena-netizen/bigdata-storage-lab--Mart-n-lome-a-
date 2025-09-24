import pandas as pd
from pandas import DataFrame
from typing import List
from datetime import datetime, timezone

def tag_lineage(df: DataFrame, source_name: str) -> DataFrame:
    """
    Añade metadatos de linaje al DataFrame.
    - source_file: nombre del archivo origen.
    - ingested_at: timestamp UTC ISO.
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[DataFrame]) -> DataFrame:
    """
    Concatena múltiples DataFrames en un esquema estándar:
    [date, partner, amount, source_file, ingested_at].
    """
    if not frames:
        return pd.DataFrame(columns=["date", "partner", "amount", "source_file", "ingested_at"])

    bronze = pd.concat(frames, ignore_index=True)

    # Asegurar columnas en orden esperado
    expected_cols = ["date", "partner", "amount", "source_file", "ingested_at"]
    bronze = bronze.reindex(columns=expected_cols)

    return bronze
