import streamlit as st
import pandas as pd
from api_client import obtener_usuarios_api
from database import (
    crear_tabla,
    guardar_usuarios,
    consultar_usuarios,
    buscar_usuario_por_nombre,
    eliminar_datos,
)

st.set_page_config(
    page_title="Proyecto API + SQLite + Streamlit",
    layout="wide"
)

st.title("Proyecto API + SQLite + Streamlit")
st.write("Asignatura: Computación en la Nube · UTH")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    ["Inicio", "Consumir API", "Ver base de datos", "Buscar usuario", "Eliminar datos"]
)

if menu == "Inicio":
    st.header("Inicio")
    st.write("""
    Esta aplicación simula una pequeña arquitectura cloud:
    - Consume una API pública (JSONPlaceholder /users).
    - Guarda los datos en una base de datos SQLite local.
    - Muestra la información en una interfaz web con Streamlit.
    """)
    st.info("Use el menú lateral para navegar entre los módulos.")

elif menu == "Consumir API":
    st.header("Consumir API y guardar en SQLite")

    if st.button("Obtener usuarios desde la API y guardar"):
        usuarios = obtener_usuarios_api()

        if usuarios:
            guardar_usuarios(usuarios)
            st.success("Usuarios obtenidos de la API y guardados en SQLite correctamente.")
            df = pd.DataFrame(usuarios)
            st.subheader("Datos crudos desde la API (JSON → tabla)")
            st.dataframe(df)
        else:
            st.error("No se pudieron obtener datos desde la API.")

elif menu == "Ver base de datos":
    st.header("Ver base de datos (SQLite)")

    crear_tabla()
    df = consultar_usuarios()

    if df.empty:
        st.warning("La tabla 'usuarios' está vacía. Primero consuma la API y guarde los datos.")
    else:
        st.subheader("Tabla de usuarios almacenados en SQLite")
        st.dataframe(df)

        st.subheader("Usuarios por ciudad")
        if "ciudad" in df.columns:
            resumen = df.groupby("ciudad")["id"].count().reset_index()
            resumen.columns = ["Ciudad", "Cantidad de usuarios"]
            st.bar_chart(resumen.set_index("Ciudad"))
        else:
            st.info("No se encontró la columna 'ciudad' en la tabla.")

elif menu == "Buscar usuario":
    st.header("Buscar usuario por nombre")

    nombre = st.text_input("Ingrese parte del nombre a buscar")

    if st.button("Buscar"):
        if nombre.strip() == "":
            st.warning("Escriba al menos un carácter para buscar.")
        else:
            resultados = buscar_usuario_por_nombre(nombre)
            if resultados.empty:
                st.info("No se encontraron usuarios con ese criterio.")
            else:
                st.subheader("Resultados de la búsqueda")
                st.dataframe(resultados)

elif menu == "Eliminar datos":
    st.header("Eliminar todos los datos de la tabla 'usuarios'")

    st.warning("Esta acción borrará todos los registros almacenados en SQLite.")

    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Todos los datos han sido eliminados de la tabla 'usuarios'.")
