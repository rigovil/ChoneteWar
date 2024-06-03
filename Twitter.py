import tweepy

class Twitter:

    def __init__(self):
        self.__clientV1 = None
        self.__clientV2 = None
        self.__tweetUltimoAtaque = 0
        self.twitterLog = '/home/chonetewar/ChoneteWar/twitter.log'                     # produccion
        self.mapaCostaRica = '/home/chonetewar/ChoneteWar/costarica.png'                # produccion
        self.mapaCostaRicaGuerra = '/home/chonetewar/ChoneteWar/costarica_guerra.png'   # produccion
        self.mapaCostaRicaAtaque = '/home/chonetewar/ChoneteWar/costarica_ataque.png'   # produccion
        self.__file = open(self.twitterLog, "a")                                        # produccion

    def authenticate(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )
        self.__clientV1 = tweepy.API(auth)
        self.__clientV2 = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

    def tweetInicio(self):
        try:
            media = self.__clientV1.media_upload(filename=self.mapaCostaRica)
            mediaId = media.media_id
            log = self.__clientV2.create_tweet(text='Ha comenzado la guerra civil en Costa Rica y los 84 cantones se disputarán entre sí el territorio costarricense.', media_ids=[mediaId])
            self.__file.write('LOG: ' + log + '\n')
        except:
            self.__file.write('EXC: tweetInicio\n')
    
    def tweetAtaque(self, ataque):
        try:
            media1 = self.__clientV1.media_upload(filename=self.mapaCostaRicaGuerra)
            media2 = self.__clientV1.media_upload(filename=self.mapaCostaRicaAtaque)
            mediaId1 = media1.media_id
            mediaId2 = media2.media_id
            log = self.__tweetUltimoAtaque = self.__clientV2.create_tweet(text=ataque, media_ids=[mediaId1, mediaId2])
            self.__file.write('LOG: ' + log + '\n')
        except:
            self.__file.write('EXC: tweetAtaque, param: ' + ataque + '\n')
    
    def tweetPosiciones(self, posiciones):
        try:
            tweetId = self.__tweetUltimoAtaque.data['id']
            log = self.__clientV2.create_tweet(text=posiciones, in_reply_to_tweet_id=tweetId)
            self.__file.write('LOG: ' + log + '\n')
        except:
            self.__file.write('EXC: tweetPosiciones, param: ' + posiciones + '\n')

    def tweetFinal(self, ganador):
        try:
            media = self.__clientV1.media_upload(filename=self.mapaCostaRicaGuerra)
            mediaId = media.media_id
            text = '¡La guerra ha terminado! ' + ganador + ' ha conquistado todo el territorio de Costa Rica.'
            log = self.__clientV2.create_tweet(text=text, media_ids=[mediaId])
            self.__file.write('LOG: ' + log + '\n')
        except:
            self.__file.write('EXC: tweetFinal, param: ' + ganador + '\n')