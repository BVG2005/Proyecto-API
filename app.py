import streamlit as st
from PIL import Image
import requests
import pandas as pd

# Función para obtener clientes
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

# Función para obtener mascotas
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

# Función para obtener un cliente por ID
def get_cliente(cliente_id):
    try:
        response = requests.get(f"http://127.0.0.1:8000/clientes/{cliente_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener los datos del cliente")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

# Función para actualizar un cliente
def update_cliente(cliente_id, cliente_data):
    try:
        response = requests.put(f"http://127.0.0.1:8000/clientes/{cliente_id}", json=cliente_data)
        return response.status_code in [200, 204]
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

# Función para eliminar un cliente
def delete_cliente(cliente_id):
    try:
        response = requests.delete(f"http://127.0.0.1:8000/clientes/{cliente_id}")
        if response.status_code in [200, 204]:
            return True
        else:
            st.error(f"Error al eliminar el cliente. Código de estado: {response.status_code}, Detalle: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

# Configuración de la página
st.set_page_config(layout="wide")

# Estilo CSS para el fondo y la presentación
st.markdown("""
    <style>
    body {
        background-color: #e0f7fa; /* Color de fondo azul claro */
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between; /* Cambiado a space-between para alinear el logo a la derecha */
        color: #0277bd; /* Color azul oscuro */
        margin-top: 20px;
        font-size: 2.5em;
    }
    .header img {
        margin-left: 10px; /* Espacio entre el título y el logo */
        width: 120px; /* Aumentado el tamaño del logo */
        border-radius: 10px; /* Añadido borde redondeado al logo */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Añadido sombra al logo */
    }
    .section {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    }
    .footer {
        text-align: center;
        color: #0277bd; /* Color azul oscuro */
        font-size: 16px;
        margin-top: 40px;
    }
    h3 {
        color: #4caf50; /* Color verde para los encabezados */
    }
    .service-list {
        list-style-type: none; /* Eliminar viñetas */
        padding: 0;
    }
    .service-list li {
        background: #f1f8e9; /* Fondo verde claro para los servicios */
        margin: 10px 0;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Imagen del logo
logo = Image.open("d:\Downloads\logo_sanmiguel.png")  

# Contenido principal
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("San Miguel Medicina Veterinaria")
st.image(logo, caption="", width=120)  

# Menú de navegación
opcion = st.sidebar.selectbox("Selecciona una opción", ["Inicio", "Agregar Cliente", "Agregar Mascota", "Agregar Cita", "Agregar Medicamento"])

# Sección de inicio
if opcion == "Inicio":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.write("""
    ### Bienvenidos a San Miguel Medicina Veterinaria
    En San Miguel, nos dedicamos a proporcionar el mejor cuidado y atención para tus mascotas. Nuestro equipo de profesionales está aquí para asegurarse de que tu amigo peludo reciba la atención que merece.
    
    #### Servicios que ofrecemos:
    <ul class="service-list">
        <li><strong>Consultas</strong>: Atención veterinaria general.</li>
        <li><strong>Vacunaciones</strong>: Protección para la salud de tus mascotas.</li>
        <li><strong>Cirugías</strong>: Procedimientos quirúrgicos realizados por expertos.</li>
        <li><strong>Otros servicios</strong>: Medicinas y accesorios para el bienestar de tus mascotas.</li>
    </ul>
    
    Contáctanos para más información o para agendar una cita.
    """, unsafe_allow_html=True)

    # Información de contacto
    st.write("### Información de Contacto")
    st.write("📞 Teléfono: 3116272410")
    st.write("✉️ Correo Electrónico: info@sanmiguelmv.com")
    st.write("🏠 Dirección: Calle 55a #24-28 Belén Manizales")
    st.markdown('<div class="social-links">', unsafe_allow_html=True)
    
    st.markdown("[Facebook ](https://www.facebook.com/SanMiguelMedicinaVeterinaria) | [Instagram](https://www.instagram.com/sanmiguelmvsas?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Sección para agregar nuevos clientes
elif opcion == "Agregar Cliente":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.write("### Agregar Nuevo Cliente")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Correo Electrónico")

    # Mantener solo el botón para agregar cliente
    if st.button("Agregar Cliente"):
        cliente_data = {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "email": email
        }
        response = requests.post("http://localhost:8000/clientes/", json=cliente_data)
        if response.status_code in [200, 201]:
            st.success("Cliente agregado exitosamente!")
        else:
            st.error("Error al agregar el cliente.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sección para agregar nuevas mascotas
elif opcion == "Agregar Mascota":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.write("### Agregar Nueva Mascota")
    nombre_mascota = st.text_input("Nombre de la Mascota")
    especie = st.text_input("Especie")
    raza = st.text_input("Raza")
    edad = st.number_input("Edad", min_value=0)

    # Seleccionar propietario de la lista de clientes
    clientes = get_clientes()
    cliente_options = {f"{cliente['nombre']} {cliente['apellido']}": cliente['id'] for cliente in clientes}
    propietario = st.selectbox("Propietario", options=list(cliente_options.keys()))

    if st.button("Agregar Mascota"):
        mascota_data = {
            "nombre": nombre_mascota,
            "especie": especie,
            "raza": raza,
            "edad": edad,
            "cliente_id": cliente_options[propietario]
        }
        response = requests.post("http://localhost:8000/mascotas/", json=mascota_data)
        if response.status_code in [200, 201]:
            st.success("Mascota agregada exitosamente!")
        else:
            st.error("Error al agregar la mascota.")
    st.markdown('</div>', unsafe_allow_html=True)

# Sección para agregar nuevas citas
elif opcion == "Agregar Cita":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.write("### Agregar Nueva Cita")
    
    # Seleccionar mascota
    mascotas = get_mascotas()
    mascota_options = {mascota['nombre']: mascota['id'] for mascota in mascotas}
    mascota_seleccionada = st.selectbox("Selecciona una Mascota", options=list(mascota_options.keys()))
    
    fecha = st.date_input("Fecha")
    motivo = st.text_input("Motivo")
    hora = st.text_input("Hora")  # Añadido campo para la hora
    
    if st.button("Agregar Cita"):
        cita_data = {
            "fecha": str(fecha),
            "mascota_id": mascota_options[mascota_seleccionada],  # Cambiado a mascota_id
            "motivo": motivo,
            "hora": hora  # Añadido campo para la hora
        }
        response = requests.post("http://localhost:8000/citas/", json=cita_data)
        if response.status_code in [200, 201]:
            st.success("Cita agregada exitosamente!")
        else:
            st.error("Error al agregar la cita.")
    st.markdown('</div>', unsafe_allow_html=True)

# Sección para agregar nuevos medicamentos
elif opcion == "Agregar Medicamento":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.write("### Agregar Nuevo Medicamento")
    
    nombre_medicamento = st.text_input("Nombre del Medicamento")
    descripcion = st.text_input("Descripción")
    stock = st.number_input("Stock", min_value=0)
    precio = st.number_input("Precio", min_value=0.0, format="%.2f")
    
    if st.button("Agregar Medicamento"):
        medicamento_data = {
            "nombre": nombre_medicamento,
            "descripcion": descripcion,
            "stock": stock,
            "precio": precio
        }
        response = requests.post("http://localhost:8000/medicamentos/", json=medicamento_data)
        if response.status_code in [200, 201]:
            st.success("Medicamento agregado exitosamente!")
        else:
            st.error("Error al agregar el medicamento.")
    st.markdown('</div>', unsafe_allow_html=True)