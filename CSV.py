import os
import csv

class CSV:

    def __init__ (self):
        self.__rutaHistorial = 'historial.csv'

    def existe(self):
        return os.path.isfile(self.__rutaHistorial)
    
    def crear(self):
        if not self.existe():
            with open(self.__rutaHistorial, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Fecha', 'CantonAtacante', 'CantonAtacado', 'CantonDisputado', 'CantonUtilizado', 'Independencia'])
            file.close()

    def ataque(self, fecha, atacante, atacado, disputado, utilizado, independencia):
        with open(self.__rutaHistorial, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([fecha, atacante, atacado, disputado, utilizado, independencia])
        file.close()

    def ataquesRegistrados(self):
        with open(self.__rutaHistorial, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            return [linea for linea in file]