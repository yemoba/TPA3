import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# Función para consultar la API
def InfoApi(ind, fech='2024'):
    url = f'https://mindicador.cl/api/{ind}/{fech}'
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Error al consultar la API. Verifique la conexión o los parámetros.")
        return None
    return response.json().get('serie', [])

# Título de la aplicación
st.title("Visualizador de Indicadores Económicos")
st.write("Esta herramienta permite consultar y analizar indicadores económicos clave de Chile (UF, IPC, UTM) durante un año específico.")

# Configuración de la barra lateral
st.sidebar.header("Configuración de consulta")
indicador = st.sidebar.selectbox(
    "Seleccione el indicador económico:",
    ['uf', 'ipc', 'utm'],
    help="Seleccione un indicador para consultar sus datos."
)
anio = st.sidebar.radio("Seleccione el año:", ['2021', '2022', '2023', '2024'])

# Botón para iniciar la consulta
if st.sidebar.button("Consultar Indicador"):
    with st.spinner("Consultando datos..."):
        datos = InfoApi(indicador, anio)

    if datos:
        # Procesamiento de datos
        df = pd.DataFrame(datos)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df.set_index('fecha', inplace=True)

        # Mostrar un resumen de los datos en una tabla
        st.subheader(f"Datos del indicador: {indicador.upper()} ({anio})")
        st.dataframe(df.head(10))  # Mostrar los primeros 10 registros

        # Cálculo de estadísticas descriptivas
        promedio = round(df['valor'].mean(), 2)
        maximo = round(df['valor'].max(), 2)
        minimo = round(df['valor'].min(), 2)

        # Mostrar métricas en cuadros separados
        col1, col2, col3 = st.columns(3)
        col1.metric("Promedio", promedio)
        col2.metric("Máximo", maximo)
        col3.metric("Mínimo", minimo)

        # Gráficos interactivos con Plotly

        # Gráfico de barras
        st.subheader("Gráfico de barras")
        fig_bar = go.Figure(data=[
            go.Bar(x=df.index, y=df['valor'], name="Valor")
        ])
        fig_bar.update_layout(
            title=f"Valores del indicador {indicador.upper()} ({anio})",
            xaxis_title="Fecha",
            yaxis_title="Valor",
        )
        st.plotly_chart(fig_bar)

        # Gráfico de líneas (Serie de tiempo)
        st.subheader("Gráfico lineal (Serie de tiempo)")
        fig_line = go.Figure(data=[
            go.Scatter(x=df.index, y=df['valor'], mode='lines+markers', name="Valor")
        ])
        fig_line.update_layout(
            title=f"Serie de tiempo del indicador {indicador.upper()} ({anio})",
            xaxis_title="Fecha",
            yaxis_title="Valor",
        )
        st.plotly_chart(fig_line)

        # Gráfico de torta
        st.subheader("Gráfico de torta (Distribución)")
        distribucion = df['valor'].value_counts().head(5)
        fig_pie = go.Figure(data=[
            go.Pie(labels=distribucion.index, values=distribucion.values, hole=0.3)
        ])
        fig_pie.update_layout(title="Distribución de valores más frecuentes")
        st.plotly_chart(fig_pie)
    else:
        st.warning("No se encontraron datos para los parámetros seleccionados.")





