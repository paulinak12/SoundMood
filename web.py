import streamlit as st
import pandas as pd
from PIL import Image

# Cargar el archivo Excel
df = pd.read_excel('base2.xlsx')

# Asegurar que 'año_exacto' sea numérico
df['año_exacto'] = pd.to_numeric(df['año_exacto'], errors='coerce')

# Inicializar estado de sesión para limpiar formulario
if 'reset' not in st.session_state:
    st.session_state.reset = False

# Crear el menú de páginas en la barra lateral
paginas = ['Presentación', 'Encuesta']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# ------------------ PÁGINA DE PRESENTACIÓN ------------------
if pagina_seleccionada == 'Presentación':
    st.markdown("<h1 style='text-align: center;'>SOUNDMOOD</h1>", unsafe_allow_html=True)

    texto = """
    ¡Hola! Somos Paulina Kosaka, Marcela Ismodes y Malena Aldazabal. Queremos darte la bienvenida a nuestra página. A continuación, te presentamos más información sobre el proyecto.

🎧 **SoundMood**: Tu estado de ánimo tiene sonido.

SoundMood es una página web interactiva que busca conectar la música con las emociones de cada usuario. A través de una interfaz amigable y personalizada, ofrecemos recomendaciones de canciones basadas en el estado de ánimo actual de la persona.

Pero vamos más allá de una simple recomendación musical: personalizamos la experiencia según las preferencias del usuario en cuanto al idioma (español o inglés), la duración de la canción y el año de lanzamiento.

Además, para enriquecer la experiencia musical, SoundMood también ofrece información detallada sobre el artista y la canción, permitiendo así que el usuario no solo escuche música, sino que también descubra y aprenda sobre lo que está escuchando.

__¿Por qué creamos SoundMood?__

La música siempre ha sido una herramienta poderosa para conectar con las emociones humanas. Todos hemos buscado canciones cuando estamos tristes, queremos motivarnos o simplemente relajarnos. Sin embargo, no siempre sabemos qué escuchar o no encontramos algo que realmente encaje con cómo nos sentimos.

SoundMood nace para resolver ese problema, ofreciendo una plataforma sencilla pero efectiva que:

- Comprende lo que sientes  
- Te recomienda música acorde a ese sentimiento  
- Te da control total sobre el tipo de música que quieres descubrir  
- Enriquece tu experiencia al darte contexto e información sobre lo que estás escuchando
    """
    st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True)

# ------------------ PÁGINA DE ENCUESTA ------------------
else:
    # Pregunta 1: Emoción
    emociones = ['Selecciona una opción', 'Alegre', 'Relajado', 'Romántico', 'Divertido', 'Motivado', 'Triste', 'Estresado/ansioso', 'Molesto']
    emocion = st.selectbox("Selecciona cómo te sientes hoy (Emoción):", emociones, key="emocion")
    if emocion == 'Selecciona una opción':
        emocion = None

    # Pregunta 2: Propósito solo si la emoción es negativa
    proposito = ''
    if emocion in ['Triste', 'Estresado/ansioso', 'Molesto']:
        proposito = st.radio("¿Qué buscas en la canción?", 
                             ['Que acompañe lo que siento', 'Que mejore mi estado de ánimo'],
                             index=0, key="proposito")

    # Pregunta 3: Duración
    opciones_duracion = df['duracion'].dropna().unique()
    duracion_elegida = st.selectbox("¿Prefieres una canción corta o larga?", ['Selecciona una opción'] + list(opciones_duracion), key="duracion")
    if duracion_elegida == 'Selecciona una opción':
        duracion_elegida = None

    # Pregunta 4: Idioma
    idioma = st.radio("", ['Selecciona una opción', 'Español', 'Inglés'], key="idioma")
    if idioma == 'Selecciona una opción':
        idioma = None

    # Pregunta 5: Época
    epoca = st.radio("", ['Selecciona una opción', 'Hasta 2010', 'Desde 2011'], key="epoca")
    if epoca == 'Selecciona una opción':
        epoca = None

    # Verificar que se completaron todas las preguntas
    if emocion and duracion_elegida and idioma and epoca:
        # Filtrar por época
        if epoca.lower() == 'hasta 2010':
            condicion_epoca = df['año_exacto'] <= 2010
        else:
            condicion_epoca = df['año_exacto'] >= 2011

        # Filtrar según los criterios seleccionados
        resultado = df[
            (df['emocion'].str.lower() == emocion.lower()) &
            (df['duracion'].str.lower() == duracion_elegida.lower()) &
            (df['idioma'].str.lower() == idioma.lower()) &
            condicion_epoca
        ]

        # Filtrar también por propósito si aplica
        if emocion.lower() in ['triste', 'estresado/ansioso', 'molesto']:
            resultado['proposito'] = resultado['proposito'].str.lower().str.strip()
            if proposito == 'Que acompañe lo que siento':
                resultado = resultado[resultado['proposito'] == 'acompañar']
            elif proposito == 'Que mejore mi estado de ánimo':
                resultado = resultado[resultado['proposito'] == 'mejorar']

        # Mostrar canción si hay resultado
        if not resultado.empty:
            cancion = resultado.sample(1).iloc[0]
            st.subheader("🎶 Información de la canción recomendada 🎶")

            # Dividir contenido en columnas
            col1, col2 = st.columns([2, 3])

            with col1:
                st.write(f"🎶 Nombre: {cancion['nombre_cancion']}")
                st.write(f"⌚ Duración: {cancion['duracion_exacta']}")
                st.write(f"🎸 Género: {cancion['genero']}")
                st.write(f"👤 Artista: {cancion['nombre_artista']}")
                st.write(f"📲 Red Social: {cancion['red_social']} ({cancion['link_red_social']})")
                foto = cancion['foto_artista']
                if isinstance(foto, str) and (foto.lower().endswith('.jpg') or foto.lower().endswith('.png')):
                    st.markdown(
                        f"""
                        <div style="text-align: center;">
                            <img src="{foto}" alt="Imagen de {cancion['nombre_artista']}" width="200" style="border-radius: 10px;">
                            <p style="font-size: 14px; color: #555;">Imagen de {cancion['nombre_artista']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.write(f"ℹ️ Info: {cancion['info_cancion']}")

            with col2:
                st.write("🌐 Escúchala o mira el video oficial:")
                st.markdown(f"[Spotify]({cancion['url_spotify']})  |  [Video]({cancion['url_video']})")

                st.markdown("📝 **Letra:**")
                st.markdown(
                    f"""
                    <div style="overflow-x: auto;">
                        <pre style="font-size: 14px; line-height: 1.5;">{cancion['letra_cancion']}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Botón para reiniciar todo
            if st.button("🔁 Buscar otra canción / Limpiar selección"):
                for key in ['emocion', 'proposito', 'duracion', 'idioma', 'epoca']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()
        else:
            st.warning("No se encontraron canciones para tu selección.")
    else:
        st.info("Por favor selecciona todas las opciones para obtener una recomendación.")
