#from classtweetreader import TweetReader
import sqlite3 as lite
import sys
import string

valid_characters = string.ascii_letters
valid_characters += string.digits
valid_characters += '_'

# Add isretweet, retweet source, convertedtime columns

tags=["IPCC","UNFCCC","AR5","WGII","WGIII","LTFchat","Pages2k","Pages","HadCRUT","GISS"]
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

tablename="htclimate"
#myreader=TweetReader(filename="twitterdata_query=#climate_time=17_01_0813_lastid=290423702833729535.pkl")
#d=myreader.twitterdict
con = lite.connect('IPCCdb.db')

# self.twitterdict[item["id_str"]]={"screen_name":item["user"]["screen_name"], "name":item["user"]["name"], "user_id_str":item["user"]["id_str"], "user_mentions":mentionslist, "hashtags":hashtagslist, "urls":urlslist, "short_urls":shorturlslist, "id_str":item["id_str"], "created_at":item["created_at"], "text":text, "followers_count":item["user"]["followers_count"], "friends_count":item["user"]["friends_count"], "statuses_count":item["user"]["statuses_count"], "retweet_count":item["retweet_count"],"in_reply_to_status_id_str":item["in_reply_to_status_id_str"], "in_reply_to_user_id_str":item["in_reply_to_user_id_str"], "truncated":item["truncated"], "retweeted":item["retweeted"]}
                  
def ctable(tablename):
    global con
    cur = con.cursor()    
    cur.execute("CREATE TABLE "+tablename+"(Id INT, ScreenName TEXT, UserId INT, FullName TEXT, Tweet TEXT, Timestamp TEXT, RetweetCount INT, InReplyToStatusId INT, InReplyToUserId INT, Truncated INT, Retweeted INT, FriendsCount INT, FollowersCount INT, IsRetweet INT, RetweetSource TEXT, ConvertedTime INT, RetweetTweet TEXT)")

for t in tags:
    ctable(t)
