from PIL import Image, ImageEnhance
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys
from sklearn.cluster import KMeans

def load_image(path):
    return Image.open(path)

def save_image(image, path):
    image.save(path)

def load_image_cv2(path):
    return cv2.imread(path)

def save_image_cv2(image, path):
    cv2.imwrite(path, image)

def get_unique_colors(image):
    colors = image.getcolors(image.size[0] * image.size[1])
    unique_colors = [color[1] for color in colors]
    return unique_colors

def assign_random_colors(image, unique_colors):
    width, height = image.size
    pixel_data = image.load()
    color_map = {color: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for color in unique_colors}

    for y in range(height):
        for x in range(width):
            current_color = pixel_data[x, y]
            if current_color in color_map:
                pixel_data[x, y] = color_map[current_color]
    
    return image

def enhance_borders(image):
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invertir la imagen (líneas negras serán blancas)
    inverted_image = cv2.bitwise_not(gray_image)
    
    # Aplicar una dilatación para hacer las líneas más gruesas
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(inverted_image, kernel, iterations=2)
    
    # Invertir la imagen de nuevo para tener las líneas negras
    enhanced_borders = cv2.bitwise_not(dilated_image)
    
    # Crear una máscara donde las líneas negras estén presentes
    mask = (enhanced_borders == 0)
    
    # Copiar la imagen original
    enhanced_image = image.copy()
    
    # Aplicar la máscara a cada canal de color (R, G, B)
    enhanced_image[mask] = [0, 0, 0]
    
    return enhanced_image

def convert_gray_to_black(image, threshold=128):
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Crear una máscara para los píxeles que están entre negro y gris (threshold)
    mask = gray_image < threshold
    
    # Convertir los píxeles que están en el rango de gris a negro
    image[mask] = [0, 0, 0]
    
    return image

def colorize_non_matching_pixels(image, target_colors):
    # Convertir la imagen a RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Crear una máscara para los píxeles que no coinciden con los colores objetivo
    mask = np.zeros_like(image_rgb[:, :, 0], dtype=bool)
    for color in target_colors:
        mask |= np.all(image_rgb == color, axis=2)

    # Convertir los píxeles no coincidentes a negro
    image[~mask] = [0, 0, 0]

    return image

def thin_lines(image, kernel_size=3, iterations=1):
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral para obtener una imagen binaria con las líneas en blanco
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    
    # Definir el kernel de erosión
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # Aplicar erosión para adelgazar las líneas
    thinned_image = cv2.erode(binary_image, kernel, iterations=iterations)
    
    # Convertir la imagen a color para visualización
    thinned_image = cv2.cvtColor(thinned_image, cv2.COLOR_GRAY2BGR)
    
    return thinned_image

def generate_unique_color(used_colors):
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color not in used_colors:
            used_colors.add(color)
            return color

def count_and_color_cantones(image):
    colors_rgb = []
    print(len(colors_rgb))

    # Optional: Visualize the colors
    # fig, ax = plt.subplots(1, figsize=(12, 6), subplot_kw=dict(xticks=[], yticks=[],
    #                                                         frame_on=False))
    # ax.imshow([colors_rgb], aspect='auto')
    # plt.show()

    # Convertir la imagen adelgazada a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral para obtener una imagen binaria con las líneas en blanco
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    
    # Encontrar contornos en la imagen binaria
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Crear una copia de la imagen original para pintar los cantones
    colored_image = image.copy()

    # Asignar un color aleatorio a cada cantón y pintarlo
    for contour in contours:
        color = colors_rgb.pop(random.randint(0,len(colors_rgb)-1))
        cv2.drawContours(colored_image, [contour], -1, color, thickness=cv2.FILLED)
    
    # Contar el número de cantones encontrados
    num_cantones = len(contours)
    return num_cantones, colored_image

def remove_black_pixels(image):
    # Convertir la imagen a RGBA si no lo es
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Crear una máscara donde los píxeles negros son True
    black_mask = np.all(image[:, :, :3] == [0, 0, 0], axis=-1)
    
    # Establecer el canal alfa de los píxeles negros a 0 (transparente)
    image[black_mask, 3] = 0
    
    return image

