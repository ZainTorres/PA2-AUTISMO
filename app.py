import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os  # <-- CORRECCIÓN: Librería importada correctamente para solucionar el NameError

# Configuración inicial del entorno de visualización
st.set_page_config(
    page_title="Plataforma de Tamizaje de Autismo en Adultos",
    page_icon="🧩",
    layout="centered"
)

# Panel lateral: Identificación institucional y recursos fuente
st.sidebar.header("⚙️ Control de Identificación")
st.sidebar.text_input("Nombre del Estudiante:", value="Robert", disabled=True)
st.sidebar.text_input("Código de Alumno:", value="[Tu Código Aquí]", disabled=True)

st.sidebar.markdown("---")
st.sidebar.subheader("🔗 Recursos del Proyecto")
# Vínculo directo al desarrollo del cuaderno de análisis en Google Colab
st.sidebar.markdown(
    "[📂 Ver Cuaderno Origen (Google Colab)](https://colab.research.google.com/drive/1CReebMxdUtDdMaOp79aPPrXNDKYIf2t_?usp=sharing)"
)

# Encabezado principal de la aplicación web
st.title("🧩 Asistente Clínico para el Tamizaje de Autismo en Adultos")
st.write(
    "Esta plataforma de software automatizada implementa un modelo de aprendizaje automático "
    "(Regresión Logística) para evaluar la probabilidad de presentación de rasgos asociados al "
    "Trastorno del Espectro Autista (TEA) en individuos mayores de 18 años, basándose en la "
    "metodología estructurada del cuestionencial conductual AQ-10."
)

st.markdown("---")

# Función optimizada para la lectura y persistencia en caché de los artefactos del modelo
@st.cache_resource
def cargar_artefactos_clinicos():
    # Detecta automáticamente la ubicación exacta de app.py en el servidor
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # CORRECCIÓN: Rutas absolutas seguras usando tus archivos reales de GitHub
    ruta_modelo = os.path.join(BASE_DIR, "model1", "modelo_autismo_lr.pkl")
    ruta_columnas = os.path.join(BASE_DIR, "model1", "columnas_modelo.pkl")
    
    modelo = joblib.load(ruta_modelo)
    columnas = joblib.load(ruta_columnas)
    return modelo, columnas

try:
    model, columnas_entrenamiento = cargar_artefactos_clinicos()
except Exception as e:
    st.error(f"Error crítico al cargar las estructuras de datos serializadas: {e}")
    st.stop()


# -------------------------------------------------------------------------
# FORMULARIO DE CAPTURA DE DATOS
# -------------------------------------------------------------------------
st.subheader("📋 Sección 1: Cuestionario de Comportamiento (AQ-10)")
st.write("Seleccione el nivel de presencia (**1** para Presencia / **0** para Ausencia) de los siguientes patrones:")

# Columnas para organizar visualmente las preguntas de tamizaje
col1, col2 = st.columns(2)

with col1:
    a1 = st.radio("A1: ¿Nota ruidos sutiles que otros no perciben?", [0, 1], horizontal=True)
    a3 = st.radio("A3: ¿Le resulta fácil hacer múltiples tareas a la vez?", [0, 1], horizontal=True)
    a5 = st.radio("A5: ¿Entiende insinuaciones de otros fácilmente?", [0, 1], horizontal=True)
    a7 = st.radio("A7: ¿Le cuesta deducir intenciones de personajes al leer?", [0, 1], horizontal=True)
    a9 = st.radio("A9: ¿Interpreta emociones analizando expresiones faciales?", [0, 1], horizontal=True)

with col2:
    a2 = st.radio("A2: ¿Se enfoca más en el panorama general que en detalles?", [0, 1], horizontal=True)
    a4 = st.radio("A4: ¿Retoma una actividad rápido tras una interrupción?",
