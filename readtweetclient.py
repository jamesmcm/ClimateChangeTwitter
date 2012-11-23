from classtweetreader import TweetReader

myTweetReader=TweetReader("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
# myTweetReader.printHashtagCount(200)
# myTweetReader.printWordCount(1000)
# print len(myTweetReader.twitterdict.keys())
print myTweetReader.getUsernames()
