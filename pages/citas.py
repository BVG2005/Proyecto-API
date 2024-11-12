import streamlit as st
import requests
import pandas as pd

def get_citas():
    try:
        response = requests.get("http://127.0.0.1:8000/citas/?skip=0&limit=100")
        if response.status_code == 200:
            citas = response.json()
            # Modificar el formato de citas para incluir los nuevos campos
            for cita in citas:
                cita['motivo'] = cita.get('motivo', 'Sin motivo')  # Cambiar 'descripcion' a 'motivo'
            return citas
        else:
            st.error("Error al obtener los datos de citas")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def get_mascotas():
    try:
        response = requests.get("http://127.0.0.1:8000/mascotas/?skip=0&limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

def main():
    st.title("Listado de Citas")
    
    # Obtener los datos de citas, clientes y mascotas
    citas = get_citas()
    mascotas = get_mascotas()  # Asegúrate de obtener la lista de mascotas
    
    if citas and mascotas:  # Asegúrate de que todas las listas tengan datos
        # Crear un diccionario de id_mascota -> nombre_mascota
        mascotas_dict = {
            mascota['id']: mascota['nombre']
            for mascota in mascotas  # Ahora 'mascotas' está definido
        }
        
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(citas)
        
        # Reemplazar mascota_id con el nombre de la mascota
        df['mascota'] = df['mascota_id'].map(mascotas_dict)  # Cambiar 'cliente' por 'mascota'
        
        # Asegurarse de que 'motivo' esté presente antes de reordenar
        if 'motivo' in df.columns:
            df = df[['id', 'fecha', 'mascota', 'motivo', 'hora']]  # Cambiar 'descripcion' a 'motivo'
        else:
            st.warning("La columna 'motivo' no está presente en los datos de citas.")
            df = df[['id', 'fecha', 'mascota']]  # Ajustar las columnas según lo disponible
        
        # Mostrar los datos en una tabla
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "fecha": "Fecha",
                "mascota": "Mascota",
                "motivo": "Motivo",
                "hora": "Hora"
            },
            hide_index=True
        )
    else:
        st.warning("No hay citas para mostrar")

if __name__ == "__main__":
    main() 