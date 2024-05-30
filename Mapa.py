import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

class Mapa:

    def __init__(self):
        self.rutaOriginal = 'costarica.png'
        self.rutaAtaque = 'costarica_ataque.png'
        self.rutaMapaGuerra = 'costarica_guerra.png'
        self.imagenOriginal = cv2.imread(self.rutaOriginal)
        self.imagenMapaAtaque = cv2.imread(self.rutaOriginal)
        self.imagenMapaGuerra = self.imagenOriginal
        # self.fig, self.ax = plt.subplots()
        # self.image_rgb = self.ax.imshow(cv2.cvtColor(self.imagenMapaGuerra, cv2.COLOR_BGR2RGB))
        # plt.title('Estado de guerra actual')
        # plt.axis('off')
        # plt.show(block=False)

    def guardePixeles(self, cantones):
        for canton in cantones:          
            color = tuple(reversed(canton.getColor()))
            pixeles = np.column_stack(np.where(np.all(self.imagenOriginal == color, axis=-1)))
            if(len(pixeles) == 0):
                print(canton.getNombre())
            pixeles[:, [0, 1]] = pixeles[:, [1, 0]]
            canton.setPixeles(pixeles)

    def coloreeAtaque(self, colorAtacado, pixelesAtacado, colorAtacante, pixelesAtacante):
        imagen = self.imagenMapaGuerra
        color = np.array(colorAtacante[::-1], dtype=np.uint8)
        coordenadasX, coordenadasY = zip(*pixelesAtacado)

        self.muestreAtaque(pixelesAtacado, pixelesAtacante, colorAtacado, colorAtacante)

        imagen[coordenadasY, coordenadasX] = color

        cv2.imwrite(self.rutaMapaGuerra, imagen)
        self.imagenMapaGuerra = cv2.imread(self.rutaMapaGuerra)

    def muestreMapa(self):
        image_rgb = cv2.cvtColor(self.imagenMapaGuerra, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.title('Estado de guerra actual')
        plt.axis('off')
        plt.show(block=False)
        plt.pause(0.5)
        # plt.close()

    def actualiceMapa(self):
        self.image_rgb.set_array(cv2.cvtColor(self.imagenMapaGuerra, cv2.COLOR_BGR2RGB))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(0.05)

    def muestreAtaque(self, pixelesAtacado, pixelesAtacante, colorAtacado, colorAtacante, zoom=2.1):
        imagen = self.imagenMapaGuerra
        colorAtacado = tuple(reversed(colorAtacado))
        colorAtacante = tuple(reversed(colorAtacante))

        # Colorear los cantones en escala gris/azulado y aplicar efecto borroso y transparente, excepto los cantones involucrados en el ataque
        color1_mask = cv2.inRange(imagen, np.array(colorAtacado), np.array(colorAtacado))
        color2_mask = cv2.inRange(imagen, np.array(colorAtacante), np.array(colorAtacante))
        black_mask = cv2.inRange(imagen, np.array([0, 0, 0]), np.array([0, 0, 0]))
        sea_mask = cv2.inRange(imagen, np.array([253, 234, 137]), np.array([253, 234, 137]))        # Color BGR
        lines_mask = cv2.inRange(imagen, np.array([255, 255, 255]), np.array([255, 255, 255]))      # Color BGR
        kernel = np.ones((3, 3), np.uint8)
        dilated_color1_mask = cv2.dilate(color1_mask, kernel, iterations=1)
        dilated_color2_mask = cv2.dilate(color2_mask, kernel, iterations=1)
        dilated_combined_mask = cv2.bitwise_or(dilated_color1_mask, dilated_color2_mask)
        black_neighbors_mask = cv2.bitwise_and(black_mask, dilated_combined_mask)
        combined_mask = cv2.bitwise_or(cv2.bitwise_or(color1_mask, color2_mask), black_neighbors_mask)
        combined_mask = cv2.bitwise_or(combined_mask, sea_mask)
        combined_mask = cv2.bitwise_or(combined_mask, lines_mask)
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        imagen_gris = cv2.cvtColor(imagen_gris, cv2.COLOR_GRAY2BGR)
        imagen_gris[:, :, 0] = cv2.add(imagen_gris[:, :, 0], 20)
        imagen_gris = np.clip(imagen_gris, 0, 255)
        imagen_borrosa = cv2.GaussianBlur(imagen_gris, (3, 3), 0, borderType=cv2.BORDER_REFLECT)
        fondo_color = np.full_like(imagen_borrosa, (253, 234, 137))
        alpha = 0.2
        imagen_borrosa = cv2.addWeighted(imagen_borrosa, alpha, fondo_color, 1 - alpha, 0)
        imagen_resaltada = cv2.bitwise_and(imagen, imagen, mask=combined_mask)
        imagen_borrosa = cv2.bitwise_and(imagen_borrosa, imagen_borrosa, mask=cv2.bitwise_not(combined_mask))
        final_image = cv2.add(imagen_resaltada, imagen_borrosa)

        # Colorear el borde de color blanco del canton atacado
        bordered_image = final_image.copy()
        coord_set = set(map(tuple, pixelesAtacado))
        for (x, y) in coord_set:
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
            for nx, ny in neighbors:
                if (nx, ny) not in coord_set:
                    if np.array_equal(bordered_image[ny, nx], [0, 0, 0]):
                        bordered_image[ny, nx] = [255, 255, 255]

        # Colorear el borde del canton por donde ataca
        coord_set = set(map(tuple, pixelesAtacante))
        for (x, y) in coord_set:
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
            for nx, ny in neighbors:
                if (nx, ny) not in coord_set:
                    if np.array_equal(bordered_image[ny, nx], [255, 255, 255]):
                        intensidad_color = np.sum(colorAtacante) / 3
                        if intensidad_color > 100:
                            bordered_image[ny, nx] = [int(c * 0.5) for c in colorAtacante] # oscurece el color
                        else:
                            bordered_image[ny, nx] = [min(int(c * 2), 255) for c in colorAtacante]   # aclara el color

        # Generar una imagen mas cerca de los cantones involucrados en el ataque
        imagen_acercada = bordered_image.copy()
        region1_pts = np.array(pixelesAtacado, dtype=np.float32)
        region2_pts = np.array(pixelesAtacante, dtype=np.float32)
        region1_center = np.mean(region1_pts, axis=0)
        region2_center = np.mean(region2_pts, axis=0)
        coord = tuple((region1_center + region2_center) / 2) 
        h, w, _ = imagen_acercada.shape
        if coord is None:
            cx, cy = w / 2, h / 2
        else:
            cx, cy = [zoom * c for c in coord]
        img_zoomed = cv2.resize(imagen_acercada, (0, 0), fx=zoom, fy=zoom)
        h_zoom, w_zoom, _ = img_zoomed.shape
        x1 = int(round(cx - w / 2))
        x2 = int(round(cx + w / 2))
        y1 = int(round(cy - h / 2))
        y2 = int(round(cy + h / 2))
        x1 = max(0, x1)
        x2 = min(w_zoom, x2)
        y1 = max(0, y1)
        y2 = min(h_zoom, y2)
        img_cropped = img_zoomed[y1:y2, x1:x2]
        cv2.imwrite(self.rutaAtaque, img_cropped)
        self.imagenMapaAtaque = cv2.imread(self.rutaAtaque)

        # image_rgb = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
        # plt.imshow(image_rgb)
        # plt.title('Ataque')
        # plt.axis('off')
        # plt.show()

        # image_rgb = cv2.cvtColor(self.imagenMapaAtaque, cv2.COLOR_BGR2RGB)
        # plt.imshow(image_rgb)
        # plt.title('Ataque')
        # plt.axis('off')
        # plt.show(block=False)
        # plt.pause(0.1)
        # # plt.close()