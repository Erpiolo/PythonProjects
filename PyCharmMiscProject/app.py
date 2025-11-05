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
    return pd.read_csv(csv_path)

st.title("Dashboard de Libros (Books to Scrape)")
st.markdown("Dashboard interactivo para analizar los datos extraídos de 'Books to Scrape'.")

df = load_data('books.csv')

if df.empty:
    st.warning("No hay datos para mostrar.")
else:

    st.sidebar.header("Filtros Interactivos")
    min_price = float(df['Precio'].min())
    max_price = float(df['Precio'].max())
    price_range = st.sidebar.slider(
        'Filtrar por Rango de Precios (£)',
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )


    df_filtrado = df[
        (df['Precio'] >= price_range[0]) &
        (df['Precio'] <= price_range[1])
    ]
    st.header("Resultados Filtrados")
    st.markdown(f"Mostrando **{len(df_filtrado)}** de **{len(df)}** libros.")
    st.dataframe(df_filtrado)


    st.header("Visualizaciones")
    st.subheader("Distribución de Calificaciones")
    rating_counts = df_filtrado['Rating'].value_counts().sort_index()
    st.bar_chart(rating_counts)



    st.subheader("Distribución de Precios")
    price_dist = df_filtrado['Precio'].value_counts(bins=6).sort_index()
    price_dist.index = price_dist.index.astype(str)
    st.bar_chart(price_dist)
