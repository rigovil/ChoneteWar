from Pais import Pais

def main():
    CostaRica = Pais()
    CostaRica.llenePais('Cantones.txt')
    CostaRica.asigneVecinos('Vecinos.txt')

    print('Costa Rica ha entrado en guerra\n')

    while(CostaRica.hayGanador() == False):   
        # input() # descomentar para ir uno por uno
        CostaRica.ataque()

    print('La guerra ha terminado')

if __name__ == "__main__":
    main()