def count_and_number_cantones(image):
    # Convertir la imagen adelgazada a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral para obtener una imagen binaria con las líneas en blanco
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    
    # Encontrar contornos en la imagen binaria
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Crear una copia de la imagen original para pintar los números de los cantones
    numbered_image = image.copy()
    
    # Asignar un número único a cada cantón y dibujarlo
    for i, contour in enumerate(contours):
        # Calcular el momento del contorno para encontrar el centroide
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # Asignar el número y dibujarlo en el centroide
        number = str(i + 1)
        cv2.putText(numbered_image, number, (cX - 10, cY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Contar el número de cantones encontrados
    num_cantones = len(contours)
    
    return num_cantones, numbered_image

def replace_color(image, target_color, new_color):
    # Convertir los colores a numpy arrays para facilitar la comparación
    target_color= np.array(list(reversed(target_color)), dtype=np.uint8)
    new_color = np.array(list(reversed(new_color)), dtype=np.uint8)
    
    # Iterar sobre todos los píxeles de la imagen
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            # Obtener el color del píxel actual
            current_color = image[y, x]
            
            # Verificar si el color del píxel actual coincide con el color objetivo
            if np.all(current_color == target_color):
                # Reemplazar el color del píxel actual con el nuevo color
                image[y, x] = new_color
    
    return image

def show_image(image, title='Image'):
    # Convertir la imagen de BGR a RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis('off')
    plt.show()

def zoom_at(img, zoom=1, angle=0, coord=None):  
    cy, cx = [ i/2 for i in img.shape[:-1] ] if coord is None else coord[::-1]
    rot_mat = cv2.getRotationMatrix2D((cx,cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR) 
    return result

def recolor_image(image_a_path, image_b_path, output_path):
    # Abre las dos imágenes
    image_a = Image.open(image_a_path)
    image_b = Image.open(image_b_path)
    
    # Verifica que las imágenes tengan el mismo tamaño
    if image_a.size != image_b.size:
        raise ValueError("Las imágenes deben tener el mismo tamaño.")
    
    # Convierte las imágenes a modo RGB si no lo están
    image_a = image_a.convert("RGB")
    image_b = image_b.convert("RGB")
    
    # Obtiene los datos de píxeles de ambas imágenes
    pixels_a = image_a.load()
    pixels_b = image_b.load()
    
    # Define los colores que no deben cambiar
    colors_to_keep = [(137, 234, 253), (255, 255, 255)]
    
    # Recorre todos los píxeles
    for x in range(image_a.width):
        for y in range(image_a.height):
            if pixels_a[x, y] not in colors_to_keep:
                pixels_a[x, y] = pixels_b[x, y]
    
    # Guarda la imagen resultante
    image_a.save(output_path)

def improve_image_quality(input_image_path, output_image_path):
    # Cargar la imagen
    image = cv2.imread(input_image_path)
    
    # Convertir a escala de grises y aplicar ecualización del histograma para mejorar el contraste
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    
    # Convertir de nuevo a color
    color_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)
    
    # Aplicar suavizado para reducir ruido
    denoised_image = cv2.fastNlMeansDenoisingColored(color_image, None, 10, 10, 7, 21)
    
    # Convertir a PIL Image para aplicar realce de nitidez
    pil_image = Image.fromarray(cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Sharpness(pil_image)
    enhanced_image = enhancer.enhance(2.0)  # Aumentar la nitidez

    # Convertir de vuelta a formato OpenCV
    final_image = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
    
    # Guardar la imagen resultante
    cv2.imwrite(output_image_path, final_image)

# Carga la imagen del mapa
image_path = 'costarica_ataque.png'
image = load_image_cv2(image_path)

# Obtén los colores únicos presentes en la imagen (presumiblemente un color por cantón)
# unique_colors = get_unique_colors(image)

# Asigna colores aleatorios a cada cantón
# new_image = assign_random_colors(image, unique_colors)

# Mejorar los bordes de los cantones
# enhanced_image = enhance_borders(image)

# Convertir píxeles gris a negro
# threshold_value = 20  # Ajusta este valor según sea necesario
# converted_image = convert_gray_to_black(image, threshold_value)

# Lista de colores RGB a preservar
# target_colors = [
#     [253, 204, 138],    
#     [252, 141, 89],    
#     [227, 74, 51],
#     [254, 240, 217],
#     [179, 0, 0]
# ]

# Colorear de negro los píxeles que no coinciden con los colores objetivo
# processed_image = colorize_non_matching_pixels(image, target_colors)

# Reducir el grosor de las líneas divisorias entre los cantones
# thinned_image = thin_lines(image, kernel_size=3, iterations=2)

# Colorizar los cantones con el color especificado
# background_color = (185, 122, 87)
# colorized_image = colorize_cantones(image, background_color)

# Reducir el grosor de las líneas divisorias entre los cantones
# thinned_image = thin_lines(image)

# Eliminar los píxeles negros
# image_without_black = remove_black_pixels(image)

# Guarda la nueva imagen con los colores asignados
output_path = 'costarica_ataque_HQ.png'
# save_image(new_image, output_path)
# save_image_cv2(enhanced_image, output_path)
# save_image_cv2(converted_image, output_path)
# save_image_cv2(processed_image, output_path)
# save_image_cv2(thinned_image, output_path)
# save_image_cv2(colorized_image, output_path)
# save_image_cv2(thinned_image, output_path)
# save_image_cv2(image_without_black, output_path)

# zoomed_image = zoom_at(image, 1.5, coord=(120, 100))
# save_image_cv2(zoomed_image, output_path)

# Colores en formato RGB
# target_color = [23, 33, 203]  # Color negro que queremos reemplazar
# new_color = [22, 193, 101]  # Color blanco que queremos poner

# # Reemplazar el color
# image_with_replaced_color = replace_color(image, target_color, new_color)
# show_image(image_with_replaced_color, title='Imagen con Color Reemplazado')

# Guardar la imagen procesada
# save_image_cv2(image_with_replaced_color, output_path)

# Contar el número de cantones y colorearlos
# num_cantones, colored_image = count_and_color_cantones(image)
# print(f"El número de cantones es: {num_cantones}")
# save_image_cv2(colored_image, output_path)

# Contar el número de cantones y numerarlos
# num_cantones, numbered_image = count_and_number_cantones(image)
# print(f"El número de cantones es: {num_cantones}")
# save_image_cv2(numbered_image, output_path)

# Colorear un mapa con otro mapa excepto el mar
# recolor_image('costarica.png', 'img/costarica_prueba.png', 'costarica2.png')

# Mejorar la calidad de una imagen
improve_image_quality(image_path, output_path)