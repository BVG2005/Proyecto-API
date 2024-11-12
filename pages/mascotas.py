import streamlit as st
import requests
import pandas as pd

def get_mascotas():
    try:
        response = requests.get("http://127.0.0.1:8000/mascotas/?skip=0&limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener los datos de mascotas")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def get_clientes():
    try:
        response = requests.get("http://127.0.0.1:8000/clientes/?skip=0&limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

def main():
    st.title("Listado de Mascotas")
    
    # Obtener los datos de mascotas y clientes
    mascotas = get_mascotas()
    clientes = get_clientes()
    
    if mascotas and clientes:
        # Crear un diccionario de id_cliente -> nombre_completo
        clientes_dict = {
            cliente['id']: f"{cliente['nombre']} {cliente['apellido']}"
            for cliente in clientes
        }
        
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(mascotas)
        
        # Verificar si 'cliente_id' está presente en el DataFrame
        if 'cliente_id' in df.columns:
            # Reemplazar cliente_id con el nombre del cliente
            df['propietario'] = df['cliente_id'].map(clientes_dict)
        else:
            st.warning("La columna 'cliente_id' no está presente en los datos de mascotas.")
            df['propietario'] = None  # O manejarlo de otra manera según tu lógica
        
        # Reordenar y mostrar las columnas
        df = df[['nombre', 'especie', 'raza', 'edad', 'propietario']]
        
        # Mostrar los datos en una tabla
        st.dataframe(
            df,
            column_config={
                "nombre": "Nombre Mascota",
                "especie": "Especie",
                "raza": "Raza",
                "edad": "Edad",
                "propietario": "Propietario"
            },
            hide_index=True
        )
    else:
        st.warning("No hay mascotas para mostrar")

if __name__ == "__main__":
    main() 