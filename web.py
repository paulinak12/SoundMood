# Importamos las librerías necesarias para el proyecto
import streamlit as st # para crear la interfaz web interactiva
import pandas as pd #para poder trabajar con la base de datos en Excel
import requests #para obtener imágenes desde enlaces externos

# Estas librerías las agregamos para generar la nube de palabras
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Cargamos nuestra base de datos desde un archivo Excel previamente trabajado
df = pd.read_excel('base2.xlsx')

# Nos aseguramos de que la columna del año esté en formato numérico para poder filtrarla luego
df['año_exacto'] = pd.to_numeric(df['año_exacto'], errors='coerce')

# -------------------- MENÚ DE PÁGINAS --------------------
# Definimos las dos secciones principales de la página: presentación y encuesta
paginas = ['Presentación', 'Encuesta']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# -------------------- PÁGINA DE PRESENTACIÓN --------------------
if pagina_seleccionada == 'Presentación':
    # Título centrado con HTML
    st.markdown("<h1 style='text-align: center;'>SOUNDMOOD</h1>", unsafe_allow_html=True)
    # Mostramos una imagen ilustrativa centrada justo debajo del título
    st.markdown(
        """
        <div style='text-align: center; margin-top: 20px;'>
            <img src="https://8b0b893f25.cbaul-cdnwnd.com/5dd570d4033bedf9e45dd6d8b0914db6/200000002-44ead44eaf/musica_y_cerebro_02-2000x1402-removebg-preview.png?ph=8b0b893f25" 
            alt="Música y cerebro" width="350">
        </div>
        """,
        unsafe_allow_html=True
    )
    # Este es el texto de presentación que redactamos para explicar el propósito del proyecto
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
    # Usamos HTML para alinear el texto y controlar su tamaño
    st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True)

# -------------------- PÁGINA DE ENCUESTA --------------------
else:
    # Pregunta 1: Selección de emoción (trabajamos con una lista predefinida)
    emociones = ['Selecciona una opción', 'Alegre', 'Relajado', 'Romántico', 'Divertido', 'Motivado', 'Triste', 'Estresado/ansioso', 'Molesto']
    emocion = st.selectbox("Selecciona cómo te sientes hoy (Emoción):", emociones, key="emocion")
    if emocion == 'Selecciona una opción':
        emocion = None

    # Pregunta 2: Solo si la emoción es negativa, preguntamos por el propósito de la canción
    proposito = ''
    if emocion in ['Triste', 'Estresado/ansioso', 'Molesto']:
        proposito = st.radio("¿Qué buscas en la canción?", 
                             ['Que acompañe lo que siento', 'Que mejore mi estado de ánimo'],
                             index=0, key="proposito")

    # Pregunta 3: Duración (corta o larga)
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

    # -------------------- FILTRADO Y LÓGICA --------------------
    # Si el usuario completó todas las opciones, filtramos la base
    if emocion and duracion_elegida and idioma and epoca:
        # Clasificamos si la canción es de antes o después del 2010
        if epoca.lower() == 'hasta 2010':
            condicion_epoca = df['año_exacto'] <= 2010
        else:
            condicion_epoca = df['año_exacto'] >= 2011

        # Filtramos según todas las condiciones
        resultado = df[
            (df['emocion'].str.lower() == emocion.lower()) &
            (df['duracion'].str.lower() == duracion_elegida.lower()) &
            (df['idioma'].str.lower() == idioma.lower()) &
            condicion_epoca
        ]

        # Si es emoción negativa, filtramos por propósito 
        if emocion.lower() in ['triste', 'estresado/ansioso', 'molesto']:
            resultado['proposito'] = resultado['proposito'].str.lower().str.strip()
            if proposito == 'Que acompañe lo que siento':
                resultado = resultado[resultado['proposito'] == 'acompañar']
            elif proposito == 'Que mejore mi estado de ánimo':
                resultado = resultado[resultado['proposito'] == 'mejorar']

        # -------------------- MOSTRAR RESULTADO --------------------
        if not resultado.empty:
            cancion = resultado.sample(1).iloc[0]
            st.subheader("🎶 Información de la canción recomendada 🎶")

            # Usamos dos columnas para dividir la información: fue una decisión para mejorar la visualización
            col1, col2 = st.columns([1, 1])
            with col1:
                # Mostramos los datos básicos de la canción
                st.write(f"🎶 Nombre: {cancion['nombre_cancion']}")
                st.write(f"📅 Año: {int(cancion['año_exacto'])}")  # Mostramos el año exacto
                st.write(f"⌚ Duración: {cancion['duracion_exacta']}")
                st.write(f"🎸 Género: {cancion['genero']}")
                st.write(f"👤 Artista: {cancion['nombre_artista']}")
                st.write(f"📲 Red Social: {cancion['red_social']} ({cancion['link_red_social']})")

                # Agregamos la imagen del artista, siempre y cuando sea válida
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
                # Incluimos una breve descripción informativa que tenemos en la BD
                st.write(f"ℹ️ Info: {cancion['info_cancion']}")

                #Nube de palabras: esto lo agregamos para reconocer visualmente los temas presentes en la letra
                st.markdown("☁️ Las palabras más destacadas de la canción:")
                texto = str(cancion['letra_cancion']).lower()
                stop_words = set(stopwords.words('english')).union(set(stopwords.words('spanish')))
                wordcloud = WordCloud(stopwords=stop_words,
                                      background_color='white',
                                      width=400,
                                      height=300,
                                      colormap='plasma').generate(texto)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)

            with col2:
                # En la segunda columna agregamos los enlaces y la letra
                st.write("🌐 Escúchala o mira el video oficial:")
                st.markdown(f"[Spotify]({cancion['url_spotify']})  |  [Video]({cancion['url_video']})")

                # Formateamos los versos de la letra para que no se vean desordenados
                st.markdown("📝 **Letra:**")
                letra = cancion['letra_cancion'].replace('\n', '<br>')
                st.markdown(
                    f"""
                    <div style="font-size: 14px; line-height: 1.6; text-align: left;">
                        {letra}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No se encontraron canciones para tu selección.")
    else:
        st.info("Por favor selecciona todas las opciones para obtener una recomendación.")
