import sqlite3 as lite
import sys
import networkx as nx
import pickle
import matplotlib.pyplot as plt
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
