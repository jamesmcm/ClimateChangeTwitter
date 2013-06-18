import sqlite3 as lite
import sys
import networkx as nx
import pickle
from classtweetreader import TweetReader
import matplotlib.pyplot as plt
from classtweetgetter import TweetGetter
from classtweetgetter import DBTweetGetter
from time import sleep
import string
import sys

valid_characters = string.ascii_letters
valid_characters += string.digits
valid_characters += '_'

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
    mygetter=TweetGetter()
    usersdict=myreader.loadDict(userdictfilename)
    myreader.purgeDead(usersdict)
    #restrict to those with 3 tweets or more
    usernamesdict=myreader.getUsernames()
    idmap=myreader.getUserIDMap()
    screenmap=myreader.getScreenNameMap()
    #retweetlist=myreader.getRetweets()
    #print idmap
    graph=nx.DiGraph()
    subdict={}
    unknownlist=[]
    for item in myreader.twitterdict.keys():
        if ("colder" in myreader.twitterdict[item]["text"]) and ("month" in myreader.twitterdict[item]["text"]):
            subdict[item]=myreader.twitterdict[item]
            subdict[item]["converted_time"]=myreader.convertTime(myreader.twitterdict[item]["created_at"])
            #myreader.convertTime(timestring)


        #Get user IDs for unknown source usernames to check following status
    for item in subdict.keys():
        if subdict[item]["text"][0:2] == "RT":
            s=subdict[item]["text"]
            #print s

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
                        if not (s[atindex+i] in myreader.valid_characters):
                            keepgoing=False
                            endindex=i
                        else:
                            i+=1
                    except:
                        keepgoing=False
                        endindex=i

            source_screen_name=s[atindex+1:atindex+endindex]
            id_str=str(item)
            text=s[atindex+endindex+1:]
            screen_name= subdict[item]["screen_name"]
            subdict[item]["retweet"]=True
            subdict[item]["source_screen_name"]=source_screen_name
            try:
                sourceid=screenmap[source_screen_name]
            except:
                unknownlist.append(source_screen_name)
        else:
            subdict[item]["retweet"]=False
            

    print len(unknownlist)
    print unknownlist
    for name in unknownlist:
            screenmap[name]=mygetter.getIDfromUser(name)
            
        

    for item in subdict.keys():
        graph.add_node(subdict[item]["screen_name"], time=subdict[item]["converted_time"])
        #If non retweet just plot node.
        #If retweet check if follows original source, if so create direct edge
        #If not then look at closest tweets beforehand, see if they follow them
        #Then do that tweet and so on
        if subdict[item]["retweet"]==True:
            source_screen_name=subdict[item]["source_screen_name"]
            screen_name=subdict[item]["screen_name"]
            #if original source then just plot direct edge

            if int(screenmap[source_screen_name]) in usersdict[screen_name]["friends_list"]:
                #Need id number of source's tweet
                #TODO
                # tweetidsource=-5
                # for item2 in subdict.keys():
                #     if ("colder" in subdict[item2]["text"]) and ("month" in subdict[item2]["text"]):
                #         if subdict[item2]["user"]["screen_name"] == source_screen_name:
                #             tweetidsource=item2
                #             break
                # if tweetidsource<0:
                #     print "Do not have original source in data set for user: "+ str(screen_name) +" and source: " + str(source_screen_name) +"\n"
                # else:
                #     graph.add_edge(tweetidsource, item)
                graph.add_edge(source_screen_name, screen_name, time=subdict[item]["converted_time"])

            else:
                edgenum=0
                #The hard part, need to convert all times (do this earlier?) find most recent, check against users, repeat
                mintime=subdict[item]["converted_time"]
                for item2 in subdict.keys():
                    if (subdict[item2]["converted_time"]<mintime) and (subdict[item2]["retweet"]==True):
                        if subdict[item2]["source_screen_name"]==source_screen_name:
                            if int(screenmap[subdict[item2]["screen_name"]]) in usersdict[subdict[item]["screen_name"]]["friends_list"]:
                                graph.add_edge(subdict[item2]["screen_name"], subdict[item]["screen_name"] ,time=subdict[item]["converted_time"])
                                edgenum+=1
                if edgenum==0:
                    print "Intermediaries not found for user: " + screen_name + ", source: " + source_screen_name +".\n"
                    graph.add_edge(source_screen_name, screen_name, time=subdict[item]["converted_time"])


    print "Built graph"
    nx.write_gml(graph, "testrt2.gml")
    print "Wrote graph"

    

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


