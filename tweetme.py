import tweepy
import os
import json

class tweetme:
    def __init__(self, config_file:str):
        try:
            with open(config_file) as configuration:
                settings = json.load(configuration)
                self.apiKey = settings['apiKey']
                self.apiSecretKey= settings['apiSecretKey']
                self.accessToken = settings['accessToken']
                self.accessTokenSecret = settings['accessTokenSecret']
        except:
            raise Exception('No configuration was found or the configuration provided was invalid.')
            
    def send(self,status:str,media=None):
        auth = tweepy.OAuthHandler(self.apiKey, self.apiSecretKey)
        auth.set_access_token(self.accessToken, self.accessTokenSecret)
        api = tweepy.API(auth)
        try:
            if media==None:
                api.update_status(status)
            else:
                api.update_with_media(filename=media,status=status)
            return True
        except Exception as e:
            return False

