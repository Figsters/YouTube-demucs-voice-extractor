from __future__ import unicode_literals
import yt_dlp
import sys
import os
from tqdm import tqdm
import validators
import subprocess
import pandas as pd
from pydub import AudioSegment

# Descarga el audio del video de Youtube en formato .wav
def download_from_url(url, artist_name):
    try:
        if not os.path.exists(artist_name):
            os.makedirs(artist_name)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(artist_name, '%(title)s.%(ext)s'), # Usa el título del video como nombre de archivo
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'quiet': True,
            'progress_hooks': [lambda d: tqdm.write(d['filename'])],
        }

        before_files = set(os.listdir(artist_name))  # archivos antes de la descarga

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        after_files = set(os.listdir(artist_name))  # archivos después de la descarga

        # Obtener el nombre del archivo descargado
        new_files = after_files - before_files
        if len(new_files) == 0:
            raise Exception("No se ha descargado ningún archivo")
        elif len(new_files) > 1:
            raise Exception("Se han descargado múltiples archivos")
        else:
            file_name = new_files.pop()
            file_path = os.path.join(artist_name, file_name)
            return file_path

    except Exception as e:
        print("Error durante la descarga: ", e)



# Maneja los argumentos de línea de comandos y llama a download_from_url
def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print("Demasiados argumentos.")
        exit()
    elif len(args) == 1:
        filename = sys.argv[1]
        urlsdb = pd.read_excel(os.path.basename(filename))
        urls = urlsdb.values.tolist()
        artist_name = os.path.splitext(os.path.basename(filename))[0]
        print(artist_name)
    else:
        urls = [input("Ingrese el enlace de Youtube: ")]
        artist_name = input("Ingrese el nombre del artista: ")
    
    if not artist_name:
        print("Debe ingresar un nombre de artista.")
        exit()
    artist_path = os.path.join(os.getcwd(), artist_name)
    if os.path.exists(artist_path):
        print("El directorio para el artista ya existe.")
    else:
        os.mkdir(artist_path)
    print(artist_path,type(artist_path))

    for url in urls:
        url = url[0]
        # Verifica que la URL es un enlace de Youtube válido
        if "youtube.com" not in url:
            print("La URL debe contener 'youtube.com'")
            exit() 

        # Verificar si la URL está bien formada
        if not validators.url(url):
            print("La URL es inválida o está mal formada.")
            exit()

        print("Descargando el video de Youtube...")
        fichero = download_from_url(url, artist_name)
        print(f"La descarga de {url} se ha completado con éxito.")
        print(fichero)
        print("Separando voz del fichero")
        subprocess.run(["python", "-m", "demucs.separate", fichero, "-o", artist_path,"--two-stems=vocals", "-d" ,"cpu" ])
        print("Fin Separando voz del fichero")

        # Mover y renombrar el archivo vocals.wav
        song_name = os.path.splitext(os.path.basename(fichero))[0]
        song_path = os.path.join(artist_path,"htdemucs", song_name)
        vocals_path = os.path.join(song_path, "vocals.wav")
        new_vocals_path = os.path.join(artist_path, song_name + " - Vocals.wav")
        os.remove(fichero)
        os.rename(vocals_path, new_vocals_path)

        # Eliminar la carpeta de la canción que contiene el segundo fichero
        os.remove(os.path.join(song_path, "no_vocals.wav"))
        os.rmdir(song_path)
        os.rmdir(os.path.join(artist_path,"htdemucs"))

        # Crea un objeto AudioSegment a partir del archivo
        audio_segment = AudioSegment.from_file(new_vocals_path, format='wav')
            
        # Divide el archivo en segmentos de 15 segundos
        segmentos = audio_segment[::15000]
            
        # Recorre los segmentos y los exporta a archivos separados
        for i, segmento in enumerate(segmentos):                
            # Define el nombre del archivo de salida
            nombre_archivo_salida = os.path.join(artist_path,new_vocals_path + f' - segmento_{i+1}.wav')
                
            # Verifica si el archivo de salida ya existe y le cambia el nombre para evitar sobrescribirlo
            if os.path.exists(nombre_archivo_salida):
                j = 1
                while True:
                    nombre_archivo_salida = os.path.join(artist_path, f'segmento_{i+1}_{j}.wav')
                    if not os.path.exists(nombre_archivo_salida):
                        break
                    j += 1
            
            # Exporta el segmento a un archivo WAV
            segmento.export(nombre_archivo_salida, format='wav')
            print(f'Segmento {i+1} exportado a: {nombre_archivo_salida}')
        os.remove(new_vocals_path)

if __name__ == "__main__":
    main()
