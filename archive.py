'''
Created on Sep 25, 2013

@author: sungoh
Credit for major help goes to Tim Bueno - www.timbueno.com
'''

import codecs
import os
import pytz
from auth import TwitterApiAuthorize
from sunlight import congress

def update_members():
    '''
    This method fetches a list of congress members from Sunlight Foundation API 
    then populates the database with the retrieved information.
    '''
    members = congress.legislators()
    senate = []
    house = []
    for x in range(len(members)):
        if members[x]['title'] == 'Sen':
            senate.append(members[x])
        elif members[x]['title'] == 'Rep':
            house.append(members[x])
    print members[1]['title']
    print senate[0]
    print len(senate)
    print len(house)
    
theUserName = 'RepDennisRoss'
archiveFile = 'RepDennisRoss.txt'
homeTZ = 'America/New_York'
homeTZ = pytz.timezone(homeTZ)

# lastTweetId file location
idFile = theUserName + '.tweetid'
working_dir = os.path.dirname(__file__) # get script directory
idFile = os.path.join(working_dir, idFile) # join dir and filename
# Instantiate time zone object
utc = pytz.utc

#Create Twitter API object from the ApiAuthorize wrapper
api = TwitterApiAuthorize.api

# helpful variables
status_list = [] # Create empty list to hold statuses
cur_status_count = 0 # set current status count to zero


if os.path.exists(idFile):
    # Get most recent tweet id from file
    f = open(idFile, 'r')
    idValue = f.read()
    f.close()
    idValue = int(idValue)
    print "- - - - - - - - - - - - - - - - -"
    print "tweetID file found! "
    print "Latest Tweet ID: " +str(idValue)
    print "Gathering unarchived tweets... "

    # Get first page of unarchived statuses
    statuses = api.user_timeline(count=200, include_rts=True, since_id=idValue, screen_name=theUserName)
    # Get User information for display
    if statuses != []:
        theUser = statuses[0].author
        total_status_count = theUser.statuses_count

    while statuses != []:
        cur_status_count = cur_status_count + len(statuses)
        for status in statuses:
            status_list.append(status)

        theMaxId = statuses[-1].id
        theMaxId = theMaxId - 1
        # Get next page of unarchived statuses
        statuses = api.user_timeline(count=200, include_rts=True, since_id=idValue, max_id=theMaxId, screen_name=theUserName)

else:
    # Request first status page from twitter
    statuses = api.user_timeline(count=200, include_rts=True, screen_name=theUserName)
    # Get User information for display
    theUser = statuses[0].author
    total_status_count = theUser.statuses_count
    print "- - - - - - - - - - - - - - - - -"
    print "No tweetID file found..."
    print "Creating a new archive file"
    print "- - - - - - - - - - - - - - - - -"

    while statuses != []:
        cur_status_count = cur_status_count + len(statuses)
        for status in statuses:
            status_list.append(status)

        # Get tweet id from last status in each page
        theMaxId = statuses[-1].id
        theMaxId = theMaxId - 1

        # Get new page of statuses based on current id location
        statuses = api.user_timeline(count=200, include_rts=True, max_id=theMaxId, screen_name=theUserName)
        print "%d of %d tweets processed..." % (cur_status_count, total_status_count)

    print "- - - - - - - - - - - - - - - - -"
    # print "Total Statuses Retrieved: " + str(len(status_list))
    print "Writing statuses to log file:"

#Write tweets to archive
if status_list != []:
    print "Writing tweets to archive..."
    print "Archive file:"
    print archiveFile
    print "- - - - - - - - - - - - - - - - -"
    f = codecs.open(archiveFile, 'a', 'utf-8')
    for status in reversed(status_list):
        theTime = utc.localize(status.created_at).astimezone(homeTZ)
        # Format your tweet archive here!
        f.write(status.text + '\n')
        f.write(theTime.strftime("%B %d, %Y at %I:%M%p\n"))
        f.write('http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)+'\n')
        f.write('- - - - - \n\n')
    f.close()

    # Write most recent tweet id to file for reuse
    print "Saving last tweet id for later..."
    f = open(idFile, 'w')
    f.write(str(status_list[0].id))
    f.close()

if status_list == []:
    print "- - - - - - - - - - - - - - - - -"
    print "No new tweets to archive!"
print "Total Statuses Retrieved: " + str(len(status_list))
print "Finished!"
print "- - - - - - - - - - - - - - - - -"