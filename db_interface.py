'''
Created on Oct 12, 2013

@author: sungoh
'''
import load_db, os
from sunlight import congress

working_dir = os.path.dirname(__file__)
db_name = 'arf.db'
database_dir = 'sqlite:///'+os.path.join(working_dir, db_name)


    
members  = load_db.LoadCongress(database_dir)
members.insert(congress.legislators())
#db = load_db.LoadTweets(db_name, database_dir)

#db.insert('NancyPelosi')