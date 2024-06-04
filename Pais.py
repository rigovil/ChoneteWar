import time
import random
import locale
from CSV import CSV
from Mapa import Mapa
from Canton import Canton
from Twitter import Twitter
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Pais:

    def __init__(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        self.fecha = datetime.now()
        self.cantones = []
        self.numeroDeCantones = 0
        self.probabilidadIndependencia = 0.08
        self.CSV = CSV()
        self.Mapa = Mapa()
        self.twitter = Twitter()

        self.twitter.authenticate(
            'akTdU3YQZCzVcjmymQDwTzN7t',
            'EqtQ8fyhzy4BaJOMbPttH4h9p4Jb0PObIdZPYCz7wsm91jvTwc',
            '1795559890909376512-UvBF2aV2rld2jmHnIXvLKcWzklwPRR',
            'wQxwx4ZQsGljdqSnZk5xgK91NlRDZyeNFoTMpisnDvCFA'
        )

    def getCanton(self, nombre):
        for canton in self.cantones:
            if(canton.getNombre() == nombre):
                return canton
    
    def hayGanador(self):
        for canton in self.cantones:
            if(canton.getNumeroDeCantonesConquistados() == self.numeroDeCantones):
                self.twitter.tweetFinal(canton.getNombre())   # produccion
                return True
                        
        return False

    def hayCantonDerrotado(self):
        for canton in self.cantones:
            if(canton.estaDerrotado()):
                return True

        return False
    
    def llenePais(self, cantones):
        with open(cantones, 'r', encoding="utf-8") as archivo:
            numero = 1
            for linea in archivo:
                datos = linea.strip().split(',')
                nombre = datos[0]
                colores = list(map(int, datos[1:]))
                canton = Canton(nombre, numero, colores)
                self.cantones.append(canton)
                numero += 1
                
            self.numeroDeCantones = numero-1

        self.Mapa.guardePixeles(self.cantones)

    def asigneVecinos(self, vecinos):
        with open(vecinos, 'r', encoding="utf-8") as archivo:
            for linea in archivo:
                cantones = linea.strip().split(',')
                nombreCanton = cantones[0]
                nombresVecinos = cantones[1:]

                for canton in self.cantones:
                    if canton.getNombre() == nombreCanton:
                        canton.vecinos = [vecino for vecino in self.cantones if vecino.getNombre() in nombresVecinos]
                        break

    def posiciones(self):
        top = []
        for canton in self.cantones:
            top.append([canton.getNombre(), canton.getNumeroDeCantonesConquistados()])
        top = sorted(top, key=lambda x: x[1], reverse=True)

        posiciones = 'Tabla de posiciones según cantidad de cantones conquistados:\n\n'
        if len(top) >= 10:
            for i in range(0,10):
                posiciones = posiciones + top[i][0] + ': ' + str(top[i][1]) + '\n'
        else:
            for i in range(0,len(top)):
                posiciones = posiciones + top[i][0] + ': ' + str(top[i][1]) + '\n'

        return posiciones
    
    def cantonesEnAtaque(self):
        cantonDondeAtaca = random.choice(self.cantones)
        cantonAtacante = cantonDondeAtaca.conquistador
        cantonAtacado = random.choice(cantonDondeAtaca.vecinos)

        while(cantonAtacado.conquistador == cantonAtacante):
            cantonDondeAtaca = random.choice(cantonAtacante.getCantonesConquistados())
            cantonAtacado = random.choice(cantonDondeAtaca.vecinos)

        return cantonAtacante, cantonAtacado, cantonDondeAtaca

    def ataque(self):
        tipoAtaque = random.random()
        fecha = self.fecha.strftime("%B %Y").capitalize()
        tweet = fecha + '\n\n'

        if(tipoAtaque <= self.probabilidadIndependencia and not self.hayCantonDerrotado()):
            tipoAtaque = self.probabilidadIndependencia + 1

        if(tipoAtaque > self.probabilidadIndependencia):
            cantonAtacante, cantonAtacado, cantonDondeAtaca = self.cantonesEnAtaque()
            self.CSV.ataque(fecha, cantonAtacante.getNombre(), cantonAtacado.conquistador.getNombre(), cantonAtacado.getNombre(), cantonDondeAtaca.getNombre(), False)
            cantonAtacante.ataca(cantonAtacado)
            tweet += cantonAtacado.esAtacado(cantonAtacante, cantonDondeAtaca, self.Mapa)
        else:
            cantonAIndependizarse = random.choice([canton for canton in self.cantones if canton.estaDerrotado()])
            self.probabilidadIndependencia -= 0.0025
            self.CSV.ataque(fecha, cantonAIndependizarse.getNombre(), cantonAIndependizarse.conquistador.getNombre(), cantonAIndependizarse.getNombre(), cantonAIndependizarse.getNombre(), True)
            tweet += cantonAIndependizarse.seIndependiza(self.Mapa)

        self.twitter.tweetAtaque(tweet)                   # produccion
        self.twitter.tweetPosiciones(self.posiciones())   # produccion
        self.fecha = self.fecha + relativedelta(months=1)

    def restaureAtaques(self):
        if self.CSV.existe():
            fecha = ''
            for ataque in self.CSV.ataquesRegistrados():
                fecha, cantonAtacante, cantonAtacado, cantonDisputado, cantonUtilizado, independencia = ataque.split(',')
                cantonAtacante = self.getCanton(cantonAtacante.strip())
                cantonAtacado = self.getCanton(cantonAtacado.strip())
                cantonDisputado = self.getCanton(cantonDisputado.strip())
                cantonUtilizado = self.getCanton(cantonUtilizado.strip())

                if independencia.strip() == "False":
                    cantonAtacante.ataca(cantonDisputado)
                    cantonDisputado.esAtacado(cantonAtacante, cantonUtilizado, self.Mapa, colorearMapa = False)
                else:
                    cantonAtacante.seIndependiza(self.Mapa, colorearMapa = False)
                    self.probabilidadIndependencia -= 0.0025
            self.fecha = datetime.strptime(fecha.strip().lower(), '%B %Y') + relativedelta(months=1)
            self.Mapa.restaureMapa(self.cantones)

            if datetime.now().minute != 0: 
                delta = 60 - datetime.now().minute
                time.sleep(delta * 60)    # produccion
        else:
            self.CSV.crear()
            self.twitter.tweetInicio()    # produccion