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

class LoadDatabase:
    """
    Sets up database engine and session. Should be inherited.
    Create your own 'insert' method for adding tweets or congressmember, etc.
    Not sure at the moment what the best way to organize my code would be. :-(
    """
    __metaclass__ = ABCMeta

    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.engine = sa.create_engine(self.database_dir, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    @abstractmethod
    def insert(self):
        """
        Do something here to insert data into database.
        """
        
        
class LoadCongress(LoadDatabase):
    """
    Inserts Congress members from Sunlight API to the database.
    Inherits LoadDatabase
    """
    
    def insert(self, members):
        #TODO: Implement insert/update logic.
        #I want this method to remove departing members, update existing members or add new members.
        members_in_db = self.session.query(CongressMember.bioguide_id)
        #List of bioguide id numbers for the members of Congress in the database
        db_bioguide_list = []
        for member_id in members_in_db:
            db_bioguide_list.append(member_id[0])
        
        def add_members_to_db(cur):
            """
            Closure method to add elements to db.
            """
            sanitized_member = CongressMember(cur['firstname'], cur['middlename'], cur['lastname'],
                                              cur['gender'], datetime.strptime(cur['birthdate'], '%Y-%m-%d').date(), cur['bioguide_id'],
                                              cur['chamber'], cur['twitter_id'], cur['party'] )
            self.session.merge(sanitized_member)
        
        #If the database is already populated, do the following block
        if len(db_bioguide_list) != 0:
            for element in range(len(members)):
                cursor = members[element]
                #Get the bioguide ID of congress members obtained from Sunlight foundation.
                #Check 'sunlight_bioguide' against 'check_bioguide' list to remove those voted out of office
                sunlight_bioguide = cursor['bioguide_id']
                if sunlight_bioguide in db_bioguide_list:
                    add_members_to_db(cursor)
                    print 'Woof'
                elif sunlight_bioguide not in db_bioguide_list:
                    #Uhoh, this dawg is out of the dawghouse!!!
                    self.session.query(CongressMember).filter(CongressMember.bioguide_id == sunlight_bioguide).delete()
        #If the database is empty, add everything from Sunlight API
        else:
            for element in range(len(members)):
                cursor = members[element]
                add_members_to_db(cursor)
        self.session.commit()
        print 'Insertion complete'
        print len(db_bioguide_list)

        
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
