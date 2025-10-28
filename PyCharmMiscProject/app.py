import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Dashboard de Libros",
    page_icon="📚",
    layout="wide"
)


@st.cache_data
def load_data(csv_path):
    if not os.path.exists(csv_path):
        st.error(f"Error: No se encontró el archivo '{csv_path}'.")
        st.error("Por favor, ejecuta primero el script 'scraper.py' para generar los datos.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()


df = load_data('books.csv')

st.title("📚 Dashboard de Libros (Books to Scrape)")
st.markdown("Dashboard interactivo para analizar los datos extraídos de la web 'Books to Scrape'.")

if df.empty:
    st.warning("No hay datos para mostrar.")
else:
    st.sidebar.header("Filtros Interactivos")

    ratings_disponibles = sorted(df['Rating'].unique())
    selected_ratings = st.sidebar.multiselect(
        'Filtrar por Calificación (Estrellas)',
        options=ratings_disponibles,
        default=ratings_disponibles
    )

    min_price = float(df['Precio'].min())
    max_price = float(df['Precio'].max())

    price_range = st.sidebar.slider(
        'Filtrar por Rango de Precios (£)',
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )

    if selected_ratings:
        df_filtrado = df[df['Rating'].isin(selected_ratings)]
    else:
        df_filtrado = df.copy()

    df_filtrado = df_filtrado[
        (df_filtrado['Precio'] >= price_range[0]) &
        (df_filtrado['Precio'] <= price_range[1])
        ]

    st.header("Resultados Filtrados")
    st.markdown(f"Mostrando **{len(df_filtrado)}** de **{len(df)}** libros.")

    st.dataframe(df_filtrado)

    st.markdown("---")

    st.header("Visualizaciones")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución de Calificaciones")
        rating_counts = df_filtrado['Rating'].value_counts().sort_index()
        st.bar_chart(rating_counts)

    with col2:
        st.subheader("Distribución de Precios")
        st.bar_chart(df_filtrado['Precio'].value_counts(bins=10).sort_index())