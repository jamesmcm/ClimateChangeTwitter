import networkx as nx
import pickle
from classtweetreader import TweetReader
import matplotlib.pyplot as plt


#loop through all retweets
#Tag same retweets somehow
# Find one closest in time - check if following
# Repeat until found then assume that was intermediate source
# See how many find successful sources - probably missing tonnes of data
#ignore double tweets from same user
#Take text after RT @user: and try to match same tweets?

#So write part to remove urls, user mentions
#Unabbreviate text, compare edit distance for typos
# What does it mean that the original source is different?
# Can we solve the original, original source?
# Need to include modified retweets too - drop RT requirement just use edit distance, etc.
# Also gets original
#Use URLS - can get netork by looping over URLs - no assumptions on text, create new thread when not retweet
#Can then see different threads from Tweet buttons on articles
#Can then plot propagation against time
# Write expansion for:
# http://fb.me/vUfScHp3
# http://flpbd.it/cly7C
# http://bit.ly/TI9AR5
# http://j.mp/Qj3YST
# http://ow.ly/fmgbG
# http://zite.to/XhGeRV
# http://vsb.li/676sfl
# http://tinyurl.com/akocj6z
# http://lnkd.in/kycnMe
# http://buff.ly/XMQ9hw
# Perhaps just visit URL then get final URL, strip of # tags
# Remove any # markers from URL
# http://grist.org/news/if-youre-27-or-younger-youve-never-experienced-a-colder-than-average-month/#.UKeZolfmFBx.twitter
def retweetplot(twitterdictfilename, userdictfilename):
    myreader=TweetReader(twitterdictfilename)
    usersdict=myreader.loadDict(userdictfilename)
    myreader.purgeDead(usersdict)
    #restrict to those with 3 tweets or more
    usernamesdict=myreader.getUsernames()
    idmap=myreader.getUserIDMap()
    screenmap=myreader.getScreenNameMap()
    #retweetlist=myreader.getRetweets()
    #print idmap
    graph=nx.DiGraph()
    for item in myreader.twitterdict.keys():
        if ("colder" in myreader.twitterdict[item]["text"]) and ("month" in myreader.twitterdict[item]["text"]):
            graph.add_node(item, time=myreader.convertTime(myreader.twitterdict[item]["created_at"]))
            #If non retweet just plot node.
            #If retweet check if follows original source, if so create direct edge
            #If not then look at closest tweets beforehand, see if they follow them
            #Then do that tweet and so on
            if myreader.twitterdict[item]["text"][0:2] == "RT":
                s=myreader.twitterdict[item]["text"]

                try:
                    atindex=s.index("@")
                    breakif=False
                except:
                    breakif=True
                # TODO
                if breakif==False:
                    keepgoing=True
                    i=1
                    while keepgoing==True:
                        try:
                            if not (s[atindex+i] in self.valid_characters):
                                keepgoing=False
                                endindex=i
                            else:
                                i+=1
                        except:
                            keepgoing=False
                            endindex=i

                source_screen_name=s[atindex+1:atindex+endindex]
                created_at= myreader.twitterdict[item]["created_at"]
                id_str=str(item)
                text=s[atindex+endindex+1:]
                screen_name= myreader.twitterdict[item]["screen_name"]

                if int(screenmap[source_screen_name]) in usersdict[screen_name]:
                    #Need id number of source's tweet
                    #TODO
                    tweetidsource=
                    graph.add_edge(tweetidsource, item)

            else:
                pass


            
            #myreader.convertTime(timestring)

    

def plotffnetwork(twitterdictfilename, userdictfilename):
    #Plot following/follower network
    myreader=TweetReader(twitterdictfilename)
    usersdict=myreader.loadDict(userdictfilename)
    myreader.purgeDead(usersdict)
    #restrict to those with 3 tweets or more
    usernamesdict=myreader.getUsernames(minimum=10)
    idmap=myreader.getUserIDMap()
    #print idmap
    graph=nx.DiGraph()
    for name in usernamesdict.keys():
        graph.add_node(name)
        try:
            for ids in usersdict[name]["followers_list"]:
                #add follower
                try:
                    #print usersdict[name]["screen_name"]
                    #print ids
                    followername=idmap[str(ids)]
                    if followername in usernamesdict.keys():
                        graph.add_edge(name, followername)
                    else:
                        print "Name missing in dict: " + str(followername)
                except:
                    #User was not in our subset, probably better way of doing this
                    pass

            for ids in usersdict[name]["friends_list"]:
                #add friend/following
                try:
                    friendname=idmap[str(ids)]
                    if friendname in usernamesdict.keys():
                        graph.add_edge(friendname,name)
                    else:
                        print "Name missing in dict: " + str(friendname)
                except:
                    #User was not in our subset, probably better way of doing this
                    pass
        except:
            pass
            #fix me later
    print "Built graph"
    nx.write_gml(graph, "friendfollower.gml")
    print "Wrote graph"
    # nx.draw(graph)
    # plt.show()


def plotnaivertnetwork(twitterdictfilename):
    #Plot naive retweet network i.e. retweeters to original source
    myreader=TweetReader(twitterdictfilename)
    print "Loaded tweets"
    retweetlist=myreader.getRetweets()
    print "Loaded retweets"
    graph=nx.DiGraph()
    for item in retweetlist:
        try:
            graph[item["source_screen_name"]][item["screen_name"]]['weight']+=1
        except:
            graph.add_edge(item["source_screen_name"], item["screen_name"], weight=1)

    print "Built graph"
    nx.write_gml(graph, "test.gml")
    print "Wrote graph"
    # nx.draw(graph)
    # print "Drew graph"
    # plt.savefig("test.png")
    # print "Saved graph"
    # plt.show()
    # print "Shown graph"
    


# plotnaivertnetwork("twitterdata_query=Global_Warming_time=02_12_2237_lastid=274513338904506370.pkl")
plotffnetwork("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl", "usersdict_twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
