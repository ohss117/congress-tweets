'''
Created on Nov 5, 2013

@author: sungoh

'''

class Tweet(object):
    """
    Turn each Tweet entry from the database into a Python object.
    This may be redundant, as database queries can easily replace this.
    But whatever man. 
    """
    def __init__(self, query_result):
        #Obviously, this query should be broken down into
        #its components
        self.query_result = query_result
        
