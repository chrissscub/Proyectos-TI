import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Proyectos TI",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# CARGA DATOS
# -------------------------

archivo = "DASHBOARD Proyectos TI.xlsm"

df = pd.read_excel(
    archivo,
    sheet_name="Hoja1",
    header=1
)

# Limpiar columnas basura
df = df.loc[:, ~df.columns.astype(str).str.contains("Unnamed")]

# Convertir avance
df["% Avance"] = pd.to_numeric(
    df["% Avance"],
    errors="coerce"
).fillna(0)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("Filtros")

estado = st.sidebar.multiselect(
    "Estado",
    sorted(df["Estado"].dropna().unique()),
    default=sorted(df["Estado"].dropna().unique())
)

area = st.sidebar.multiselect(
    "Área",
    sorted(df["Área solicitante"].dropna().unique()),
    default=sorted(df["Área solicitante"].dropna().unique())
)

df_filtrado = df[
    (df["Estado"].isin(estado))
    &
    (df["Área solicitante"].isin(area))
]

# -------------------------
# KPIS
# -------------------------

st.title("📊 Dashboard Proyectos TI")

total = len(df_filtrado)

finalizados = len(
    df_filtrado[
        df_filtrado["Estado"] == "Fin"
    ]
)

proceso = len(
    df_filtrado[
        df_filtrado["Estado"] == "En proceso"
    ]
)

no_iniciado = len(
    df_filtrado[
        df_filtrado["Estado"] == "No iniciado"
    ]
)

avance_promedio = round(
    df_filtrado["% Avance"].mean() * 100,
    1
)

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Total", total)
c2.metric("Finalizados", finalizados)
c3.metric("En Proceso", proceso)
c4.metric("No Iniciados", no_iniciado)
c5.metric("Avance Promedio", f"{avance_promedio}%")

st.divider()

# -------------------------
# GRAFICOS
# -------------------------

col1,col2 = st.columns(2)

with col1:

    estado_chart = (
        df_filtrado
        .groupby("Estado")
        .size()
        .reset_index(name="Cantidad")
    )

    fig_estado = px.pie(
        estado_chart,
        names="Estado",
        values="Cantidad",
        title="Estado de proyectos"
    )

    st.plotly_chart(
        fig_estado,
        use_container_width=True
    )

with col2:

    area_chart = (
        df_filtrado
        .groupby("Área solicitante")
        .size()
        .reset_index(name="Cantidad")
    )

    fig_area = px.bar(
        area_chart,
        x="Área solicitante",
        y="Cantidad",
        title="Proyectos por área",
        color="Cantidad"
    )

    st.plotly_chart(
        fig_area,
        use_container_width=True
    )

# -------------------------
# TOP PROYECTOS
# -------------------------

st.subheader("🏆 Avance por Proyecto")

ranking = df_filtrado.sort_values(
    "% Avance",
    ascending=True
)

fig_avance = px.bar(
    ranking,
    x="% Avance",
    y="Nombre Proyecto",
    orientation="h",
    color="% Avance",
    color_continuous_scale="Blues"
)

st.plotly_chart(
    fig_avance,
    use_container_width=True
)

# -------------------------
# SEMAFORO
# -------------------------

st.subheader("🚦 Estado General")

def semaforo(x):

    if x >= 0.8:
        return "🟢"

    elif x >= 0.3:
        return "🟡"

    else:
        return "🔴"

tabla = df_filtrado[
    [
        "Nombre Proyecto",
        "Área solicitante",
        "Estado",
        "% Avance"
    ]
].copy()

tabla["Semáforo"] = tabla["% Avance"].apply(semaforo)

st.dataframe(
    tabla,
    use_container_width=True
)

# -------------------------
# TABLA DETALLE
# -------------------------

st.subheader("📋 Detalle Completo")

st.dataframe(
    df_filtrado,
    use_container_width=True
)
