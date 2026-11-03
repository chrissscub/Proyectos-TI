import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Proyectos TI",
    page_icon="📊",
    layout="wide"
)

archivo = "DASHBOARD Proyectos TI.xlsm"

# Leer usando la segunda fila como encabezado
df = pd.read_excel(
    archivo,
    sheet_name="Hoja1",
    header=1
)

st.title("📊 Dashboard Proyectos TI")

st.subheader("Vista previa de datos")

st.dataframe(df)

st.subheader("Columnas detectadas")

st.write(df.columns.tolist())
