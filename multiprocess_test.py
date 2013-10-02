'''
Created on Oct 1, 2013

@author: sungoh
'''
import multiprocessing
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from time import time
import os
from auth import TwitterApiAuthorize


working_dir = os.path.dirname(__file__)
database_name = 'multi_test.db'
database_dir = 'sqlite:///' + os.path.join(working_dir, database_name)
engine = create_engine(database_dir, echo=True)
Base = declarative_base()
api = TwitterApiAuthorize.api


def multi_download(theUserName):
    statuses = api.user_timeline(count=200, include_rts=True, screen_name=theUserName)
    print statuses
    
class MultiTest(Base):
    __tablename__ = 'multitest'
    id = Column(Integer, primary_key=True)
    my_entry = Column(String, )

if __name__ == '__main__':
    p = multiprocessing.Pool(2)
    congress_list = ['NancyPelosi', 'SenatorReid', 'john_dingell']
    
    t1 = time()
    print(p.map(multi_download, congress_list))
    t2 = time()
    
    print('Time taken: {} seconds.'.format(t2-t1))