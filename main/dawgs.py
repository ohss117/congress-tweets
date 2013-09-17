'''
Created on Sep 16, 2013

@author: sungoh
'''
import tweepy

auth = tweepy.auth.OAuthHandler('lnRooNIFnJdWBz8LQnMbOQ', '69aFhthvjtxlLpZQ3sJ8tt8cQZ3nFZ3I7a0qCVI')
auth.set_access_token('635070399-LJfZWHLeNYD9h55REcNyqFXl9JOW8Wp27bbBaHre', 'nXcJAMcTObvo5ziPkjTuxjHE9oBRDDC1AF8V9ERc')
api = tweepy.API(auth)

if api.verify_credentials() is not False:
    print 'good'
    #return api
else:
    print 'Invalid Authentication'
    #return None
    
print api.get_user(screen_name = 'NancyPelosi').__getstate__()

barack = api.get_user(screen_name = 'BarackObama').__getstate__()

print barack['screen_name']

dawgs = []
for member in tweepy.Cursor(api.list_members, 'CSPAN', 'members-of-congress').items():
    dawgs.append(member.__getstate__()['screen_name'])
print dawgs
