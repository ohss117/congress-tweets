'''
Created on Oct 12, 2013

@author: sungoh
'''
import load_db, os
from sunlight import congress

working_dir = os.path.dirname(__file__)
db_name = 'congress_tweets.db'
database_dir = 'sqlite:///'+os.path.join(working_dir, db_name)

congress_members = congress.legislators()

member_database = load_db.LoadCongress(database_dir)
member_database.insert_and_update(congress_members)


"""
twitter_database = load_db.LoadTweets(database_dir)

senate_members_twitter = [member['twitter_id'] for member in congress_members if member['chamber'] == 'senate']

for senator_twitter_id in senate_members_twitter:
    twitter_database.insert_and_update(senator_twitter_id)
"""