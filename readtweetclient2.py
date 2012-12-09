from classtweetreader import TweetReader
#from classtweetgetter import TweetGetter

myTweetReader=TweetReader("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
#myTweetGetter=TweetGetter("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
#myTweetReader.printHashtagCount(500)
#myTweetReader.printWordCount(500)
#print len(myTweetReader.twitterdict.keys())
#userdict=myTweetGetter.loadPickle("usersdict_twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
#myTweetGetter.buildUserDB(userdict)
#print myTweetReader.getUsernames()
for item in myTweetReader.twitterdict.keys():
    if not ( " #climatechange" in myTweetReader.twitterdict[item]["text"].lower() or "#climatechange " in myTweetReader.twitterdict[item]["text"].lower()):
        print myTweetReader.twitterdict[item]["text"]

