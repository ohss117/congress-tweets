'''
Created on Oct 4, 2013

@author: sungoh
Credit for major help goes to Tim Bueno - www.timbueno.com

'''
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from congress_model import CongressMember, Tweets
from datetime import datetime
from auth import TwitterApiAuthorize
from abc import ABCMeta, abstractmethod  
import pytz
import time

class LoadDatabase:
    """
    Sets up database engine and session. Should be inherited.
    Create your own 'insert' method for adding tweets or congressmember, etc.
    """
    __metaclass__ = ABCMeta

    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.engine = sa.create_engine(self.database_dir, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    @abstractmethod
    def insert_and_update(self):
        """
        Do something here to insert and update Congress members or Tweets into database.
        """
        
        
class LoadCongress(LoadDatabase):
    """
    Inserts and updates Congress members from Sunlight API to the database.
    Inherits LoadDatabase
    """
    
    def insert_and_update(self, members):
        #Query the database for bioguide ID in order to remove departing members.
        #Primary key for the CongressMember table is 'bioguide_id'
        members_in_db = self.session.query(CongressMember.bioguide_id)
        #List of bioguide id numbers for the members of Congress in the database
        db_bioguide_list = [member_id[0] for member_id in members_in_db]
        #A list of bioguide IDs directly from the Sunlight foundation API
        sunlight_bioguide_list = [sun_member['bioguide_id'] for sun_member in members]
        
        #For each element in 'db_bioguide_list', check to see if it's in the 'sunlight_bioguide_list'
        #If an element of 'db_bioguide' is not in 'sunlight_bioguide', append to 'voted_out' list
        #uh oh, these dawgs are out of the dawghouse!!!
        for congress_member_id in db_bioguide_list:
            if congress_member_id not in sunlight_bioguide_list:
                #delete voted out members
                print 'Deleting {}'.format(congress_member_id)
                self.session.query(CongressMember).filter(CongressMember.bioguide_id == congress_member_id).delete()
            
        def add_members_to_db(cur):
            """
            Closure method to add elements to the current database.
            """
            sanitized_member = CongressMember(cur['firstname'], cur['middlename'], cur['lastname'],
                                              cur['gender'], datetime.strptime(cur['birthdate'], '%Y-%m-%d').date(), cur['bioguide_id'],
                                              cur['chamber'], cur['twitter_id'], cur['party'] )
            self.session.merge(sanitized_member)
        

        for element in range(len(members)):
            print 'Updating database'
            cursor = members[element]
            add_members_to_db(cursor)
        #Commit everything to the database.
        self.session.commit()
        print 'Insertion complete'
        
class LoadTweets(LoadDatabase):
    """
    If a Congress member has a Twitter account, load all Tweets into the database.
    Inherits LoadDatabase.
    """
    
    def insert_and_update(self, username):
        utc = pytz.utc
        homeTZ = 'America/Chicago'
        homeTZ = pytz.timezone(homeTZ)
        self.api = TwitterApiAuthorize.api
        self.status_list = []
        self.cur_status_count = 0
        #get the id of last tweet made by this user
        last_tweet = self.session.query(Tweets.tweet_id).filter(Tweets.congress_member == username).order_by(Tweets.tweet_id.desc()).first()[0]
        #last_tweet will be none if the db hasn't been initialized...
        #TODO:I might have goofed up here.
        
        #Default latest_tweet_id at the time of database creation is set to 0
        if last_tweet != 0:
            print 'First if statement'
            #Get Tweets made by the user since the last archive
            statuses = self.api.user_timeline(count=200, include_rts=True, since_id=last_tweet, screen_name=username)
            #Pause gathering data for 11 seconds to prevent Twitter from hating you
            print 'Waiting 11 seconds...'
            time.sleep(11)
            if statuses != []:
                theUser = statuses[0].author
                total_status_count = theUser.statuses_count
            while statuses != []:
                self.cur_status_count = self.cur_status_count + len(statuses)
                for status in statuses:
                    self.status_list.append(status)

                theMaxId = statuses[-1].id
                theMaxId = theMaxId - 1
                # Get next page of unarchived statuses
                statuses = self.api.user_timeline(count=200, include_rts=True, since_id=last_tweet, max_id=theMaxId, screen_name=username)
                #Pause
                print 'Waiting 11 seconds...'
                time.sleep(11)
        #When no Tweets have been archived       
        elif last_tweet == 0:
            statuses = self.api.user_timeline(count=200, include_rts=True, screen_name=username)
            #Pause
            print 'Waiting 11 seconds...'
            time.sleep(11)
            theUser = statuses[0].author
            total_status_count = theUser.statuses_count
            while statuses != []:
                self.cur_status_count = self.cur_status_count + len(statuses)
                for status in statuses:
                    self.status_list.append(status)

                # Get tweet id from last status in each page
                theMaxId = statuses[-1].id
                theMaxId = theMaxId - 1

                # Get new page of statuses based on current id location
                statuses = self.api.user_timeline(count=200, include_rts=True, max_id=theMaxId, screen_name=username)
                print "%d of %d tweets processed..." % (self.cur_status_count, total_status_count)
                time.sleep(11)
        #Add mined results to the database
        if self.status_list != []:
            for status in reversed(self.status_list):
                tweet_datetime = utc.localize(status.created_at).astimezone(homeTZ)
                tweet_url = 'http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)
                cleaned_status = Tweets(status.id, status.author.screen_name, status.text, tweet_datetime, tweet_url)
                self.session.add(cleaned_status)
            self.session.commit()
            print 'Insertion Complete'
        elif self.status_list == [] and last_tweet is not None:
            print 'No new tweets'
            
        rate_limit = self.api.rate_limit_status()
        #twitter_user_timeline =  rate_limit_json['/statuses/user_timeline']
        #remaining = twitter_user_timeline['remaining']
        #limit = twitter_user_timeline['limit']
        #print '{} calls remaining out of {}'.format(remaining, limit)
        print rate_limit['resources']['statuses']['/statuses/user_timeline']