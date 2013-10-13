'''
Created on Oct 1, 2013

@author: sungoh
'''
import multiprocessing
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from time import time
from auth import TwitterApiAuthorize

api = TwitterApiAuthorize.api

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


def multi_download(theUserName):
    statuses = api.user_timeline(count=200, include_rts=True, screen_name=theUserName)
    print statuses
    
class MultiTest(Base):
    __tablename__ = 'multitest'
    id = Column(Integer, primary_key=True)
    my_entry = Column(String, )
    
def init_sqlalchemy(dbname = 'sqlite:///sqlalchemy.db'):
    global engine
    engine = create_engine(dbname, echo=False)
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def test_sqlalchemy_core(n=100000):
    init_sqlalchemy()
    t0 = time()
    engine.execute(
        MultiTest.__table__.insert(),
        [{"my_entry":'meow ' + str(i)} for i in range(n)]
    )
    print "SqlAlchemy Core: Total time for " + str(n) + " records " + str(time() - t0) + " secs"



if __name__ == '__main__':
    '''
    p = multiprocessing.Pool(2)
    congress_list = ['NancyPelosi', 'SenatorReid', 'john_dingell']
    
    t1 = time()
    print(p.map(multi_download, congress_list))
    t2 = time()
    
    print('Time taken: {} seconds.'.format(t2-t1))
    '''
    test_sqlalchemy_core(100000)
