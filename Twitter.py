import tweepy

class Twitter:

    def __init__(self):
        self.__clientV1 = None
        self.__clientV2 = None
        self.__tweetUltimoAtaque = 0
        self.mapaCostaRica = 'costarica.png'
        self.mapaCostaRicaGuerra = 'costarica_guerra.png'
        self.mapaCostaRicaAtaque = 'costarica_ataque.png'

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
        media = self.__clientV1.media_upload(filename=self.mapaCostaRica)
        mediaId = media.media_id
        self.__clientV2.create_tweet(text='Ha comenzado la guerra civil en Costa Rica y los 84 cantones se disputarán entre sí el territorio costarricense.', media_ids=[mediaId])
    
    def tweetAtaque(self, ataque):
        media1 = self.__clientV1.media_upload(filename=self.mapaCostaRicaGuerra)
        media2 = self.__clientV1.media_upload(filename=self.mapaCostaRicaAtaque)
        mediaId1 = media1.media_id
        mediaId2 = media2.media_id
        self.__tweetUltimoAtaque = self.__clientV2.create_tweet(text=ataque, media_ids=[mediaId1, mediaId2])
    
    def tweetPosiciones(self, posiciones):
        tweetId = self.__tweetUltimoAtaque.data['id']
        self.__clientV2.create_tweet(text=posiciones, in_reply_to_tweet_id=tweetId)

    def tweetFinal(self, ganador):
        media = self.__clientV1.media_upload(filename=self.mapaCostaRicaGuerra)
        mediaId = media.media_id
        text = '¡La guerra ha terminado! ' + ganador + ' ha conquistado todo el territorio de Costa Rica.'
        self.__clientV2.create_tweet(text=text, media_ids=[mediaId])