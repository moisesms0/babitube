
from pytube import YouTube,exceptions
import av
from src.utils import *
from tkinter import messagebox
import threading

# Primer paso al pulsar el boton de descargar, donde se comprueba si la url es valida y si hay canciones en la cola
def descargar():
    from src.gui import url_entry
    
    # Se obtiene la url escrita en el entry
    url = url_entry.get()



    if  len(cola) >= 1 and YouTube(url) == cola[-1]:
        messagebox.showerror("Error", "La canción ya se encuentra en la cola")
        return
    
    # Se comprueba que la url sea correcta
    try:
        cola.append(YouTube(url))
    except:
        messagebox.showerror("Error", "URL Inválida")
        return

    # Si hay canciones en la cola la comienza a descargar
    if len(cola) == 1:
        threading.Thread(target=descargar_siguiente).start()


# Se descargan las canciones de la cola, se convierten a mp3 y se borran en su version mp4
def descargar_siguiente():
    from src.gui import progress_value, status_label

    # Se guarda el primero en la cola
    video = cola[0]

    # Se sustituyen valores que puedan dar errores en el nombre
    try:
        formatted_filename = video.title.replace("@","").replace(".","")
    except exceptions.PytubeError as e:
        status_label.config(text=f"Error al descargar")
        cola.pop(0)
        return   

    status_label.config(text=f"Descargando {formatted_filename}...")

    # Descarga el video
    audio = video.streams.get_lowest_resolution().download();
    new_name = os.path.splitext(audio)

    # Creamos un objeto de tipo contenedor AV para leer el archivo de entrada
    container = av.open(new_name[0]+'.mp4')
    audio_stream = next(s for s in container.streams if s.type == 'audio')

    # crear un objeto para el archivo de audio de salida
    output = av.open(os.path.join(carpeta_destino, f"{formatted_filename}.mp3"), 'w')

    # agregar un stream de audio al archivo de salida
    output_stream = output.add_stream('mp3')
    total_frames = container.streams.audio[0].frames
    frames_converted = 0


    # iterar a través de los paquetes de audio y decodificarlos, luego codificarlos como mp3 y escribirlos en el archivo de salida

    for packet in container.demux(audio_stream):
        for frame in packet.decode():
            encoded_packet = output_stream.encode(frame)
            if encoded_packet:
                try:
                    output.mux(encoded_packet)
                except av.error.ValueError as e:

                    return

            frames_converted += 1
            progress_value.set(int((frames_converted / total_frames) * 100))


    # Cerrar los archivos de entrada y salida, borrar el archivo mp4
    container.close()
    output.close()
    os.remove(new_name[0]+'.mp4')

    # Se elimina de la cola


    # Se muestra en la consola que se descargo correctamente (Para pruebas)
    print(f"{formatted_filename} Se ha descargado correctamente")
    status_label.config(text=f"{formatted_filename} Se ha descargado correctamente")
    cola.pop(0)
    progress_value.set(0)

    # Si hay otra cancion en la cola se actualiza el estado y se comienza a descargar la siguiente
    if len(cola) > 0:
        threading.Thread(target=descargar_siguiente).start()



