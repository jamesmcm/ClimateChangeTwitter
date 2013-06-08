import sqlite3 as lite
import sys
import numpy as np
from classtweetgetter import DBTweetGetter
from time import sleep


mygetter=DBTweetGetter(None,None)
con=lite.connect("tweetsdb.db")
cur=con.cursor()

ucon=lite.connect("userdb.db")
ucur=ucon.cursor()
crawlers=[]
chainlengths=[]
nsame=[]
noded={}
chainlfile=open("chaindata.txt","w")
nsamefile=open("nsamedata.txt","w")
class chainCrawler(object):
    #note this method will repeat chains if there is V structure, should be minimal effect
    def __init__(self, node, n):
        self.n=n
        self.node=node
        self.stopwalk=False

    def walk(self):
        while self.stopwalk==False:
            self.step()
        return 0
    def step(self):
        if len(self.node[1])==0:
            #basecase, stop walk, add to data
            self.stopwalk=True
            chainlfile.write(str(self.n)+"\n")
        else:
            #set me to be first child, add additional children to list
            self.n+=1
           
            if len(self.node[1])>1:
                for i in range(1,len(self.node[1])):
                    crawlers.append(chainCrawler(noded[self.node[1][i]], self.n))
            self.node=noded[self.node[1][0]]
tablename="htclimatechange"

cur.execute("SELECT Tweet, ScreenName, RetweetSource, ConvertedTime FROM " + tablename + " WHERE IsRetweet=1 AND RetweetSource <> ''")

d=cur.fetchall()

#grab middle by percentage, check for substrings in total set, (if length greater than 1) build graph
#need to remove tweets from subsample after found
retweets=[]
ttweets=[]
# for item in d:
#     retweets.append(item)
retweets=d

cur.execute("SELECT Tweet, ScreenName, RetweetSource, ConvertedTime FROM " + tablename)
x=cur.fetchall()
# for item in x:
#     ttweets.append(item[0])


i =0
while i<len(retweets):
    t=retweets[i][0]
    t=t[int(0.35*len(t)):int(0.65*len(t))]
    j=i+1
    while j<len(retweets):
        if t in retweets[j][0]:
            retweets.pop(j)
        else:
            j+=1

    i+=1


con.close()

cl=0
for t0 in retweets:

    cl+=1
    # print t0
    # print t0[0]
    # print t0[0][int(0.35*len(t0[0])):int(0.65*len(t0[0]))]
    t=t0[0][int(0.35*len(t0[0])):int(0.65*len(t0[0]))]
    noded={} #{node: ([parentslist], [childslist])}
    subset=[]
    subset.append(t0)
    for item in x:
        if (t in item[0]) and (item[1].lower()!=t0[1]):
            #Add to subset for this tweet
            subset.append(item)
    #have subset, need plot, etc.
    #{node: [parents],[children]}
    print "Number of retweets:" + str(len(subset))
    kl=0
    for item in subset:
        print "Set: " + str(cl)+"/"+str(len(retweets)) + ", Tweet "+str(kl)+"/"+str(len(subset))
        kl+=1
        if item[2].lower()!="-" and item[2].lower()!="''" and item[2].lower()!=None:
            skip=False
            #check if user is following source, need idmap and user details
            #pull data if necessary
            ucur.execute("SELECT FriendId FROM friends WHERE ScreenName='"+item[1].lower()+"' COLLATE NOCASE")
            fl=ucur.fetchall()
            if len(fl)==0:
                #grab friends
                print "Downloading friends for " + item[1].lower()
                friendslist=mygetter.getFriends(item[1].lower(), [], -1)
                if friendslist!="FAIL":
                    for friend in friendslist:
                        ucur.execute("INSERT INTO friends VALUES('" + item[1].lower() + "'," + str(friend) + ")" )
                    fl=friendslist
                else:
                    skip=True
                sleep(10)
                    #should drop deleted user datas here
            else:
                l2=fl
                fl=[]
                for le in l2:
                    fl.append(le[0])
            #get source id
            ucur.execute("SELECT UserId FROM usermap WHERE ScreenName='"+item[2].lower()+"' COLLATE NOCASE")
            sid=ucur.fetchall()
            if len(sid)==0:
                #get ID from web
                print "Downloading userid for " + item[2].lower()
                x=mygetter.getIDfromUser(item[2].lower())
                if x!="FAIL":
                    ucur.execute("INSERT INTO usermap VALUES('" +item[2].lower()+ "'," + x + ")" )
                    sid=x
                else:
                    skip=True
                sleep(10)
            else:
                sid=sid[0][0]
            ucon.commit()
            #Do checking shit here, form list, etc.
            if skip==False:
                if sid in fl:
                    #make direct connection: append source to parents list, attempt to append self to child list of source
                    if item[1].lower() in noded:
                        if not (item[2].lower() in noded[item[1].lower()][0]):
                            npl=noded[item[1].lower()][0]
                            ncl=noded[item[1].lower()][1]
                            npl.append(item[2].lower())
                            noded[item[1].lower()]=(npl,ncl) 
                    else:
                        noded[item[1].lower()]=([item[2].lower()], [])

                    if item[2].lower() in noded:
                        if not (item[1].lower() in noded[item[2].lower()][1]):
                            npl=noded[item[2].lower()][0]
                            ncl=noded[item[2].lower()][1]
                            ncl.append(item[1].lower())
                            noded[item[2].lower()]=(npl,ncl) 
                    else:
                        noded[item[2].lower()]=([], [item[1].lower()])

                        
                else:
                    #find other connection, hard - convertedtime item[3]
                    edgenum=0
                    for twe in subset:
                        if (item[3]>twe[3]) and (item[2].lower()==twe[2].lower()):
                            # print "Actually tested intermediary"
                            ucur.execute("SELECT UserId FROM usermap WHERE ScreenName='"+twe[1].lower()+"' COLLATE NOCASE")
                            uskip=False
                            uid=ucur.fetchall()
                            if len(uid)==0:
                                #get ID from web
                                x=mygetter.getIDfromUser(twe[1].lower())
                                print "Downloading userid for " + twe[1].lower()
                                sleep(10)
                                if x!="FAIL":
                                    ucur.execute("INSERT INTO usermap VALUES('" +twe[1].lower()+ "'," + x + ")" )
                                    uid=x
                                else:
                                    uskip=True
                            else:
                                uid=uid[0][0]
                            ucon.commit()
                            if uskip==False:
                                if uid in fl:
                                    #make connection: append int. source to parents list, attempt to append self to child list of source
                                    if item[1].lower() in noded:
                                        if not (twe[1].lower() in noded[item[1].lower()][0]):
                                            npl=noded[item[1].lower()][0]
                                            ncl=noded[item[1].lower()][1]
                                            npl.append(twe[1].lower())
                                            noded[item[1].lower()]=(npl,ncl) 
                                    else:
                                        noded[item[1].lower()]=([twe[1].lower()], [])

                                    if twe[1].lower() in noded:
                                        if not (item[1].lower() in noded[twe[1].lower()][1]):
                                            npl=noded[twe[1].lower()][0]
                                            ncl=noded[twe[1].lower()][1]
                                            ncl.append(item[1].lower())
                                            noded[twe[1].lower()]=(npl,ncl) 
                                    else:
                                        noded[twe[1].lower()]=([], [item[1].lower()])
                                    edgenum+=1
                    if edgenum==0:
                            print "Intermediaries not found for user: " + item[1].lower() + ", source: " + item[2].lower() +".\n"
                            #Link to source node directly
                            if (item[1].lower() in noded):
                                if not (item[2].lower() in noded[item[1].lower()][0]):
                                    npl=noded[item[1].lower()][0]
                                    ncl=noded[item[1].lower()][1]
                                    npl.append(item[2].lower())
                                    noded[item[1].lower()]=(npl,ncl) 
                            else:
                                noded[item[1].lower()]=([item[2].lower()], [])
                        
                            if item[2].lower() in noded:
                                if not (item[1] in noded[item[2].lower()][1]):
                                    npl=noded[item[2].lower()][0]
                                    ncl=noded[item[2].lower()][1]
                                    ncl.append(item[1].lower())
                                    noded[item[2].lower()]=(npl,ncl) 
                            else:
                                noded[item[2].lower()]=([], [item[1].lower()])

            else:
                #Just add node (but need followers?)
                if not (item[1].lower() in noded):
                    noded[item[1].lower()]=([],[])
    #print noded
    #nsame.append(len(noded.keys()))
    nsamefile.write(str(len(noded.keys()))+"\n")
    #noded complete, write algorithm to calculate average chain length
    for nomo in noded.keys():
        if len(noded[nomo][0])==0:
            #no parents
            #create object
            crawlers.append(chainCrawler(noded[nomo], 0))
    v=0
    while v<len(crawlers):
        crawlers[v].walk()
        crawlers.pop(0)
    chainlfile.flush()
    nsamefile.flush()
