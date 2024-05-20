class Canton:

    def __init__(self, nombre = '', numeroDeCanton = 0, vecinos = []):
        self.__nombre = nombre
        self.__numeroDeCanton = numeroDeCanton
        self.__numeroDeCantonesConquistados = 1
        self.__cantonesConquistados = []
        self.__derrotado = False
        self.__conquistado = False
        self.conquistador = self
        self.vecinos = vecinos
        self.__cantonesConquistados.append(self)

    def __eq__(self, canton):
        return self.__nombre == canton.getNombre()
    
    def __str__(self):
        return("Nombre: " + self.__nombre + ", conquistador: " + self.conquistador.getNombre())

    def getNombre(self):
        return self.__nombre

    def getNumeroDeCanton(self):
        return self.__numeroDeCanton
    
    def getNumeroDeCantonesConquistados(self):
        return self.__numeroDeCantonesConquistados
    
    def getCantonesConquistados(self):
        return self.__cantonesConquistados
    
    def estaDerrotado(self):
        return self.__derrotado
    
    def estaConquistado(self):
        return self.__conquistado

    def pierdeCanton(self, cantonPerdido):
        for canton in self.__cantonesConquistados:
            if(canton == cantonPerdido):
                self.__cantonesConquistados.remove(canton)
                self.__numeroDeCantonesConquistados -= 1
                break
        
        if(self.__numeroDeCantonesConquistados == 0):
            self.__derrotado = True       

    def ataca(self, canton):
        self.__numeroDeCantonesConquistados += 1
        self.__cantonesConquistados.append(canton)

    def esAtacado(self, atacante):
        self.conquistador.pierdeCanton(self)

        if(atacante == self):
            print(self.__nombre + ' ha atacado a ' + self.conquistador.getNombre() + ' y ha recuperado su propio territorio.')
        else:
            print(atacante.getNombre() + ' ha atacado a ' + self.conquistador.getNombre() + ' y le ha quitado el territorio de ' + self.__nombre)

        self.conquistador = atacante