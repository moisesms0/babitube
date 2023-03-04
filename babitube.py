from pytube import YouTube
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import av
import threading

cola = []

carpeta_destino = os.path.join(os.path.expanduser("~"), "Music")

# Primer paso al pulsar el boton de descargar, donde se comprueba si la url es valida y si hay canciones en la cola
def descargar():
    
    # Se obtiene la url escrita en el entry
    url = url_entry.get()

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
    
    # Se guarda el primero en la cola
    video = cola[0]

    # Se sustituyen valores que puedan dar errores en el nombre
    formatted_filename = video.title.replace("___","_").replace("__","_")

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

    # iterar a través de los paquetes de audio y decodificarlos, luego codificarlos como mp3 y escribirlos en el archivo de salida
    for packet in container.demux(audio_stream):
        for frame in packet.decode():
            encoded_packet = output_stream.encode(frame)
            if encoded_packet:
                output.mux(encoded_packet)

    # Cerrar los archivos de entrada y salida, borrar el archivo mp4
    container.close()
    output.close()
    os.remove(new_name[0]+'.mp4')

    # Se elimina de la cola
    cola.pop(0)

    # Se muestra en la consola que se descargo correctamente (Para pruebas)
    print(f"{formatted_filename} Se ha descargado correctamente")

    # Si hay otra cancion en la cola se actualiza el estado y se comienza a descargar la siguiente
    if len(cola) > 0:
        actualizar_estado()
        threading.Thread(target=descargar_siguiente).start()

# Crea la ventana, pone icono, vuelve la ventana no redimensionable, pone el tiulo y fondo
window = tk.Tk()
window.iconbitmap('babiboy.ico')
window.geometry("450x280")
window.resizable(False, False)
window.title("Babilawi's Youtube Downloader")
window.config(bg='#262626')

# Crea el formulario
form_frame = tk.Frame(window, bg='#262626')
form_frame.pack(expand=True, fill='both', padx=20, pady=(20,10))
url_label = tk.Label(form_frame, text="Ingresa la URL del video de YouTube:", bg='#262626', fg='white', font=('Arial', 14))
url_entry = tk.Entry(form_frame, bg='#333333', fg='white', insertbackground='white', font=('Arial', 12), width=35)

# Estilo personalizado para el botón
style = ttk.Style()
style.theme_use('clam')
style.configure('Custom.TButton', background='#f44336', foreground='white', font=('Arial', 12), padding=10)
style.map('Custom.TButton', background=[('active', '#ff5722')])

# Crear el botón utilizando el estilo personalizado
download_button = ttk.Button(form_frame, text="Descargar", style='Custom.TButton', command=descargar)

# al pulsar el boton de cambiar carpeta actualiza la ruta a la seleccionada, en caso de no seleccionar se pone la ruta por defecto
def configurar_carpeta_destino():
    global carpeta_destino

    carpeta_destino = filedialog.askdirectory()
    if not carpeta_destino:
        carpeta_destino = os.path.join(os.path.expanduser("~"), "Music")
    else:
        carpeta_destino_label.config(text=f'Carpeta de destino: {carpeta_destino}')

# Crea un label y un entry para mostrar la carpeta de destino seleccionada
carpeta_destino_label = tk.Label(form_frame, text="Carpeta de destino:", bg='#262626', fg='white', font=('Arial', 12))
carpeta_destino_label.config(text=f'Carpeta de destino: {carpeta_destino}')

# Agrega un botón para seleccionar la carpeta de destino
seleccionar_carpeta_button = ttk.Button(form_frame, text="Seleccionar Carpeta", style='Custom.TButton', command=configurar_carpeta_destino)

# Agrega los modulos del formulario
url_label.pack(pady=(0,10))
url_entry.pack(pady=(0,10))
carpeta_destino_label.pack(pady=(0,10))
seleccionar_carpeta_button.pack(pady=(0,20))
download_button.pack()

# Agrega un label de estado
status_label = tk.Label(window, text='Esperando descarga...', bg='#262626', fg='white')
status_label.pack(side='bottom', fill='x', padx=10, pady=10)

# Define una función para actualizar el estado
def actualizar_estado():
    if len(cola) == 0:
        status_label.config(text='Esperando descarga...')
    else:
        status_label.config(text=f'Descargando {cola[0].title}...')
    window.after(100, actualizar_estado)

# Crea un bucle y comienza a actualizar el estado

actualizar_estado()
window.mainloop()