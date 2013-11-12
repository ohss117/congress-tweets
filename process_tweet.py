'''
Created on Nov 5, 2013

@author: sungoh

This module will sanitize a tweet in order to enhance feature selectsion.

E.g. If a tweet contains an user-id, it should be replaced with something generic.
Perhaps I can replace '@some_user' to 'twitter_user' and tell nltk to ignore
all instances of 'twitter_user'. I'll have to think more about how this should
be accomplished, however. 
'''

class CleanTweet(object):
    """
    TODO: I need to get information from the database.
    What would be the best way to set up the connection?
    Also, should I create a Tweet class? Which would be better,
    dealing with raw text, or wrapping up data as a Tweet class
    object?
    """
    
    def remove_user_id(self):
        """
        Replaces all instances of strings
        that start with '@' to 'twitter_user'
        """
        
