from classtweetgetter import TweetGetter
from classtweetreader import TweetReader


myTweets=TweetGetter()
myTweets.query('#climate',160000, False)

#Write log file
# with open("GlobalWarming.txt", "a") as myfile:
#     readTweet=TweetReader(filename=None, dict=myTweets.twitterdict)
#     print "Total number of tweets: " + str(len(myTweets.twitterdict.keys()))
#     myfile.write("Total number of tweets: " + str(len(myTweets.twitterdict.keys())))
#     udict=readTweet.getUsernames()
#     print "Total number of users: " + str(len(udict.keys()))
#     myfile.write("Total number of tweets: " + str(len(myTweets.twitterdict.keys())))
#     for item in udict.items():
#         if item[1]<3:
#             del udict[item[0]]
#     print "Total number of users with 3 tweets or more: " + str(len(udict.keys()))
#     myfile.write("Total number of users with 3 tweets or more: " + str(len(udict.keys())))

