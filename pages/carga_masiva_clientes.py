import streamlit as st
import pandas as pd
import requests
import io

st.title("Carga Masiva de Clientes")

# Widget para subir archivo
archivo_csv = st.file_uploader("Selecciona el archivo CSV", type=['csv'])

if archivo_csv is not None:
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv)
        
        # Verificar que el CSV tenga las columnas requeridas
        columnas_requeridas = ['nombre', 'apellido', 'telefono', 'email']
        if not all(columna in df.columns for columna in columnas_requeridas):
            st.error("El archivo CSV debe contener las columnas: nombre, apellido, telefono, email")
        else:
            # Mostrar preview de los datos
            st.write("Preview de los datos:")
            st.dataframe(df.head())
            
            if st.button("Cargar Clientes"):
                # Preparar datos para la API
                clientes = []
                for _, row in df.iterrows():
                    cliente = {
                        "nombre": str(row['nombre']),
                        "apellido": str(row['apellido']),
                        "telefono": str(row['telefono']),
                        "email": str(row['email'])
                    }
                    clientes.append(cliente)
                
                payload = {"clientes": clientes}
                
                # Realizar la petición POST
                try:
                    response = requests.post(
                        "http://localhost:8000/clientes/bulk/",
                        json=payload
                    )
                    
                    if response.status_code in [200, 201]:
                        # Intentar parsear la respuesta JSON
                        clientes_creados = response.json()
                        st.success(f"Se cargaron {len(clientes_creados)} clientes exitosamente!")
                        
                        # Mostrar detalles de los clientes creados
                        st.write("Clientes creados:")
                        df_creados = pd.DataFrame(clientes_creados)
                        st.dataframe(df_creados)
                    else:
                        st.error(f"Error al cargar los clientes. Código de estado: {response.status_code}")
                        st.error(f"Detalle del error: {response.text}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {str(e)}")
    
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}") 