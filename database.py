import streamlit as st

import pandas as pd

from api_client import obtener_usuarios_api

from database import crear_tabla, guardar_usuarios, consultar_usuarios, eliminar_datos

st.set_page_config(

    page_title="API + SQLite + Streamlit",

    layout="wide"

)

crear_tabla()

st.title("Proyecto Cloud: API + SQLite + Streamlit")

st.write("Aplicación que consume una API pública, guarda los datos en SQLite y los muestra en una tabla.")

menu = st.sidebar.selectbox(

    "Seleccione una opción",

    [

        "Inicio",

        "Consumir API",

        "Ver base de datos",

        "Buscar usuario",

        "Eliminar datos"

    ]

)

if menu == "Inicio":

    st.header("Panel principal")

    st.write("""

    Esta aplicación simula una arquitectura básica de computación en la nube:

    - API externa como fuente de datos.

    - Streamlit como interfaz web.

    - SQLite como base de datos.

    - GitHub como repositorio.

    - Streamlit Cloud como plataforma de despliegue.

    """)

    st.info("Use el menú lateral para interactuar con la aplicación.")

elif menu == "Consumir API":

    st.header("Consumir API pública")

    st.write("API utilizada:")

    st.code("https://jsonplaceholder.typicode.com/users")

    if st.button("Obtener datos desde API"):

        usuarios = obtener_usuarios_api()

        if usuarios:

            guardar_usuarios(usuarios)

            st.success("Datos obtenidos y guardados correctamente en SQLite.")

            st.json(usuarios[0])

        else:

            st.error("No se pudieron obtener datos desde la API.")