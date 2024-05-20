import random
from Canton import Canton
import matplotlib.pyplot as plt
import numpy as np

class Pais:

    def __init__(self):
        self.cantones = []
        self.numeroDeCantones = 0
    
    def llenePais(self, cantones):
        with open(cantones, 'r') as archivo:
            numero = 1
            for linea in archivo:
                nombre = linea.strip()
                canton = Canton(nombre, numero)
                self.cantones.append(canton)
                numero += 1
                
            self.numeroDeCantones = numero-1

    def asigneVecinos(self, vecinos):
        with open(vecinos, 'r') as archivo:
            for linea in archivo:
                cantones = linea.strip().split(',')
                nombreCanton = cantones[0]
                nombresVecinos = cantones[1:]

                for canton in self.cantones:
                    if canton.getNombre() == nombreCanton:
                        canton.vecinos = [vecino for vecino in self.cantones if vecino.getNombre() in nombresVecinos]
                        break

    def hayGanador(self):
        for canton in self.cantones:
            if(canton.getNumeroDeCantonesConquistados() == self.numeroDeCantones):
                print(canton.getNombre() + ' HA GANADO!')
                return True
                        
        return False
    
    def hayCantonDerrotado(self):
        for canton in self.cantones:
            if(canton.estaDerrotado()):
                return True

        return False
    
    def cantonesEnAtaque(self):
        cantonDondeAtaca = random.choice(self.cantones)
        cantonAtacante = cantonDondeAtaca.conquistador
        cantonAtacado = random.choice(cantonDondeAtaca.vecinos)

        while(cantonAtacado.conquistador == cantonAtacante):
            cantonDondeAtaca = random.choice(self.cantones)
            cantonAtacado = random.choice(cantonDondeAtaca.vecinos)

        return cantonAtacante, cantonAtacado

    def ataque(self):
        cantonAtacante, cantonAtacado = self.cantonesEnAtaque()
        cantonAtacante.ataca(cantonAtacado)
        cantonAtacado.esAtacado(cantonAtacante)

    def estadistica(self):
        for canton in self.cantones:
            if canton.getNumeroDeCantonesConquistados() != 0:
                print(canton.getNombre() + ': ' + str(canton.getNumeroDeCantonesConquistados()), end=', ')
        print('\n')