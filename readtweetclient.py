from classtweetreader import TweetReader
from classtweetgetter import TweetGetter

myTweetReader=TweetReader("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
myTweetGetter=TweetGetter("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
# myTweetReader.printHashtagCount(200)
# myTweetReader.printWordCount(1000)
# print len(myTweetReader.twitterdict.keys())
userdict=myTweetGetter.loadPickle("usersdict_twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
#myTweetGetter.buildUserDB(userdict)
myTweetGetter.fastRepairUserDB(userdict)
#print myTweetReader.getUsernames()
