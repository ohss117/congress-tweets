'''
Created on Sep 26, 2013

@author: sungoh

Constructs an in-memory database of all the congress members and their tweets.
Pulls the list of congressmembers from the Sunlight Foundation's API.

'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy import Date, Time, DateTime, Sequence
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

class CongressMember(Base):
    '''
    Database table of all US Congress Members.
    '''
    __tablename__ = 'congress_members'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    
    first_name = Column(String(35))
    middle_name = Column(String(35))
    last_name = Column(String(35))
    gender = Column(String(1))
    birthday = Column(Date)
    
    #Sen or Rep
    chamber = Column(String(3))
    #Thomas ID for a legislator
    thomas_id = Column(String)
    twitter_id = Column(String(20))
    party = Column(String(1))
    last_updated = Column(DateTime, default=datetime.datetime.now())
    
    
class Tweets(Base):
    '''
    Database table of Tweets made by congress members.
    One to many relationship between CongressMembers and this table.
    '''
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    congress_member = Column(Integer, ForeignKey('congress_members.id'))
    member = relationship("CongressMember", backref=backref('tweets', order_by=id))

    
    tweet_id = Column(Integer, primary_key=True)
    tweet_body = Column(Text(140))
    tweet_date = Column(Date)
    tweet_time = Column(Time)
    tweet_url = Column(String)
    
    def __init__(self, tweet_author, tweet_body, tweet_date, tweet_time, tweet_url):
        self.tweet_author = tweet_author
        self.tweet_body = tweet_body
        self.tweet_date = tweet_date
        self.tweet_time = tweet_time
        self.tweet_url = tweet_url
    
    def __repr__(self):
        return "Author: %s , Tweet: %s , Tweet time: %s at %s , URL: %s" % \
                (self.tweet_author, self.tweet_body, self.tweet_date, self.tweet_time, self.tweet_url)
    
    
#update_members()
#Base.metadata.create_all(engine)

member = CongressMember(first_name='Nancy', last_name='Pelosi', twitter_id='NancyPelosi')
session.add(member)
session.commit()