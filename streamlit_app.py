# Placeholder de la aplicación Streamlit
import streamlit as st
import pandas as pd
from io import BytesIO

# Importar funciones locales
from src.transform import normalize_columns, to_silver
from src.validate import basic_checks
from src.ingest import tag_lineage, concat_bronze

st.set_page_config(
    page_title="Big Data Storage Lab",
    layout="wide"
)

st.title("📊 Big Data Storage Lab")
st.markdown("De CSVs heterogéneos a un almacén analítico confiable.")

# --- Configuración en barra lateral ---
st.sidebar.header("Configuración de columnas origen")
col_date = st.sidebar.text_input("Columna origen para fecha", value="date")
col_partner = st.sidebar.text_input("Columna origen para partner", value="partner")
col_amount = st.sidebar.text_input("Columna origen para amount", value="amount")

uploaded_files = st.file_uploader(
    "Sube uno o varios archivos CSV",
    type=["csv"],
    accept_multiple_files=True
)

# --- Procesamiento ---
bronze_frames = []

if uploaded_files:
    for file in uploaded_files:
        try:
            # Intentar UTF-8 y fallback a latin-1
            try:
                df = pd.read_csv(file, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding="latin-1")

            # Mapping origen → canónico
            mapping = {
                col_date: "date",
                col_partner: "partner",
                col_amount: "amount",
            }

            df = normalize_columns(df, mapping)
            df = tag_lineage(df, source_name=file.name)
            bronze_frames.append(df)

        except Exception as e:
            st.error(f"Error procesando {file.name}: {e}")

# --- Mostrar resultados ---
if bronze_frames:
    bronze = concat_bronze(bronze_frames)

    st.subheader("📂 Datos Bronze (unificados)")
    st.dataframe(bronze.head(50))

    # Validaciones
    st.subheader("🔎 Validaciones")
    errors = basic_checks(bronze)
    if errors:
        st.error("Se encontraron errores:")
        for err in errors:
            st.write(f"- {err}")
    else:
        st.success("Validaciones OK ✅")

        # Silver
        silver = to_silver(bronze)

        st.subheader("🥈 Datos Silver (partner × mes)")
        st.dataframe(silver.head(50))

        # KPIs simples
        st.markdown("### KPIs")
        total_amount = silver["total_amount"].sum()
        partners_count = silver["partner"].nunique()
        months_count = silver["month"].nunique()

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Amount (€)", f"{total_amount:,.2f}")
        kpi2.metric("N° Partners", partners_count)
        kpi3.metric("N° Meses", months_count)

        # Bar chart
        st.markdown("### Evolución mensual (total_amount)")
        chart_data = silver.groupby("month")["total_amount"].sum().reset_index()
        st.bar_chart(chart_data, x="month", y="total_amount")

        # Botones descarga
        st.subheader("⬇️ Descargas")
        def to_csv_download(df: pd.DataFrame) -> BytesIO:
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return buffer

        bronze_buf = to_csv_download(bronze)
        silver_buf = to_csv_download(silver)

        st.download_button(
            "Descargar Bronze CSV",
            data=bronze_buf,
            file_name="bronze.csv",
            mime="text/csv"
        )
        st.download_button(
            "Descargar Silver CSV",
            data=silver_buf,
            file_name="silver.csv",
            mime="text/csv"
        )

# Punto de entrada: visualizar KPIs calculados desde la capa silver

import streamlit as st

st.title("Big Data Storage Lab - <apellido>")
st.write("Dashboard inicial en construcción...")