def dbplotnaivertnetwork(dbname,tablename):
    #Plot naive retweet network i.e. retweeters to original source
    con = lite.connect(dbname)
    mintime=1358090418
    cur=con.cursor()
    cur.execute("SELECT ScreenName, RetweetSource FROM "+tablename+" WHERE IsRetweet=1 AND RetweetSource<>'' AND ConvertedTime>" + str(mintime))
    data=cur.fetchall()
    graph=nx.DiGraph()
    for item in data:
        try:
            graph[item[1].lower()][item[0].lower()]['weight']+=1
        except:
            graph.add_edge(item[1].lower(), item[0].lower(), weight=1)

    print "Built graph"
    nx.write_gml(graph, "naivertnew" + tablename+ ".gml")
    print "Wrote graph"
    # nx.draw(graph)
    # print "Drew graph"
    # plt.savefig("test.png")
    # print "Saved graph"
    # plt.show()
    # print "Shown graph"


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
    


def dbplotffnetwork():
    graph=nx.DiGraph()
    #Plot following/follower network
    #restrict to those with 3 tweets or more
    mintime=1358090418
    maxtime=1363963163
    mygetter=DBTweetGetter(None,None)
    con = lite.connect("tweetsdb.db")
    cur=con.cursor()
    ucon = lite.connect("userdb.db")
    ucur=ucon.cursor()
    tusers=[]
    users=[]
    
    cur.execute("SELECT ScreenName FROM htglobalwarming WHERE ConvertedTime > "+str(mintime) +" AND ConvertedTime < " + str(maxtime) + " COLLATE NOCASE")
    temp=cur.fetchall()
    for item in temp:
        tusers.append(item[0].lower())
    for item in tusers:
        if not (item in users):
            if tusers.count(item)>7:
                users.append(item)

    print len(users)


    # cur.execute("SELECT ScreenName FROM htclimatechange WHERE ConvertedTime > "+str(mintime)+" AND ConvertedTime < " + str(maxtime) + " COLLATE NOCASE")
    # temp=cur.fetchall()
    # tusers=[]
    # for item in temp:
    #     tusers.append(item[0].lower())
    # for item in tusers:
    #     if not (item in users):
    #         if tusers.count(item)>29:
    #             users.append(item)

    # print len(users)


    # cur.execute("SELECT ScreenName FROM htagw WHERE ConvertedTime > "+str(mintime) + " COLLATE NOCASE")
    # temp=cur.fetchall()
    # tusers=[]
    # for item in temp:
    #     tusers.append(item[0].lower())
    # for item in tusers:
    #     if not (item in users):
    #         if tusers.count(item)>2:
    #             users.append(item)

    # print len(users)


    #aim for 380
    #sys.exit("Hammertime")
    i=0
    try:
        users.remove("undercoverzen")
        users.remove("jivelad")
        users.remove("anabananazavala")
        #TODO Formalise this
    except:
        pass
    for user in users:
        print "User " + str(i)+"/"+str(len(users))
        i+=1
        #For each user check which other users are in friends, followers
        ucur.execute("SELECT FriendId FROM friends WHERE ScreenName='"+user.lower()+"' COLLATE NOCASE")
        frl=[]
        temp=ucur.fetchall()
        skip=False
        if len(temp)==0:
            #get friends
            print "Downloading friends for " + user.lower()
            friendslist=mygetter.getFriends(user.lower(), [], -1)
            if friendslist!="FAIL":
                for friend in friendslist:
                    ucur.execute("INSERT INTO friends VALUES('" + user.lower() + "'," + str(friend) + ")" )
                frl=friendslist
            else:
                skip=True
                try:
                    users.remove(user.lower())
                except:
                    pass
            sleep(10)
                
        else:
            for item in temp:
                frl.append(item[0])


        ucur.execute("SELECT FollowerId FROM followers WHERE ScreenName='"+user+"' COLLATE NOCASE")
        fol=[]
        temp=ucur.fetchall()
        skip=False
        if len(temp)==0:
            #get friends
            print "Downloading followers for " + user.lower()
            followerslist=mygetter.getFollowers(user.lower(), [], -1)
            if followerslist!="FAIL":
                for follower in followerslist:
                    ucur.execute("INSERT INTO followers VALUES('" + user.lower() + "'," + str(follower) + ")" )
                fol=followerslist
            else:
                skip=True
                try:
                    users.remove(user.lower())
                except:
                    pass
            sleep(10)
                
        else:
            for item in temp:
                fol.append(item[0])

        ucon.commit()
        if skip==False:
            graph.add_node(user.lower())
            for other in users:
                skip2=False
                ucur.execute("SELECT UserId FROM usermap WHERE ScreenName='"+other.lower()+"' COLLATE NOCASE")
                temp=ucur.fetchall()
                if len(temp)==0:
                    #get ID from web
                    print "Downloading userid for " + other.lower()
                    x=mygetter.getIDfromUser(other.lower())
                    if x!="FAIL":
                        ucur.execute("INSERT INTO usermap VALUES('" +other.lower()+ "'," + x + ")" )
                        sid=x
                        ucon.commit()
                    else:
                        try:
                            users.remove(other.lower())
                        except:
                            pass
                        skip2=True
                    sleep(10)
                else:
                    sid=temp[0][0]
                if skip2==False:
                    if sid in fol:
                        graph.add_edge(other.lower(), user.lower())
                    if sid in frl:
                        graph.add_edge(user.lower(), other.lower())

    print "Built graph"
    nx.write_gml(graph, "newfriendfollowerhtccgt29.gml")
    ucon.commit()
    con.close()
    ucon.close()
    print "Wrote graph"
    # nx.draw(graph)
    # plt.show()

