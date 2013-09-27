'''
Created on Sep 25, 2013

@author: sungoh
'''
import tweepy, os

class TwitterApiAuthorize():
    '''
    Container for Twitter API authentication
    '''
    auth = tweepy.auth.OAuthHandler(os.environ.get('CONSUMERTOKEN'), os.environ.get('CONSUMERSECRET'))
    auth.set_access_token(os.environ.get('ACCESSTOKEN'), os.environ.get('ACCESSSECRET'))
    api = tweepy.API(auth)


class SunlightApiAuthorize():
    '''
    Container for Sunlight Foundation API authentication.
    Use this class if you do not have the .sunlight.key file in your home directory.
    If there exists both the API key file and the API environment variable, the environment variable will override the file.
    '''
    os.environ.get('SUNLIGHT_API_KEY')