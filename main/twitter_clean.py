'''
Created on Sep 16, 2013

@author: sungoh
'''

"""
This Python script cleans up non-congress members from 'members-of-congress' at CSPAN's account
"""
#read in file
with open('congress_members_raw.txt') as f:
    lines = f.readlines()

#split at comma
a = lines[0].split(',')

#write output
output = open('congress_clean.txt', 'w')
#I prepended all of the non-members with '&'. Removing those things now.
b = [item.strip() for item in a if item[1] != '&']
for item in b:
    output.write("%s\n" % item)
