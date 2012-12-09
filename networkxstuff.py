import networkx as nx
import pickle
from classtweetreader import TweetReader
import matplotlib.pyplot as plt


def plotffnetwork(twitterdictfilename, userdictfilename):
    #Plot following/follower network
    myreader=TweetReader(twitterdictfilename)
    usersdict=myreader.loadDict(userdictfilename)
    myreader.purgeDead(usersdict)
    #restrict to those with 3 tweets or more
    usernamesdict=myreader.getUsernames()
    idmap=myreader.getUserIDMap()
    print idmap
    graph=nx.DiGraph()
    for name in usernamesdict.keys():
        graph.add_node(name)
        try:
            for ids in usersdict[name]["followers_list"]:
                #add follower
                try:
                    #print usersdict[name]["screen_name"]
                    print ids
                    followername=idmap[ids]
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
                    friendname=idmap[ids]
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
