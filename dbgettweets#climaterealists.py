from classtweetgetter import DBTweetGetter
from classtweetreader import DBTweetReader

import datetime
tablename="htclimaterealists"
queryname='#climaterealists'
fname="#climaterealists"

myTweets=DBTweetGetter("tweetsdb.db", tablename)
myTweets.query(queryname,3160000, False)
#Write log file
with open("dblog"+fname+".txt", "a") as myfile:
    now = datetime.datetime.now()
    timestr=now.strftime("%d_%m_%H%M")
    myfile.write(timestr+"\n")
    readTweet=DBTweetReader("tweetsdb.db", tablename)
    print "Total number of tweets: " + str(readTweet.getNumberOfTweets(tablename))
    myfile.write("Total number of tweets: " + str(readTweet.getNumberOfTweets(tablename))+"\n")
    udict=readTweet.getUserDict(tablename)
    print "Total number of users: " + str(len(udict.keys()))
    myfile.write("Total number of users: " + str(len(udict.keys()))+"\n")
    for item in udict.items():
        if item[1]<3:
            del udict[item[0]]
    print "Total number of users with 3 tweets or more: " + str(len(udict.keys()))
    myfile.write("Total number of users with 3 tweets or more: " + str(len(udict.keys()))+"\n")

#modify this script
# with open("gettweetsClimateChange.py", "r") as myfile:
#     mytext=myfile.read()

# st=mytext.index("myTweets=TweetGetter")+22
# end=mytext.index('")', st)

# newtext=mytext[0:st] + myTweets.savedname + mytext[end:]
# #print newtext
# print "'Climate Change' finished"

# with open("gettweetsClimateChange.py", "w") as myfile:
#     myfile.write(newtext)
