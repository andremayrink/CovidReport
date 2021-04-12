import tweepy as tw
import json
import datetime as dt
from  utils.datahora import DataHoraUtils

class Tweeter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.setDataInicial(dt.datetime(2020,1,1))
        self._inicialize()

    def _inicialize(self):
        self._auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        self._auth.set_access_token(self.access_token, self.access_token_secret)
        self._api = tw.API(self._auth, wait_on_rate_limit=True)

    def setDataInicial(self, dataInicial):
        self._dataInicial = dataInicial

    def setLang(self, lang):
        self._lang = lang

    def getSeachCursor(self, itenCount, palavrasChave):
        tweets = tw.Cursor(self._api.search,
              q=" OR ".join(palavrasChave),
              lang=self._lang,
              since=self._dataInicial, 
              tweet_mode="extended").items(itenCount)
        return tweets
    
    def getTweetsFromCursor(self, cursor):
        tweets = {}
        for t in cursor:
            tweet = {}
            tweet["id"] = t.id_str
            tweet["nomeAutor"] = t.author.name
            tweet["nomeTelaAutor"] = t.author.screen_name
            
            if (t.author.location):
                tweet["localAutor"] = t.author.location
            else: tweet["localAutor"] = ""
            
            if (t.place):
                tweet["localTweet"] = t.place.full_name
            else: tweet["localTweet"] = ""
            du = DataHoraUtils()
            tweet["data"] = du.datetime_from_utc_to_local(t.created_at)
            key = tweet["data"].strftime("%d_%m_%Y")
            tweet["data"] = tweet["data"].strftime("%d/%m/%Y %H:%M%S")
            tweet["texto"] = t.full_text
            tweet["metrics"] = {"retweetado":t.retweet_count,
                                "favoritado":t.favorite_count}
            tweet["retweetado"] = t.retweeted
            
            if not(key in tweets.keys()):
                tweets[key] = []
            tweets[key].append(tweet)
        return tweets