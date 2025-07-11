import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
df = pd.read_excel('base2.xlsx')
paginas = ['Presentación', 'Experiencia']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)
if pagina_seleccionada == 'Presentación':
    st.markdown("<h1 style='text-align: center;'>SoundMood</h1>", unsafe_allow_html=True)
    texto = """
    Aquí escribe una presentación creativa sobre ti.
    ¿Quién eres?, 
    ¿De dónde eres?, 
    ¿Qué estudias?, 
    ¿Qué te gusta de tu carrera?, 
    ¿Qué te gustaría hacer en el futuro?, 
    ¿Qué te gusta hacer en tu tiempo libre?
    """
    # Las comillas triples (""") en Python se utilizan para definir cadenas multilínea.
    
    # Mostramos el texto
    st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True)
else: 
    emociones = ['alegre', 'triste', 'relajado', 'romántico', 'divertido', 'motivado', 'estresado/ansioso', 'molesto']
    emocion = st.selectbox("Selecciona cómo te sientes hoy (Emoción):", emociones)
    # for i, emocion in enumerate(emociones, 1):
        # print(f"[{i}] {emocion.capitalize()}")
    # emocion_elegida = int(input("S la emoción: "))
    # emocion = emociones[emocion_elegida - 1]

    proposito = ''
    if emocion in ['triste', 'estresado/ansioso', 'molesto']:
        proposito = st.radio("¿Qué buscas en la canción?", ['Que acompañe lo que siento', 'Que mejore mi estado de ánimo'])
        #print("¿Qué buscas en la canción?")
        #print("[1] Que acompañe lo que siento")
        #print("[2] Que mejore mi estado de ánimo")
        #proposito = 'acompañar' if int(input("Selecciona una opción: ")) == 1 else 'mejorar'
        proposito = 'acompañar' if proposito == 'Que acompañe lo que siento' else 'mejorar'

        opciones_duracion = df['duracion'].dropna().unique()
        duracion_elegida = st.selectbox("¿Prefieres una canción corta o larga?", opciones_duracion)
       # print("¿Prefieres una canción corta o larga?")
        #for i, val in enumerate(opciones_duracion, 1):
           # print(f"[{i}] {val.capitalize()}")
        #duracion_elegida = opciones_duracion[int(input("Selecciona una opción: ")) - 1]

        idioma = st.radio("Selecciona el idioma de la canción:", ['Español', 'Inglés'])
        #print("Selecciona el idioma de la canción:")
        #print("[1] Español")
        # print("[2] Inglés")
        #idioma = 'español' if int(input("Selecciona una opción: ")) == 1 else 'inglés'

        epoca = st.radio("¿De qué época prefieres la canción?", ['Hasta 2010', 'Desde 2011'])
        #print("¿De qué época prefieres la canción?")
        #print("[1] Hasta 2010")
        #print("[2] Desde 2011")
        #epoca = 'hasta 2010' if int(input("Selecciona una opción: ")) == 1 else 'desde 2011'

        resultado = df[
            (df['emocion'].str.lower() == emocion.lower()) &
            (df['duracion'].str.lower() == duracion_elegida.lower()) &
            (df['idioma'].str.lower() == idioma.lower()) &
            ((df['año_exacto'] <= 2010) if epoca == 'hasta 2010' else (df['año_exacto'] >= 2011))
        ]

        if not resultado.empty:
            cancion = resultado.sample(1).iloc[0]
            st.subheader("🎶 Información de la canción recomendada 🎶")
            st.write(f"🎶 Nombre: {cancion['nombre_cancion']}")
            st.write(f"👤 Artista: {cancion['nombre_artista']}")
            st.write(f"🎸 Género: {cancion['genero']}")
            
            # Mostrar imagen usando display_html de IPython
            foto = cancion['foto_artista']
            if isinstance(foto, str) and (foto.lower().endswith('.jpg') or foto.lower().endswith('.png')):
                    st.image(foto, caption=f"Imagen de {cancion['nombre_artista']}", use_container_width=True)

            st.write(f"📲 Red Social: {cancion['red_social']} ({cancion['link_red_social']})")
            st.write(f"📝 Letra:\n{cancion['letra_cancion']}")
            st.write(f"ℹ️ Info: {cancion['info_cancion']}")
            st.write(f"🌐 [Spotify]({cancion['url_spotify']})  |  [Video]({cancion['url_video']})")
        else:
            #print("No se encontraron canciones para tu selección.")
            st.write("No se encontraron canciones para tu selección.")
