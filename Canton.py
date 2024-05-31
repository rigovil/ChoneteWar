class Canton:

    def __init__(self, nombre = '', numeroDeCanton = 0, colores = []):
        self.__nombre = nombre
        self.__numeroDeCanton = numeroDeCanton
        self.__numeroDeCantonesConquistados = 1
        self.__cantonesConquistados = []
        self.__derrotado = False
        self.__conquistado = False
        self.__color = colores
        self.__pixeles = []
        self.conquistador = self
        self.vecinos = []

        self.__cantonesConquistados.append(self)

    def __eq__(self, canton):
        return self.__nombre == canton.getNombre()
    
    def __str__(self):
        return("Nombre: " + self.__nombre + ", conquistador: " + self.conquistador.getNombre())
    
    def printVecinos(self):
        string = ''
        for vecino in self.vecinos:
            string += vecino.getNombre() + ', '

        return string

    def getNombre(self):
        return self.__nombre

    def getNumeroDeCanton(self):
        return self.__numeroDeCanton
    
    def getNumeroDeCantonesConquistados(self):
        return self.__numeroDeCantonesConquistados
    
    def getCantonesConquistados(self):
        return self.__cantonesConquistados
    
    def getColor(self):
        return self.__color
    
    def getPixeles(self):
        return self.__pixeles
    
    def setPixeles(self, pixeles):
        self.__pixeles = pixeles

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
            
        tweet = ''
        if(self.__numeroDeCantonesConquistados == 0):
            self.__derrotado = True
            tweet = '\n' + self.__nombre + ' ha sido completamente derrotado.'

        return tweet  

    def ataca(self, canton):
        self.__numeroDeCantonesConquistados += 1
        self.__cantonesConquistados.append(canton)

    def esAtacado(self, atacante, dondeAtaca, mapa):
        mapa.coloreeAtaque(self.conquistador.getColor(), self.getPixeles(), atacante.getColor(), dondeAtaca.getPixeles())

        if(atacante == self):
            tweet = self.__nombre + ' ha atacado a ' + self.conquistador.getNombre() + ' y ha recuperado su propio territorio.'
        else:
            tweet = atacante.getNombre() + ' ha atacado a ' + self.conquistador.getNombre() + ' y le ha quitado el territorio de ' + self.__nombre + '.'

        tweet += self.conquistador.pierdeCanton(self)
        self.conquistador = atacante
        return tweet

    def seIndependiza(self, mapa):
        mapa.coloreeAtaque(self.conquistador.getColor(), self.__pixeles, self.__color, self.__pixeles)

        if(self.__numeroDeCantonesConquistados == 0):
            tweet = self.__nombre + ' se ha independizado de ' + self.conquistador.getNombre() + '.'
        else:
            tweet = self.__nombre + ' ha recuperado su territorio previamente ocupado por ' + self.conquistador.getNombre() + '.'

        tweet += self.conquistador.pierdeCanton(self)

        self.conquistador = self
        self.__derrotado = False
        self.__cantonesConquistados.append(self)
        self.__numeroDeCantonesConquistados += 1
        return tweet