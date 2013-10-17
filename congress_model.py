'''
Created on Sep 26, 2013

@author: sungoh

Constructs a database of all the congress members and their tweets.
Pulls the list of congressmembers from the Sunlight Foundation's API.

'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy import Date, DateTime
import datetime
import os

working_dir = os.path.dirname(__file__)
db_name = 'congress_tweets.db'
database_dir = 'sqlite:///'+os.path.join(working_dir, db_name)

engine = create_engine(database_dir, echo=True)
Base = declarative_base()


class CongressMember(Base):
    """
    Database table of all US Congress Members, both Senate and House.
    """
    __tablename__ = 'congressmember'
    bioguide_id = Column(String(20), primary_key=True)
    
    first_name = Column(String(50))
    middle_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(1))
    birthday = Column(Date)
    state = Column(String(2))
    #Sen or Rep
    chamber = Column(String(6))
    #Twitter User ID
    twitter_id = Column(String(35))
    party = Column(String(1))
    last_updated = Column(DateTime, default=datetime.datetime.now())
    title = Column(String(10))
    
    def __init__(self, first_name, middle_name, last_name, state, gender, birthday, 
                 bioguide_id, chamber, twitter_id, party, title):
        self.bioguide_id = bioguide_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.state = state
        self.gender = gender
        self.birthday = birthday
        self.chamber = chamber
        self.twitter_id = twitter_id
        self.party = party
        self.title = title
        
    

class Tweets(Base):
    """
    Database table of Tweets made by congress members.
    One to many relationship between CongressMembers and this table.
    """
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String)
    congress_member = Column(String(20), ForeignKey('congressmember.bioguide_id'))
    tweet_body = Column(Text(140))
    tweet_datetime = Column(DateTime)
    tweet_url = Column(String)
    
    def __init__(self, tweet_id, tweet_author, tweet_body, tweet_datetime, tweet_url):
        self.tweet_id = tweet_id
        self.congress_member = tweet_author
        self.tweet_body = tweet_body
        self.tweet_datetime = tweet_datetime
        self.tweet_url = tweet_url
    
    def __repr__(self):
        return "<ID: %s> , <Author: %s> , <Tweet: %s> , <Tweet time: %s at %s >, <URL: %s>" % \
                (self.tweet_author, self.tweet_body, self.tweet_date, self.tweet_time, self.tweet_url)
#Creates the database
Base.metadata.create_all(engine)

