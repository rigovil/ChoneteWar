import time
from Pais import Pais
from datetime import datetime

def espera():
    delta = 60 - datetime.now().minute
    time.sleep(delta * 60)

def main():
    CostaRica = Pais()
    CostaRica.llenePais('/home/chonetewar/ChoneteWar/Cantones.txt')       # produccion
    CostaRica.asigneVecinos('/home/chonetewar/ChoneteWar/Vecinos.txt')    # produccion
    CostaRica.restaureAtaques()

    print('Costa Rica ha entrado en guerra\n')

    while(CostaRica.hayGanador() == False):
        CostaRica.ataque()
        # espera()  # produccion
        input('ataque')
        # time.sleep(2)
    
    print('La guerra ha terminado')

if __name__ == "__main__":
    main()