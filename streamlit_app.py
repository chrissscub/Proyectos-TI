import streamlit as st
import pandas as pd

archivo = "DASHBOARD Proyectos TI.xlsm"

st.title("Dashboard Proyectos TI")

hoja1 = pd.read_excel(archivo, sheet_name="Hoja1")
proyectos = pd.read_excel(archivo, sheet_name="Proyectos")

st.header("Hoja1")
st.dataframe(hoja1.head(10))

st.write("Columnas Hoja1")
st.write(list(hoja1.columns))

st.header("Proyectos")
st.dataframe(proyectos.head(10))

st.write("Columnas Proyectos")
st.write(list(proyectos.columns))
