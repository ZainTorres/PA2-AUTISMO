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
