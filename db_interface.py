'''
Created on Oct 12, 2013

@author: sungoh
'''
import load_db, os
from sunlight import congress

working_dir = os.path.dirname(__file__)
db_name = 'arf.db'
database_dir = 'sqlite:///'+os.path.join(working_dir, db_name)


    
#members  = load_db.LoadCongress(database_dir)
#members.insert_and_update(congress.legislators())
db = load_db.LoadTweets(database_dir)

db.insert_and_update('NancyPelosi')