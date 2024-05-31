import time
from Pais import Pais

def main():
    CostaRica = Pais()
    CostaRica.llenePais('/home/chonetewar/ChoneteWar/Cantones.txt')       # produccion
    CostaRica.asigneVecinos('/home/chonetewar/ChoneteWar/Vecinos.txt')    # produccion
    CostaRica.restaureAtaques()

    print('Costa Rica ha entrado en guerra\n')

    while(CostaRica.hayGanador() == False):
        CostaRica.ataque()
        time.sleep(3600)  # produccion
    
    print('La guerra ha terminado')

if __name__ == "__main__":
    main()