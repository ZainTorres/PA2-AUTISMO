import streamlit as st
import pandas as pd
import numpy as np
import joblib

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
    "metodología estructurada del cuestionario conductual AQ-10."
)

st.markdown("---")

# Función optimizada para la lectura y persistencia en caché de los artefactos del modelo
@st.cache_resource
def cargar_artefactos_clinicos():
    # Carga de la arquitectura matemática y la estructura exacta de vectores de entrada
    modelo = joblib.load("model1/logistic_regression_model.pkl")
    columnas = joblib.load("model1/columnas_modelo.pkl")
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
    a4 = st.radio("A4: ¿Retoma una actividad rápido tras una interrupción?", [0, 1], horizontal=True)
    a6 = st.radio("A6: ¿Nota con facilidad si alguien se aburre al hablar?", [0, 1], horizontal=True)
    a8 = st.radio("A8: ¿Dedica mucho tiempo a clasificar o coleccionar datos?", [0, 1], horizontal=True)
    a10 = st.radio("A10: ¿Tiene gran dificultad para adaptarse a cambios de rutina?", [0, 1], horizontal=True)

st.markdown("---")
st.subheader("👤 Sección 2: Perfil Demográfico y Antecedentes")

col_demo1, col_demo2, col_demo3 = st.columns(3)

with col_demo1:
    edad = st.number_input("Edad del evaluado:", min_value=18, max_value=100, value=28, step=1)

with col_demo2:
    genero = st.selectbox("Género asignado al nacer:", ["m", "f"])

with col_demo3:
    jaundice = st.selectbox("¿Manifestó ictericia neonatal?", ["no", "yes"])


# -------------------------------------------------------------------------
# PROCESAMIENTO Y PRECOCCIÓN DE DATOS (PIPELINE DE INFERENCIA)
# -------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔮 Obtener Predicción", type="primary", use_container_width=True):
    
    # 1. Reconstrucción base del diccionario con los nombres originales del dataset
    registro = {
        'A1_Score': a1, 'A2_Score': a2, 'A3_Score': a3, 'A4_Score': a4, 'A5_Score': a5,
        'A6_Score': a6, 'A7_Score': a7, 'A8_Score': a8, 'A9_Score': a9, 'A10_Score': a10,
        'age': float(edad)
    }
    
    df_usuario = pd.DataFrame([registro])
    
    # 2. Replicación controlada de la lógica One-Hot Encoding manual.
    # Evaluamos dinámicamente cómo quedaron nombradas las columnas en tu entrenamiento original.
    for col in columnas_entrenamiento:
        # Mapeo para variables de género (soporta gender_m, gender_f, o variantes en mayúsculas)
        if 'gender' in col.lower():
            if genero in col.lower():
                df_usuario[col] = 1
            else:
                df_usuario[col] = 0
                
        # Mapeo para variables de ictericia (jaundice_yes / jundice_yes / jaundice_no)
        elif 'jaund' in col.lower():  # Tolerante a errores comunes de escritura como 'jundice'
            if jaundice in col.lower():
                df_usuario[col] = 1
            else:
                df_usuario[col] = 0

    # 3. Reindexación matemática rígida. Alinea el vector al orden y cantidad exacta de columnas 
    # de entrenamiento, rellenando con 0 cualquier categoría que no se haya activado (ej. otras etnias/países).
    df_usuario_final = df_usuario.reindex(columns=columnas_entrenamiento, fill_value=0)
    
    # 4. Inferencia mediante el estimador
    prediccion = model.predict(df_usuario_final)[0]
    probabilidades = model.predict_proba(df_usuario_final)[0]
    
    # -------------------------------------------------------------------------
    # DESPLIEGUE VISUAL DEL DICTAMEN CLÍNICO
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📊 Dictamen de Evaluación Analítica")
    
    if prediccion == 1 or str(prediccion).lower() == 'yes':
        porcentaje_certeza = probabilidades[1] * 100
        st.error(
            f"⚠️ **Riesgo Clínico de Rasgos de TEA Detectado**  \n"
            f"El clasificador estima una probabilidad de **{porcentaje_certeza:.2f}%** basada en las métricas de comportamiento ingresadas."
        )
        st.info(
            "💡 **Nota Técnica:** Este resultado responde a la presencia significativa de indicadores del "
            "test AQ-10 que se correlacionan estadísticamente con clasificaciones positivas de TEA dentro "
            "de la muestra de control de la UCI."
        )
    else:
        porcentaje_certeza = probabilidades[0] * 100
        st.success(
            f"✅ **Bajo Riesgo de Rasgos de TEA**  \n"
            f"El clasificador estima una probabilidad de **{porcentaje_certeza:.2f}%** de pertenecer al grupo de control estándar."
        )
        st.write("Las variables ingresadas no muestran una correlación matemática crítica con las trazas del trastorno.")
        
    # Cláusula de exención de responsabilidad clínico obligatoria
    st.markdown(
        "<small style='color: gray;'>⚠️ **Advertencia Médica Institucional:** Este sistema digital representa "
        "una herramienta estrictamente analítica de tamizaje estadístico y soporte preliminar. "
        "**No constituye un diagnóstico médico, clínico o psicométrico formal.** Cualquier conclusión debe ser "
        "evaluada y contrastada de manera presencial por un profesional de la salud o especialista calificado en el área neurorreferencial.</small>", 
        unsafe_allow_html=True
    )
