import tkinter as tk
from tkinter import ttk, filedialog
import os
from src.download import *


# Crea la ventana, pone icono, vuelve la ventana no redimensionable, pone el tiulo y fondo
window = tk.Tk()
progress_value = tk.DoubleVar()
window.iconbitmap('babiboy.ico')
window.geometry("450x306")
window.resizable(False, False)
window.title("Babilawi's Youtube Downloader")
window.config(bg='#262626')

# Crea el formulario
form_frame = tk.Frame(window, bg='#262626')
form_frame.pack(expand=True, fill='both', padx=20, pady=(20,0))
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
download_button.pack(pady=(0,0))

# Agrega un label de estado
status_label = tk.Label(form_frame, text='Esperando descarga...', bg='#262626', fg='white')
status_label.pack( fill='x', padx=0, pady=(15))

# Crea un frame para la barra de progreso
progress_frame = tk.Frame(window, bg='#262626')
progress_frame.pack(expand=True, fill='both', padx=0, pady=0)

style.configure('green.Horizontal.TProgressbar', troughcolor='#262626', background='green', bordercolor='#262626',borderwidth=1)

progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate', length=450, variable=progress_value, style="green.Horizontal.TProgressbar")
progress_bar.pack(side='bottom', pady=(0,0))