def dbconversation(tablename):
    #creates edges from OP to mentioned
    graph=nx.DiGraph()
    #Plot following/follower network
    #restrict to those with 3 tweets or more
    mygetter=DBTweetGetter(None,None)
    con = lite.connect("tweetsdb.db")
    cur=con.cursor()
    mintime=1358090418
    cur.execute("SELECT DISTINCT ScreenName FROM "+tablename+" WHERE ConvertedTime>"+str(mintime) + " AND IsRetweet=0")
    l=cur.fetchall()

    users=[]
    for item in l:
        users.append(item[0].lower())
    cur.execute("SELECT Tweet, ScreenName FROM "+tablename+" WHERE ConvertedTime>"+str(mintime) + " AND IsRetweet=0")
    d=cur.fetchall()
    lz=len(d)
    z=1
    for item in d:
        #print "Tweet " +str(z)+"/"+str(lz)
        z+=1
        if ("@" in item[0].lower()) and ("rt:" not in item[0].lower()):
            #Continue until character not in valid set, then check if is user in set
            #First count number of @s
            names=[]
            c=item[0].lower().count("@")
            start=0
            for i in range(c):
                s=item[0].lower().index("@", start)
                start=s+1
                k=0
                try:
                    j=item[0][start]
                except:
                    print item[0]
                while j in valid_characters:
                    k+=1
                    try:
                        j=item[0][start+k]
                    except:
                        j="/"
                names.append(item[0][start:start+k].lower())

            for name in names:
                if name.lower() in users and name.lower()!=item[1].lower():
                    try:
                        graph[item[1].lower()][ name.lower()]['weight']+=1
                    except:
                        graph.add_edge(item[1].lower(),name.lower(), weight=1)

                    #graph.add_edge(item[1].lower(), name.lower())

    print "Built graph"
    nx.write_gml(graph, "newconv"+tablename+"nortdir.gml")
    print "Wrote graph"

                
# plotnaivertnetwork("twitterdata_query=Global_Warming_time=02_12_2237_lastid=274513338904506370.pkl")
#plotffnetwork("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl", "usersdict_twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
#retweetplot("twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl", "usersdict_twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl")
#dbplotnaivertnetwork("tweetsdb.db", "htagw")
#dbplotffnetwork()
dbconversation("htglobalwarming")
