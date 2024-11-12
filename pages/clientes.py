import streamlit as st
import requests
import pandas as pd

def get_clientes():
    try:
        response = requests.get("http://127.0.0.1:8000/clientes/?skip=0&limit=100")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener los datos de clientes")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

# Función para eliminar un cliente
def delete_cliente(cliente_id):
    try:
        response = requests.delete(f"http://127.0.0.1:8000/clientes/{cliente_id}")
        # Considerar 200 y 204 como respuestas exitosas
        if response.status_code in [200, 204]:
            return True
        else:
            st.error(f"Error al eliminar el cliente. Código de estado: {response.status_code}, Detalle: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

# Función para actualizar un cliente
def update_cliente(cliente_id, cliente_data):
    try:
        response = requests.put(f"http://127.0.0.1:8000/clientes/{cliente_id}", json=cliente_data)
        if response.status_code in [200, 204]:
            return True
        else:
            st.error(f"Error al actualizar el cliente. Código de estado: {response.status_code}, Detalle: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

def main():
    st.title("Listado de Clientes")
    
    # Obtener los datos de clientes
    clientes = get_clientes()
    
    if clientes:
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(clientes)
        
        # Mostrar los datos en una tabla
        st.dataframe(
            df,
            column_config={
                "nombre": "Nombre",
                "apellido": "Apellido",
                "telefono": "Teléfono",
                "email": "Correo Electrónico",
                "id": "ID"
            },
            hide_index=True
        )

        # Opción para actualizar un cliente existente
        cliente_id = st.number_input("ID del Cliente a Actualizar", min_value=1, step=1)
        nombre = st.text_input("Nuevo Nombre")
        apellido = st.text_input("Nuevo Apellido")
        telefono = st.text_input("Nuevo Teléfono")
        email = st.text_input("Nuevo Correo Electrónico")

        if st.button("Actualizar Cliente"):
            cliente_data = {
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono,
                "email": email
            }
            if update_cliente(cliente_id, cliente_data):
                st.success("Cliente actualizado exitosamente!")
            else:
                st.error("Error al actualizar el cliente.")

        # Opción para eliminar un cliente
        cliente_id_delete = st.number_input("ID del Cliente a Eliminar", min_value=1, step=1)
        if st.button("Eliminar Cliente"):
            if delete_cliente(cliente_id_delete):
                st.success("Cliente eliminado exitosamente!")
            else:
                st.error("Error al eliminar el cliente.")
    else:
        st.warning("No hay clientes para mostrar")

if __name__ == "__main__":
    main() 