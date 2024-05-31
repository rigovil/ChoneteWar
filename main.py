import datetime, time
from Pais import Pais

def main():
    CostaRica = Pais()
    CostaRica.llenePais('Cantones.txt')
    CostaRica.asigneVecinos('Vecinos.txt')
    CostaRica.restaureAtaques()

    print('Costa Rica ha entrado en guerra\n')

    while(CostaRica.hayGanador() == False):
        CostaRica.ataque()
        # time.sleep(3600)
        print('ataque')
        time.sleep(5)
    
    print('La guerra ha terminado')

if __name__ == "__main__":
    main()