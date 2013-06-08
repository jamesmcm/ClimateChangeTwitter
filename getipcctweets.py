from classtweetgetter import DBTweetGetter
#from classtweetreader import DBTweetReader

import datetime
tags=["IPCC","UNFCCC","AR5","WGII","WGIII","LTFchat","Pages2k","Pages","HadCRUT","GISS"]


for name in tags:
    myTweets=DBTweetGetter("IPCCdb.db", name)
    myTweets.query2("#"+name,1600000, False)
    #Write log file
    # with open("log"+name+".txt", "a") as myfile:
    #     now = datetime.datetime.now()
    #     timestr=now.strftime("%d_%m_%H%M")
    #     myfile.write(timestr+"\n")
    #     readTweet=DBTweetReader("IPCCdb.db", tablename)
    #     print "Total number of tweets: " + str(readTweet.getNumberOfTweets(tablename))
    #     myfile.write("Total number of tweets: " + str(readTweet.getNumberOfTweets(tablename))+"\n")
    #     udict=readTweet.getUserDict(tablename)
    #     print "Total number of users: " + str(len(udict.keys()))
    #     myfile.write("Total number of users: " + str(len(udict.keys()))+"\n")
    #     for item in udict.items():
    #         if item[1]<3:
    #             del udict[item[0]]
    #     print "Total number of users with 3 tweets or more: " + str(len(udict.keys()))
    # myfile.write("Total number of users with 3 tweets or more: " + str(len(udict.keys()))+"\n"
