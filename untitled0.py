import pandas as pd

df = pd.read_excel('/mnt/data/Base de datos (1).xlsx')

emociones = ['alegre', 'triste', 'relajado', 'romantico', 'divertido', 'motivado', 'estresado', 'ansioso', 'molesto']
print("Selecciona cómo te sientes hoy (Emoción):")
for i, emocion in enumerate(emociones, 1):
    print(f"[{i}] {emocion.capitalize()}")
emocion_elegida = int(input("Ingresa el número de la emoción: "))
emocion = emociones[emocion_elegida - 1]

proposito = ''
if emocion in ['triste', 'estresado', 'ansioso', 'molesto']:
    print("¿Qué buscas en la canción?")
    print("[1] Que acompañe lo que siento")
    print("[2] Que mejore mi estado de ánimo")
    proposito = 'acompañar' if int(input("Selecciona una opción: ")) == 1 else 'mejorar'

# USAR DIRECTAMENTE LOS VALORES DE LA COLUMNA "duracion"
opciones_duracion = df['duracion'].dropna().unique()
print("¿Prefieres una canción corta o larga?")
for i, val in enumerate(opciones_duracion, 1):
    print(f"[{i}] {val.capitalize()}")
duracion_elegida = opciones_duracion[int(input("Selecciona una opción: ")) - 1]

print("Selecciona el idioma de la canción:")
print("[1] Español")
print("[2] Inglés")
idioma = 'español' if int(input("Selecciona una opción: ")) == 1 else 'inglés'

print("¿De qué época prefieres la canción?")
print("[1] Hasta 2010")
print("[2] Desde 2011")
epoca = 'hasta 2010' if int(input("Selecciona una opción: ")) == 1 else 'desde 2011'

resultado = df[
    (df['emocion'].str.lower() == emocion.lower()) &
    (df['duracion'].str.lower() == duracion_elegida.lower()) &
    (df['idioma'].str.lower() == idioma.lower()) &
    ((df['año_exacto'] <= 2010) if epoca == 'hasta 2010' else (df['año_exacto'] >= 2011))
]

if not resultado.empty:
    cancion = resultado.sample(1).iloc[0]
    print("\n=== Información de la canción recomendada ===")
    print(f"🎶 Nombre: {cancion['nombre_cancion']}")
    print(f"👤 Artista: {cancion['nombre_artista']}")
    print(f"🎸 Género: {cancion['genero']}")
    print(f"🖼️ Foto: {cancion['foto_artista']}")
    print(f"📲 Red Social: {cancion['red_social']} ({cancion['link_red_social']})")
    print(f"📝 Letra:\n{cancion['letra_cancion']}")
    print(f"ℹ️ Info: {cancion['info_cancion']}")
    print(f"🌐 Spotify: {cancion['url_spotify']}  |  Video: {cancion['url_video']}")
else:
    print("No se encontraron canciones para tu selección.")

