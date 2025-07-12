import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Cargar el archivo Excel
df = pd.read_excel('base2.xlsx')

# Asegurarse de que la columna 'año_exacto' sea numérica
df['año_exacto'] = pd.to_numeric(df['año_exacto'], errors='coerce')  # Convertir 'año_exacto' a numérico, ignorando errores


# Asegurarse de que la columna 'año_exacto' sea numérica
df['año_exacto'] = pd.to_numeric(df['año_exacto'], errors='coerce')  # Convertir 'año_exacto' a numérico, ignorando errores

# Crear el menú de páginas en la barra lateral
paginas = ['Presentación', 'Encuesta']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# Página de Presentación
if pagina_seleccionada == 'Presentación':
    st.markdown("<h1 style='text-align: center;'>SOUNDMOOD</h1>", unsafe_allow_html=True)
    
    texto = """
    ¡Hola! Somos Paulina Kosaka, Marcela Ismodes y Malena Aldazabal. Queremos darte la bienvenida a nuestra página. A continuación, te presentamos más información sobre el proyecto.
    
🎧 **SoundMood**: Tu estado de ánimo tiene sonido. ¿Qué es SoundMood?
    
SoundMood es una página web interactiva que busca conectar la música con las emociones de cada usuario. A través de una interfaz amigable y personalizada, ofrecemos recomendaciones de canciones basadas en el estado de ánimo actual de la persona. 
    
Pero vamos más allá de una simple recomendación musical: personalizamos la experiencia según las preferencias del usuario en cuanto al idioma (español o inglés), la duración de la canción y el año de lanzamiento.
    
Además, para enriquecer la experiencia musical, SoundMood también ofrece información detallada sobre el artista y la canción, permitiendo así que el usuario no solo escuche música, sino que también descubra y aprenda sobre lo que está escuchando.
    
__¿Por qué creamos SoundMood?__
    
La música siempre ha sido una herramienta poderosa para conectar con las emociones humanas. Todos hemos buscado canciones cuando estamos tristes, queremos motivarnos o simplemente relajarnos. Sin embargo, no siempre sabemos qué escuchar o no encontramos algo que realmente encaje con cómo nos sentimos.
    
SoundMood nace para resolver ese problema, ofreciendo una plataforma sencilla pero efectiva que:
    
- Comprende lo que sientes
- Te recomienda música acorde a ese sentimiento
- Te da control total sobre el tipo de música que quieres descubrir
- Enriquece tu experiencia al darte contexto e información sobre lo que estás escuchando
    """
    
    st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True)

# Página de Encuesta
else: 
    # Selección de emociones con la opción "Selecciona una opción"
    emociones = ['Selecciona una opción', 'Alegre', 'Relajado', 'Romántico', 'Divertido', 'Motivado', 'Triste', 'Estresado/ansioso', 'Molesto']
    emocion = st.selectbox("Selecciona cómo te sientes hoy (Emoción):", emociones)

    # Verifica si se ha seleccionado una emoción válida
    if emocion == 'Selecciona una opción':
        emocion = None

    # Propósito de la canción solo para emociones específicas (triste, estresado/ansioso, molesto)
    proposito = ''
    if emocion in ['Triste', 'Estresado/ansioso', 'Molesto']:
        # Aquí utilizamos un radio button para seleccionar el propósito de la canción
        proposito = st.radio("¿Qué buscas en la canción?", 
                             ['Que acompañe lo que siento', 'Que mejore mi estado de ánimo'],
                             index=0)  # Usamos index=0 para que la opción predeterminada sea 'Que acompañe lo que siento'

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
        # Definir el filtro de época basado en la selección
        if epoca.lower() == 'hasta 2010':
            condicion_epoca = df['año_exacto'] <= 2010
        else:
            condicion_epoca = df['año_exacto'] >= 2011

        # Filtrar el DataFrame con los criterios seleccionados
        resultado = df[
            (df['emocion'].str.lower() == emocion.lower()) &
            (df['duracion'].str.lower() == duracion_elegida.lower()) &
            (df['idioma'].str.lower() == idioma.lower()) &
            condicion_epoca
        ]
    
        if emocion in ['triste', 'estresado/ansioso', 'molesto']:
    # Normalizar texto en la columna 'proposito'
            resultado['proposito'] = resultado['proposito'].str.lower().str.strip()

            if proposito == 'Que acompañe lo que siento':
                resultado = resultado[resultado['proposito'] == 'acompañar']
            elif proposito == 'Que mejore mi estado de ánimo':
                resultado = resultado[resultado['proposito'] == 'mejorar']


        # Mostrar la canción recomendada si existe
        if not resultado.empty:
            cancion = resultado.sample(1).iloc[0]
            
            # Mostrar la información de la canción
            st.subheader("🎶 Información de la canción recomendada 🎶")
            st.write(f"🎶 Nombre: {cancion['nombre_cancion']}")
            st.write(f"⌚ Duración: {cancion['duracion_exacta']}")
            st.write(f"🎸 Género: {cancion['genero']}")
            st.write(f"👤 Artista: {cancion['nombre_artista']}")
            st.write(f"📲 Red Social: {cancion['red_social']} ({cancion['link_red_social']})")

            # Mostrar imagen del artista si está disponible
            # Obtener la URL de la imagen del artista desde la base de datos
            foto = cancion['foto_artista']

            # Verificar que el valor en 'foto_artista' sea una cadena (str) y que termine en .jpg o .png
            if isinstance(foto, str) and (foto.lower().endswith('.jpg') or foto.lower().endswith('.png')):
    
            # Usar HTML incrustado para centrar la imagen y mostrar un texto debajo (caption)
                st.markdown(
                    f"""
                    <div style="text-align: center;">  <!-- Centra todo el contenido dentro del div -->
                        <img src="{foto}" alt="Imagen de {cancion['nombre_artista']}" width="200" style="border-radius: 10px;"> <!-- Muestra la imagen con ancho reducido y bordes redondeados -->
                        <p style="font-size: 14px; color: #555;">Imagen de {cancion['nombre_artista']}</p> <!-- Texto debajo de la imagen, en gris claro -->
                    </div>
                    """,
                    unsafe_allow_html=True  # Permite renderizar HTML dentro de Streamlit
                )

            # Mostrar más detalles
            st.write(f"ℹ️ Info: {cancion['info_cancion']}")
            st.write("📝 Letra:")
            # Mostrar la letra de la canción tal como está, respetando saltos de línea y espacios
            st.text(cancion['letra_cancion'])
            st.write(f"🌐 [Spotify]({cancion['url_spotify']})  |  [Video]({cancion['url_video']})")
        else:
            st.write("No se encontraron canciones para tu selección.")
    else:
        st.write("Por favor selecciona todas las opciones para obtener una recomendación.")
