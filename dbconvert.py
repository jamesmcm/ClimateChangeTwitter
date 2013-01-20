from classtweetreader import TweetReader
import sqlite3 as lite
import sys
import string

valid_characters = string.ascii_letters
valid_characters += string.digits
valid_characters += '_'

# Add isretweet, retweet source, convertedtime columns


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
myreader=TweetReader(filename="twitterdata_query=#climate_time=17_01_0813_lastid=290423702833729535.pkl")
d=myreader.twitterdict
con = lite.connect('tweetsdb.db')

# self.twitterdict[item["id_str"]]={"screen_name":item["user"]["screen_name"], "name":item["user"]["name"], "user_id_str":item["user"]["id_str"], "user_mentions":mentionslist, "hashtags":hashtagslist, "urls":urlslist, "short_urls":shorturlslist, "id_str":item["id_str"], "created_at":item["created_at"], "text":text, "followers_count":item["user"]["followers_count"], "friends_count":item["user"]["friends_count"], "statuses_count":item["user"]["statuses_count"], "retweet_count":item["retweet_count"],"in_reply_to_status_id_str":item["in_reply_to_status_id_str"], "in_reply_to_user_id_str":item["in_reply_to_user_id_str"], "truncated":item["truncated"], "retweeted":item["retweeted"]}
                  

with con:
    
    cur = con.cursor()    
    cur.execute("CREATE TABLE "+tablename+"(Id INT, ScreenName TEXT, FullName TEXT, Tweet TEXT, Timestamp TEXT, RetweetCount INT, InReplyToStatusId INT, InReplyToUserId INT, Truncated INT, Retweeted INT, FriendsCount INT, FollowersCount INT, IsRetweet INT, RetweetSource TEXT, ConvertedTime INT, RetweetTweet TEXT)")

    for item in d.keys():

        # sname=escapes(repr(d[item]["screen_name"])[1:])
        # name=escapes(repr(d[item]["name"])[1:])
        # tweet=escapes(repr(d[item]["text"])[1:])
            



        #     for item in self.twitterdict.keys():
        ctime=str(myreader.convertTime(d[item]["created_at"]))
        isretweet="0"
        source=u"-"
        tweet=u"-"
        if d[item]["text"][0:2] == "RT":
            isretweet="1"
            s=d[item]["text"]
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
                
        #         returnlist.append({"text":s[atindex+endindex+1:],"screen_name": self.twitterdict[item]["screen_name"], "created_at": self.twitterdict[item]["created_at"], "source_screen_name":s[atindex+1:atindex+endindex], "id_str":str(item)})

        #print "INSERT INTO "+tablename+" VALUES("+str(item)+","+escapes(repr(d[item]["screen_name"])[1:])+","+escapes(repr(d[item]["name"])[1:])+","+escapes(repr(d[item]["text"])[1:])+",'"+d[item]["created_at"]+"',"+str(d[item]["retweet_count"]) +","+str(fixnone(d[item]["in_reply_to_status_id_str"]))+","+str(fixnone(d[item]["in_reply_to_user_id_str"])) +"," + str(convertbool(d[item]["truncated"])) +","+str(convertbool(d[item]["retweeted"])) +","+str(d[item]["friends_count"]) +"," + str(d[item]["followers_count"]) + "," + isretweet +","+ escapes(repr(source))[1:] +","+ctime+"," +escapes(repr(tweet))[1:] + ")"
                
        cur.execute("INSERT INTO "+tablename+" VALUES("+str(item)+","+escapes(repr(d[item]["screen_name"])[1:])+","+escapes(repr(d[item]["name"])[1:])+","+escapes(repr(d[item]["text"])[1:])+",'"+d[item]["created_at"]+"',"+str(d[item]["retweet_count"]) +","+str(fixnone(d[item]["in_reply_to_status_id_str"]))+","+str(fixnone(d[item]["in_reply_to_user_id_str"])) +"," + str(convertbool(d[item]["truncated"])) +","+str(convertbool(d[item]["retweeted"])) +","+str(d[item]["friends_count"]) +"," + str(d[item]["followers_count"]) + "," + isretweet +","+ escapes(repr(source)[1:]) +","+ctime+"," +escapes(repr(tweet)[1:]) + ")" )


