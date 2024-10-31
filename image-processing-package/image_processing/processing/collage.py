#Work in progress
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np

def crear_collage(dataframe, columnas, filas, ancho_img=100, alto_img=100, titulo_collage=None):
    """
    Crea un collage de imágenes.
    
    Parámetros:
    - dataframe: DataFrame con 'nombre_imagen' (ruta a la imagen), 'titulo' (texto superior), y 'subtitulo' (texto inferior).
    - columnas: Número de columnas en el collage.
    - filas: Número de filas en el collage.
    - ancho_img: Ancho de cada imagen (opcional).
    - alto_img: Alto de cada imagen (opcional).
    - titulo_collage: Título general para el collage (opcional).
    """
    
    # Tamaño del collage
    fig, axes = plt.subplots(filas, columnas, figsize=(columnas * (ancho_img/100), filas * (alto_img/100)))
    fig.suptitle(titulo_collage, fontsize=16) if titulo_collage else None #podemos especificar tamanio de fuente
    
    # Ajuste para cuando solo haya una fila o columna (ejes no iterables)
    axes = np.array(axes).reshape(filas, columnas)
    
    # Iterar sobre cada imagen y su posición en el grid
    idx = 0
    for i in range(filas):
        for j in range(columnas):
            ax = axes[i, j]
            ax.axis("off")  # Quitamos ejes
            
            if idx < len(dataframe):
                # Cargamos la imagen
                img_data = dataframe.iloc[idx]
                imagen = Image.open(img_data['nombre_imagen']).resize((ancho_img, alto_img))
                
                # Mostrar la imagen en el eje
                ax.imshow(imagen)
                
                # Añadir título superior e inferior
                ax.set_title(img_data['titulo'], fontsize=10, color='blue')
                ax.text(0.5, -0.1, img_data['subtitulo'], va='top', ha='center', fontsize=8, color='gray', transform=ax.transAxes)
                
            idx += 1
    
    # Ajuste de espacio
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.show()

# Ejemplo de uso:
'''data = {
    'nombre_imagen': ['ruta/imagen1.jpg', 'ruta/imagen2.jpg', 'ruta/imagen3.jpg', 'ruta/imagen4.jpg'],
    'titulo': ['Título 1', 'Título 2', 'Título 3', 'Título 4'],
    'subtitulo': ['Subtítulo 1', 'Subtítulo 2', 'Subtítulo 3', 'Subtítulo 4']
}
df = pd.DataFrame(data)
crear_collage(df, columnas=2, filas=2, ancho_img=150, alto_img=150, titulo_collage="Mi Collage")'''