chainlfile.close()
nsamefile.close()
# print nsame
# print len(nsame)
# print np.mean(nsame)
# print "---"
# print chainlengths
# print len(chainlengths)
# print np.mean(chainlengths)
    
                        
ucon.close()
# def retweetplot(subset):
#     graph=nx.DiGraph()
#     subdict={}
#     unknownlist=[]

#     print len(unknownlist)
#     print unknownlist
#     for name in unknownlist:
#             screenmap[name]=mygetter.getIDfromUser(name)
#     for item in subdict.keys():
#         graph.add_node(subdict[item]["screen_name"], time=subdict[item]["converted_time"])
#         #If non retweet just plot node.
#         #If retweet check if follows original source, if so create direct edge
#         #If not then look at closest tweets beforehand, see if they follow them
#         #Then do that tweet and so on
#         if subdict[item]["retweet"]==True:
#             source_screen_name=subdict[item]["source_screen_name"]
#             screen_name=subdict[item]["screen_name"]
#             #if original source then just plot direct edge

#             if int(screenmap[source_screen_name]) in usersdict[screen_name]["friends_list"]:
#                 graph.add_edge(source_screen_name, screen_name, time=subdict[item]["converted_time"])

#             else:
#                 edgenum=0
#                 #The hard part, need to convert all times (do this earlier?) find most recent, check against users, repeat
#                 mintime=subdict[item]["converted_time"]
#                 for item2 in subdict.keys():
#                     if (subdict[item2]["converted_time"]<mintime) and (subdict[item2]["retweet"]==True):
#                         if subdict[item2]["source_screen_name"]==source_screen_name:
#                             if int(screenmap[subdict[item2]["screen_name"]]) in usersdict[subdict[item]["screen_name"]]["friends_list"]:
#                                 graph.add_edge(subdict[item2]["screen_name"], subdict[item]["screen_name"] ,time=subdict[item]["converted_time"])
#                                 edgenum+=1
#                 if edgenum==0:
#                     print "Intermediaries not found for user: " + screen_name + ", source: " + source_screen_name +".\n"
#                     graph.add_edge(source_screen_name, screen_name, time=subdict[item]["converted_time"])


#     print "Built graph"
#     nx.write_gml(graph, "testrt2.gml")
#     print "Wrote graph"
