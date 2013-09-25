'''
Created on Sep 25, 2013

@author: sungoh
'''
import tweepy, os

class ApiAuthorize():
    '''
    Class wrapper for Twitter API authentication
    '''
    auth = tweepy.auth.OAuthHandler(os.environ.get('CONSUMERTOKEN'), os.environ.get('CONSUMERSECRET'))
    auth.set_access_token(os.environ.get('ACCESSTOKEN'), os.environ.get('ACCESSSECRET'))
    api = tweepy.API(auth)
    
    def __init__(self, auth, api):
        '''
        Constructor
        '''
        self.auth = auth
        self.api = api
        
    