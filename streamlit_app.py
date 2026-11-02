import streamlit as st
import pandas as pd

st.title("Dashboard Proyectos TI")

archivo = "DASHBOARD Proyectos TI.xlsm"

try:
    xls = pd.ExcelFile(archivo)

    st.success("Archivo cargado correctamente")

    st.write("Hojas disponibles:")
    st.write(xls.sheet_names)

except Exception as e:
    st.error(f"Error: {e}")
