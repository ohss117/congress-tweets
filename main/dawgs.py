'''
Created on Sep 16, 2013

@author: sungoh
'''
import tweepy
from auth import ApiAuthorize

api = ApiAuthorize.api
    
#Testing API        
if api.verify_credentials() is not False:
        print 'good'
else:
    print 'Invalid Authentication'
 
print api.get_user(screen_name = 'NancyPelosi').__getstate__()

barack = api.get_user(screen_name = 'BarackObama').__getstate__()

print barack['screen_name']
    
#All the members of the congress that have twitter accounts according to this list-- https://twitter.com/cspan/lists/members-of-congress
dawgs = []
for member in tweepy.Cursor(api.list_members, 'CSPAN', 'members-of-congress').items():
    dawgs.append(member.__getstate__()['screen_name'])
print dawgs

print 'This many dawgs have twitta: ' + str(len(dawgs))
