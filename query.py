'''
Created on Oct 4, 2013

@author: sungoh
Testing out queries on the database.
'''

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from congress_model import CongressMember
import os, re

#Do I need to do this every time?
working_dir = os.path.dirname(__file__)
database_name = 'congress.db'
database_dir = 'sqlite:///'+os.path.join(working_dir, database_name)
engine = sa.create_engine(database_dir, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

no_twitter = []

for instance in session.query(CongressMember).order_by(CongressMember.id):
    name = '"%s"' % (instance.first_name+' '+instance.middle_name+' '+instance.last_name)
    if instance.twitter_id == '':
        no_twitter.append(re.sub(' +', ' ', instance.govtrack+', '+name))

#Write query result to a file.
data = open("no_twitter.txt", "w")
for entry in no_twitter:
    data.write("%s\n" % entry)
data.close()