import pickle
import operator
import string
from twython import Twython
import datetime
import time
import sqlite3 as lite
import sys

class DBTweetReader(object):
    def __init__(self, filename, tablename):
        self.con = lite.connect(filename)
        self.cur=self.con.cursor()
        self.table=tablename

    def getNumberOfTweets(self, tablename):
        self.cur.execute("SELECT max(rowid) FROM "+tablename)
        num=self.cur.fetchall()[0][0]
        return num

    def getUserDict(self, tablename, minimum=0):
        self.cur.execute("SELECT ScreenName FROM "+tablename)
        data=self.cur.fetchall()
        l=[]
        usersdict={}
        for item in data:
            l.append(item[0])

        for item in l:
            try:
                usersdict[item]+=1
            except:
                usersdict[item]=1

        if minimum>0:
            for item in usersdict.items():
                if item[1]<minimum:
                    del usersdict[item[0]]

        return usersdict
        
    def getRetweets(self, tablename):
        self.cur.execute("SELECT RetweetSource, ScreenName, RetweetTweet FROM "+tablename +" WHERE IsRetweet=1")
        print self.cur.fetchall()
