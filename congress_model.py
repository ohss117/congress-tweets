'''
Created on Sep 26, 2013

@author: sungoh

Constructs a database of all the congress members and their tweets.
Pulls the list of congressmembers from the Sunlight Foundation's API.

'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy import Date, Time, DateTime
from sunlight import congress

import datetime
import os

working_dir = os.path.dirname(__file__)
database_name = 'test.db'
database_dir = 'sqlite:///'+os.path.join(working_dir, database_name)
engine = create_engine(database_dir, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()



class CongressMember(Base):
    '''
    Database table of all US Congress Members.
    '''
    __tablename__ = 'congressmember'
    id = Column(Integer, primary_key=True)
    
    first_name = Column(String(35))
    middle_name = Column(String(35))
    last_name = Column(String(35))
    gender = Column(String(1))
    birthday = Column(Date)
    
    thomas_id = Column(Integer(15))
    
    #Sen or Rep
    chamber = Column(String(3))
    #Twitter User ID
    twitter_id = Column(String(20))
    party = Column(String(1))
    last_updated = Column(DateTime, default=datetime.datetime.now())
    tweets_made = relationship('Tweets', backref='congressmember')

    
class Tweets(Base):
    '''
    Database table of Tweets made by congress members.
    One to many relationship between CongressMembers and this table.
    '''
    __tablename__ = 'tweets'
    tweet_id = Column(Integer, primary_key=True)
    congress_member = Column(Integer, ForeignKey('congressmember.id'))

    
    
    tweet_body = Column(Text(140))
    tweet_date = Column(Date)
    tweet_time = Column(Time)
    tweet_url = Column(String)
    test_column = Column(String)
    
    def __init__(self, tweet_id, tweet_author, tweet_body, tweet_date, tweet_time, tweet_url):
        self.tweet_id = tweet_id
        self.tweet_author = tweet_author
        self.tweet_body = tweet_body
        self.tweet_date = tweet_date
        self.tweet_time = tweet_time
        self.tweet_url = tweet_url
    
    def __repr__(self):
        return "<ID: %s> , <Author: %s> , <Tweet: %s> , <Tweet time: %s at %s >, <URL: %s>" % \
                (self.tweet_author, self.tweet_body, self.tweet_date, self.tweet_time, self.tweet_url)
'''
class Test(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)
    my_column = Column(String)
    my_derp = Column(Integer)
    my_herp = Column(String)
'''
#update_members()
#Base.metadata.create_all(engine)
'''
member = CongressMember(first_name='Nancy', last_name='Pelosi', twitter_id='NancyPelosi')
session.add(member)
session.commit()
'''