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
import pytz

class LoadDatabase(object):
    """
    Sets up database engine and session. Should be inherited. TODO: Abstract Base Class?
    Not sure at the moment what the best way to organize my code would be. :-(
    Create your own 'insert' method for adding tweets or congressmember, etc.
    """

    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.engine = sa.create_engine(self.database_dir, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

class LoadCongress(LoadDatabase):
    """
    Inserts Congress members from Sunlight API to the database.
    Inherits LoadDatabase
    """
    
    def insert(self, members):
        for element in range(len(members)):
            cursor = members[element]
            sanitized_member = CongressMember(cursor['firstname'], cursor['middlename'], cursor['lastname'],
                                              cursor['gender'], datetime.strptime(cursor['birthdate'], '%Y-%m-%d').date(), cursor['bioguide_id'],
                                              cursor['chamber'], cursor['twitter_id'], cursor['party'] )
            self.session.add(sanitized_member)
        self.session.commit()
        print 'Insertion complete'
        
class LoadTweets(LoadDatabase):
    """
    If a Congress member has a Twitter account, load all Tweets into the database.
    Inherits LoadDatabase.
    """
    
    def insert(self, username):
        utc = pytz.utc
        homeTZ = 'America/New_York'
        homeTZ = pytz.timezone(homeTZ)
        self.api = TwitterApiAuthorize.api
        self.status_list = []
        self.cur_status_count = 0
        #get the id of last tweet made by this user
        try:
            last_tweet = self.session.query(Tweets.tweet_id).filter(Tweets.congress_member == username).order_by(Tweets.tweet_id.desc()).first()[0]
        except:
            last_tweet = None
        #Default latest_tweet_id at the time of database creation is set to 0
        if last_tweet != 0 and self.status_list != []:
            #Get Tweets made by the user since the last archive
            statuses = self.api.user_timeline(count=200, include_rts=True, since_id=last_tweet, screen_name=username)
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
        elif self.status_list == [] and last_tweet is not None:
            print 'No new tweets'
        #When no Tweets have been archived       
        elif last_tweet == None:
            statuses = self.api.user_timeline(count=200, include_rts=True, screen_name=username)
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
        #Add mined results to the database
        if self.status_list != []:
            for status in reversed(self.status_list):
                tweet_datetime = utc.localize(status.created_at).astimezone(homeTZ)
                tweet_url = 'http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)
                cleaned_status = Tweets(status.id, status.author.screen_name, status.text, tweet_datetime, tweet_url)
                self.session.add(cleaned_status)
            self.session.commit()
            print 'Insertion Complete'
