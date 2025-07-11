import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Cargar el archivo Excel
df = pd.read_excel('base2.xlsx')

# Crear el menú de páginas en la barra lateral
paginas = ['Presentación', 'Experiencia']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# Página de Presentación
if pagina_seleccionada == 'Presentación':
    st.markdown("<h1 style='text-align: center;'>SOUNDMOOD</h1>", unsafe_allow_html=True)
    
    texto = """
    Aquí escribe una presentación creativa sobre ti.
    ¿Quién eres?, 
    ¿De dónde eres?, 
    ¿Qué estudias?, 
    ¿Qué te gusta de tu carrera?, 
    ¿Qué te gustaría hacer en el futuro?, 
    ¿Qué te gusta hacer en tu tiempo libre?
    """
    
    st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True)

# Página de Experiencia
else: 
    # Selección de emociones con la opción "Selecciona una opción"
    emociones = ['Selecciona una opción', 'alegre', 'triste', 'relajado', 'romántico', 'divertido', 'motivado', 'estresado/ansioso', 'molesto']
    emocion = st.selectbox("Selecciona cómo te sientes hoy (Emoción):", emociones)

    # Verifica si se ha seleccionado una emoción válida
    if emocion == 'Selecciona una opción':
        emocion = None

    # Propósito de la canción solo para emociones específicas (triste, estresado/ansioso, molesto)
    proposito = ''
    if emocion in ['triste', 'estresado/ansioso', 'molesto']:
        proposito = st.radio("¿Qué buscas en la canción?", ['Que acompañe lo que siento', 'Que mejore mi estado de ánimo'])

    # Opciones de duración de la canción
    opciones_duracion = df['duracion'].dropna().unique()
    duracion_elegida = st.selectbox("¿Prefieres una canción corta o larga?", ['Selecciona una opción'] + list(opciones_duracion))
    
    if duracion_elegida == 'Selecciona una opción':
        duracion_elegida = None

    # Selección de idioma sin título
    idioma = st.radio("", ['Selecciona una opción', 'Español', 'Inglés'])
    
    if idioma == 'Selecciona una opción':
        idioma = None

    # Selección de época sin título
    epoca = st.radio("", ['Selecciona una opción', 'Hasta 2010', 'Desde 2011'])
    
    if epoca == 'Selecciona una opción':
        epoca = None

    # Verificamos que se haya hecho una selección válida
    if emocion and duracion_elegida and idioma and epoca:
        # Filtrar el DataFrame con los criterios seleccionados
        resultado = df[
            (df['emocion'].str.lower() == emocion.lower()) &
            (df['duracion'].str.lower() == duracion_elegida.lower()) &
            (df['idioma'].str.lower() == idioma.lower()) &
            ((df['año_exacto'] <= 2010) if epoca == 'hasta 2010' else (df['año_exacto'] >= 2011))
        ]

        # Mostrar la canción recomendada si existe
        if not resultado.empty:
            cancion = resultado.sample(1).iloc[0]
            
            # Mostrar la información de la canción
            st.subheader("🎶 Información de la canción recomendada 🎶")
            st.write(f"🎶 Nombre: {cancion['nombre_cancion']}")
            st.write(f"👤 Artista: {cancion['nombre_artista']}")
            st.write(f"🎸 Género: {cancion['genero']}")

            # Mostrar imagen del artista si está disponible
            foto = cancion['foto_artista']
            if isinstance(foto, str) and (foto.lower().endswith('.jpg') or foto.lower().endswith('.png')):
                st.image(foto, caption=f"Imagen de {cancion['nombre_artista']}", use_container_width=True)

            # Mostrar más detalles
            st.write(f"📲 Red Social: {cancion['red_social']} ({cancion['link_red_social']})")
            st.write(f"📝 Letra:\n{cancion['letra_cancion']}")
            st.write(f"ℹ Info: {cancion['info_cancion']}")
            st.write(f"🌐 [Spotify]({cancion['url_spotify']})  |  [Video]({cancion['url_video']})")
        else:
            st.write("No se encontraron canciones para tu selección.")
    else:
        st.write("Por favor selecciona todas las opciones para obtener una recomendación.")
