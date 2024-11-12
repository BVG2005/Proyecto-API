import streamlit as st
import requests
import pandas as pd

def get_medicamentos():
    try:
        response = requests.get("http://127.0.0.1:8000/medicamentos/?skip=0&limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener los datos de medicamentos")
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
    st.title("Listado de Medicamentos")
    
    # Obtener los datos de medicamentos
    medicamentos = get_medicamentos()
    
    if medicamentos:
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(medicamentos)
        
        # Reordenar y mostrar las columnas
        df = df[['nombre', 'descripcion', 'stock', 'precio']]  # Mostrar nombre, descripción, stock y precio
        
        # Mostrar los datos en una tabla
        st.dataframe(
            df,
            column_config={
                "nombre": "Nombre",
                "descripcion": "Descripción",
                "stock": "Stock",
                "precio": "Precio"
            },
            hide_index=True
        )
    else:
        st.warning("No hay medicamentos para mostrar")

if __name__ == "__main__":
    main() 