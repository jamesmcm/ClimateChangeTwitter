import sqlite3 as lite
import sys
import string
from twython import Twython
import time
import datetime
from time import sleep
import pickle
import datetime
import os

valid_characters = string.ascii_letters
valid_characters += string.digits
valid_characters += '_'

#utility functions
def convertbool(bool):
    if bool==True:
        return 1
    else:
        return 0

def fixnone(x):
    if x == None:
        return 0
    else:
        return x

def escapes(s):
    f=s[0]
    s=s[1:-1]
    s=s.replace(r'"', r'\"')
    if f=='"':
        s=s.replace(r"'", r"\'")

    s=s.replace(r"\'", r"''")
    s="'"+s+"'"
    return s

class DBTweetGetter(object):
    """ 
    This class gets the tweets and stores them in the database. 
    query(query,numtweets=160000, usemaxid=True) is responsible for actually downloading the tweets. The IDs of the downloaded tweets are checked in the initialisation of the class, and query checks against this to know when it has downloaded all of the most recent, unseen tweets.
    """
    def __init__(self, filename, tablename):
        if filename!=None:
            self.con = lite.connect(filename)
            self.screened=[]
            self.cur=self.con.cursor()
            self.ucon = lite.connect("userdb.db")
            self.ucur=self.ucon.cursor()
            self.tablename=tablename
            self.ucur.execute("SELECT ScreenName FROM usermap")
            a=self.ucur.fetchall()
            for item in a:
                self.screened.append(item[0])
            self.cur.execute("SELECT Id FROM "+tablename)
            data=self.cur.fetchall()
            l=[]
            for item in data:
                l.append(item[0])
            self.idlist=l
        try:
            self.twython= Twython(app_key="674Getn4iR5ZonBvSZIE6w", app_secret="XIIhDdsCmByqLQG89ED9h7MILQbS4hsMV3ob6hlLYA", oauth_token="27203313-Oujk9Qu6sKe7tBBYYrheAb1r484PViz2w8GShZCeg", oauth_token_secret="cm95hSRUmkloWBVbYrTHuIYA7fSQqFJH5iYGIbw5ZKo")
        except Exception as detail:
            print "Error loading Twython object. Error message: " + str(detail)
            raise Exception(detail)

    def query(self,query,numtweets=160000, usemaxid=True):
        if usemaxid==False:
            self.maxid=None
        self.query=query
        ntweets=0
        nmatch=0
        while ntweets<numtweets:
            try:
                if self.maxid!=None:
                    mydict=self.twython.search(q=query, result_type="recent", count="100", max_id=str(self.maxid))
                else:
                    mydict=self.twython.search(q=query, result_type="recent", count="100")

                actualcount=len(mydict["statuses"])
                if actualcount != 0:
                    
                    self.maxid=int(mydict["statuses"][actualcount-1]["id_str"])-1 #int at the moment

                    for item in mydict["statuses"]:
                        
                        if (not (int(item["id_str"]) in self.idlist)):
                            text=item["text"].replace(unichr(8220),'"')
                            text=text.replace(unichr(8221),'"')
                            ctime=str(self.convertTime(item["created_at"]))
                            isretweet="0"
                            source=u"-"
                            tweet=u"-"
                            if text[0:2] == "RT":
                                isretweet="1"
                                s=text
                                try:
                                    atindex=s.index("@")
                                    breakif=False
                                except:
                                    breakif=True

                                if breakif==False:
                                    keepgoing=True
                                    i=1
                                    while keepgoing==True:
                                        try:
                                            if not (s[atindex+i] in valid_characters):
                                                keepgoing=False
                                                endindex=i
                                            else:
                                                i+=1
                                        except:
                                            keepgoing=False
                                            endindex=i
                                    source=s[atindex+1:atindex+endindex]
                                    tweet=s[atindex+endindex+1:]

                            if not (item["user"]["screen_name"] in self.screened):
                                self.ucur.execute("INSERT INTO usermap VALUES('" + item["user"]["screen_name"]  + "'," + item["user"]["id_str"] + ")" )
                                self.screened.append(item["user"]["screen_name"])

                            self.con.execute("INSERT INTO "+self.tablename+" VALUES("+str(item["id_str"])+","+escapes(repr(item["user"]["screen_name"])[1:])+","+escapes(repr(item["user"]["name"])[1:])+","+escapes(repr(text)[1:])+",'"+item["created_at"]+"',"+str(item["retweet_count"]) +","+str(fixnone(item["in_reply_to_status_id_str"]))+","+str(fixnone(item["in_reply_to_user_id_str"])) +"," + str(convertbool(item["truncated"])) +","+str(convertbool(item["retweeted"])) +","+str(item["user"]["friends_count"]) +"," + str(item["user"]["followers_count"]) + "," + isretweet +","+ escapes(repr(source)[1:]) +","+ctime+"," +escapes(repr(tweet)[1:]) + ")" )


                            ntweets+=1
                        else:
                            nmatch+=1
                            if nmatch>3:
                                print "Grabbing old tweets, stopping."
                                ntweets=numtweets+1
                        
                else:
                    print "Cannot obtain more tweets"
                    ntweets=numtweets+1
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                sleep(300)
                

            print str(ntweets)
            sleep(10)
        self.con.commit()
        self.con.close()
        self.ucon.commit()
        self.ucon.close()

    def query2(self,query,numtweets=160000, usemaxid=True):
        #Used to get tweets for new IPCC hashtags, to add in the userID which was omitted in the previous database by mistake
        if usemaxid==False:
            self.maxid=None
        self.query=query
        ntweets=0
        nmatch=0
        while ntweets<numtweets:
            try:
                if self.maxid!=None:
                    mydict=self.twython.search(q=query, result_type="recent", count="100", max_id=str(self.maxid))
                else:
                    mydict=self.twython.search(q=query, result_type="recent", count="100")

                actualcount=len(mydict["statuses"])
                if actualcount != 0:
                    
                    self.maxid=int(mydict["statuses"][actualcount-1]["id_str"])-1 #int at the moment

                    for item in mydict["statuses"]:
                        
                        if (not (int(item["id_str"]) in self.idlist)):
                            text=item["text"].replace(unichr(8220),'"')
                            text=text.replace(unichr(8221),'"')
                            ctime=str(self.convertTime(item["created_at"]))
                            isretweet="0"
                            source=u"-"
                            tweet=u"-"
                            if text[0:2] == "RT":
                                isretweet="1"
                                s=text
                                try:
                                    atindex=s.index("@")
                                    breakif=False
                                except:
                                    breakif=True

                                if breakif==False:
                                    keepgoing=True
                                    i=1
                                    while keepgoing==True:
                                        try:
                                            if not (s[atindex+i] in valid_characters):
                                                keepgoing=False
                                                endindex=i
                                            else:
                                                i+=1
                                        except:
                                            keepgoing=False
                                            endindex=i
                                    source=s[atindex+1:atindex+endindex]
                                    tweet=s[atindex+endindex+1:]

                            if not (item["user"]["screen_name"] in self.screened):
                                self.ucur.execute("INSERT INTO usermap VALUES('" + item["user"]["screen_name"]  + "'," + item["user"]["id_str"] + ")" )
                                self.screened.append(item["user"]["screen_name"])

                            self.con.execute("INSERT INTO "+self.tablename+" VALUES("+str(item["id_str"])+","+escapes(repr(item["user"]["screen_name"])[1:])+","+str(item["user"]["id_str"])+","+escapes(repr(item["user"]["name"])[1:])+","+escapes(repr(text)[1:])+",'"+item["created_at"]+"',"+str(item["retweet_count"]) +","+str(fixnone(item["in_reply_to_status_id_str"]))+","+str(fixnone(item["in_reply_to_user_id_str"])) +"," + str(convertbool(item["truncated"])) +","+str(convertbool(item["retweeted"])) +","+str(item["user"]["friends_count"]) +"," + str(item["user"]["followers_count"]) + "," + isretweet +","+ escapes(repr(source)[1:]) +","+ctime+"," +escapes(repr(tweet)[1:]) + ")" )


                            ntweets+=1
                        else:
                            nmatch+=1
                            if nmatch>3:
                                print "Grabbing old tweets, stopping."
                                ntweets=numtweets+1
                        
                else:
                    print "Cannot obtain more tweets"
                    ntweets=numtweets+1
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                sleep(300)
                

            print str(ntweets)
            sleep(10)
        self.con.commit()
        self.con.close()
        self.ucon.commit()
        self.ucon.close()

    def convertTime(self, timestring):
        #Fri Nov 16 22:31:39 +0000 2012
        lts=timestring.split(" ")
        tt=lts[3].split(":")
        monthdict={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        dt=datetime.datetime(int(lts[5]), int(monthdict[lts[1]]), int(lts[2]),int(tt[0]),int(tt[1]),int(tt[2]))
        return int(time.mktime(dt.timetuple()))


    def getIDfromUser(self,screen_name):
        gotry=True
        while gotry==True:
            try:
                d=self.twython.showUser(screen_name=screen_name, entities="false")
                gotry=False
            except Exception as detail:
                if ("The URI requested is invalid" in str(detail)) or ("Unauthorized" in str(detail)):
                    print "User " + screen_name + " does not exist."
                    sleep(8)
                    return "FAIL"
                elif "suspended" in str(detail):
                    print "Some Twitter error: " + str(detail)
                    gotry=True
                    sleep(3600)
                else:
                    print "Some Twitter error: " + str(detail)
                    gotry=True
                    sleep(300)
        sleep(8)
        return d["id_str"]

    def getUserDescription(self, screen_name):
        gotry=True
        while gotry==True:
            try:
                d=self.twython.showUser(screen_name=screen_name, entities="false")
                gotry=False
            except Exception as detail:
                if ("The URI requested is invalid" in str(detail)) or ("Unauthorized" in str(detail)) or ("An error occurred processing your request" in str(detail)):
                    print "User " + screen_name + " does not exist."
                    sleep(5)
                    return "FAIL"
                elif "suspended" in str(detail):
                    print "Some Twitter error: " + str(detail)
                    #sleep(300)
                    return "FAIL"

                else:
                    print "Some Twitter error: " + str(detail)
                    gotry=True
                    sleep(5)
        sleep(3)
        return d["description"]

    def getFriends(self, name, friendslist, cursor):
        #Recursively get followers
        sleep(8)
        #print "Getting Friends:" + name
        while True:
            try:
                d=self.twython.getFriendsIDs(screen_name=name, cursor=str(cursor))
                cursor=d["next_cursor"]
                #print str(cursor)
                break
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                print name
                print str(cursor)
                if ("The URI requested is invalid" in str(detail)) or ("Unauthorized" in str(detail)):
                    print name
                    cursor=-1
                    return "FAIL"
                elif "suspended" in str(detail):
                    sleep(3600)
                else:
                    sleep(300)
        friendslist=friendslist+d["ids"]
                    

        if cursor>0:
            sleep(7)
            friendslist=self.getFriends(name, friendslist, cursor)
        # else:
        return friendslist

    def getFollowers(self, name, followerslist, cursor):
        #Recursively get followers
        sleep(7)
        #print "Getting Followers:" + name
        while True:
            try:
                d=self.twython.getFollowersIDs(screen_name=name, cursor=str(cursor))
                cursor=d["next_cursor"]
                #print str(cursor)
                break
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                print name
                print str(cursor)
                if ("The URI requested is invalid" in str(detail)) or ("Unauthorized" in str(detail)):
                    cursor=-1
                    return "FAIL"
                elif "suspended" in str(detail):
                    sleep(3600)
                else:
                    sleep(300)

        followerslist=followerslist+d["ids"]
        # print name + ": " +str(len(followerslist))

            
        if cursor>0:
            sleep(7)
            followerslist=self.getFollowers(name, followerslist, cursor)
        # print len(followerslist)
        return followerslist

