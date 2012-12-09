from twython import Twython
from time import sleep
import pickle
import datetime
import os

class TweetGetter(object):
    def __init__(self,filename=None):
        self.filename=filename
        if filename==None:
            self.twitterdict={}
            self.maxid=None
        else:
            try:
                picklefile=open(filename, "r")
                self.twitterdict=pickle.load(picklefile)
                picklefile.close()
                self.maxid=int(self.filename[self.filename.index("lastid=")+7:self.filename.index(".pkl")])
            except Exception as detail:
                print "Error loading pickle file: " + str(self.filename) +"\nWill assume empty dictionary and leave file untouched. Error message: " + str(detail)
                self.filename=None
                self.maxid=None

        try:
            self.twython= Twython(app_key="674Getn4iR5ZonBvSZIE6w", app_secret="XIIhDdsCmByqLQG89ED9h7MILQbS4hsMV3ob6hlLYA", oauth_token="27203313-Oujk9Qu6sKe7tBBYYrheAb1r484PViz2w8GShZCeg", oauth_token_secret="cm95hSRUmkloWBVbYrTHuIYA7fSQqFJH5iYGIbw5ZKo")
        except Exception as detail:
            print "Error loading Twython object. Error message: " + str(detail)
            raise Exception(detail)

    def query(self,query,numtweets=500, usemaxid=True):
        if usemaxid==False:
            self.maxid=None
        self.query=query
        ntweets=0
        nmatch=0
        while ntweets<numtweets:
            try:
                if self.maxid!=None:
                    mydict=self.twython.search(q=query, result_type="recent", count="100", max_id=str(self.maxid))
                else:
                    mydict=self.twython.search(q=query, result_type="recent", count="100")

                actualcount=len(mydict["statuses"])
                if actualcount != 0:
                    self.maxid=int(mydict["statuses"][actualcount-1]["id_str"])-1 #int at the moment

                    for item in mydict["statuses"]:
                        if (not (item["id_str"] in self.twitterdict)):
                            mentionslist=[]
                            hashtagslist=[]
                            urlslist=[]
                            text=item["text"].replace(unichr(8220),'"')
                            text=item["text"].replace(unichr(8221),'"')

                            for x in item["entities"]["user_mentions"]:
                                mentionslist.append({"id_str":x["id_str"], "screen_name":x["screen_name"], "name":x["name"]})

                            for x in item["entities"]["hashtags"]:
                                hashtagslist.append(x["text"].lower())

                            for x in item["entities"]["urls"]:
                                hashtagslist.append(x["expanded_url"])

                            self.twitterdict[item["id_str"]]={"screen_name":item["user"]["screen_name"], "name":item["user"]["name"], "user_id_str":item["user"]["id_str"], "user_mentions":mentionslist, "hashtags":hashtagslist, "urls":urlslist, "id_str":item["id_str"], "created_at":item["created_at"], "text":text, "followers_count":item["user"]["followers_count"], "friends_count":item["user"]["friends_count"], "statuses_count":item["user"]["statuses_count"], "retweet_count":item["retweet_count"],"in_reply_to_status_id_str":item["in_reply_to_status_id_str"], "in_reply_to_user_id_str":item["in_reply_to_user_id_str"], "truncated":item["truncated"], "retweeted":item["retweeted"]}
                            ntweets+=1
                        else:
                            nmatch+=1
                            if nmatch==6:
                                print "Grabbing old tweets, stopping."
                                ntweets=numtweets+1
                        
                else:
                    print "Cannot obtain more tweets"
                    ntweets=numtweets+1
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                sleep(300)
                

            print str(ntweets)
            sleep(10)
            
        self.save()

    def save(self):
        now = datetime.datetime.now()
        timestr=now.strftime("%d_%m_%H%M")
        query=self.query.replace('"', "")
        query=query.replace("'", "")
        query=query.replace(" ", "_")
        fname="twitterdata_query="+query+"_time="+timestr+"_lastid="+str(self.maxid)+".pkl"
        self.savedname=fname
        picklefile=open(fname, "w")
        pickle.dump(self.twitterdict,picklefile)
        picklefile.close()
        # if self.filename!=None:
        #     try:
        #         os.remove(self.filename)
        #     except Exception as detail:
        #         print "Unable to remove file: " + str(self.filename)+". Error message: " +str(detail)
        # self.filename=fname
                
        

    def buildUserDB(self, userdict=None):
        #Want to build new dictionary of followers/following for each user we have
        #Need to handle cursoring i.e. only returned in 5000 steps, maybe look up friend/follower count
        # Cursoring pseudocode from documentation:
        # cursor = -1
        # api_path = "https://api.twitter.com/1.1/endpoint.json?screen_name=targetUser" 
        # do {
        #     url_with_cursor = api_path + "&cursor=" + cursor      
        #     response_dictionary = perform_http_get_request_for_url( url_with_cursor )
        #     cursor = response_dictionary[ 'next_cursor' ]
        # }
        # while ( cursor != 0 )
        userslist=[]
        j=0
        for item in self.twitterdict.keys():
            name=self.twitterdict[item]["screen_name"]
            if (not (name in userslist)):
                userslist.append(name)

        if userdict==None:
            userdict={}

        l = len(userslist)
        fname="usersdict_"+self.filename
        for name in userslist:
            if (not (name in userdict.keys())):
                followerslist=self.getFollowers(name, [], -1)
                friendslist=self.getFriends(name, [], -1)
                userdict[name]={"screen_name":name, "followers_list":followerslist, "friends_list":friendslist}
                

            else:
                #Check for new followers, repair possible failures
                try:
                    followerslist=self.getFollowers(name, userdict[name]["followers_list"], -1)
                except KeyError:
                    followerslist=self.getFollowers(name, [], -1)
                try:
                    friendslist=self.getFriends(name, userdict[name]["friends_list"], -1)
                except KeyError:
                    friendslist=self.getFriends(name, [], -1)
                    
                userdict[name]={"screen_name":name, "followers_list":followerslist, "friends_list":friendslist}
            j+=1
            now = datetime.datetime.now()
            timestr=now.strftime("%d_%m_%H%M")
            print "["+timestr+"] "+ name + ": " + str(j) + "/" + str(l)
            if j%100==0:
                picklefile=open(fname, "w")
                pickle.dump(userdict,picklefile)
                picklefile.close()

        picklefile=open(fname, "w")
        pickle.dump(userdict,picklefile)
        picklefile.close()
        

        return userdict


    def fastRepairUserDB(self, userdict):
        #Want to repair None entries in dictionary
        userslist=[]
        j=0
        for item in userdict.keys():
            if ( (userdict[item]["followers_list"]==None) or (userdict[item]["friends_list"]==None)):
                userslist.append(item)

        l = len(userslist)
        fname="usersdict_"+self.filename
        for name in userslist:
            followerslist=self.getFollowers(name, [], -1)
            print len(followerslist)
            friendslist=self.getFriends(name, [], -1)

            if followerslist == None:
                print "Followers BROKEN! " + str(name)
            if friendslist==None:
                print "Friends BROKEN! " + str(name)
                    
            userdict[name]={"screen_name":name, "followers_list":followerslist, "friends_list":friendslist}
            j+=1
            print name + ": " + str(j) + "/" + str(l)
            if j%100==0:
                picklefile=open(fname, "w")
                pickle.dump(userdict,picklefile)
                picklefile.close()

        picklefile=open(fname, "w")
        pickle.dump(userdict,picklefile)
        picklefile.close()
        

        return userdict

    def loadPickle(self, filename):
        picklefile=open(filename,"r")
        data=pickle.load(picklefile)
        picklefile.close()
        return data
    
    def getFollowers(self, name, followerslist, cursor):
        #Recursively get followers
        sleep(7)
        #print "Getting Followers:" + name
        while True:
            try:
                d=self.twython.getFollowersIDs(screen_name=name, cursor=str(cursor))
                cursor=d["next_cursor"]
                #print str(cursor)
                break
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                print name
                print str(cursor)
                if ("The URI requested is invalid" in str(detail)) or ("Unauthorized" in str(detail)):
                    cursor=-1
                    return followerslist
                else:
                    sleep(300)

        # if ((followerslist != []) and (followerslist !=None)):
        #     for item in d["ids"]:
        #         if ( not (item in followerslist)):
        #             followerslist = followerslist + [item]
        #         else:
        #             cursor=-1
        #             break
        # elif followerslist == []:
        #     followerslist=followerslist+d["ids"]
        # elif followerslist==None:
        #     followerslist=d["ids"]

        followerslist=followerslist+d["ids"]
        # print name + ": " +str(len(followerslist))

            
        if cursor>0:
            sleep(7)
            followerslist=self.getFollowers(name, followerslist, cursor)
        # print len(followerslist)
        return followerslist

    def getFriends(self, name, friendslist, cursor):
        #Recursively get followers
        sleep(7)
        #print "Getting Friends:" + name
        while True:
            try:
                d=self.twython.getFriendsIDs(screen_name=name, cursor=str(cursor))
                cursor=d["next_cursor"]
                #print str(cursor)
                break
            except Exception as detail:
                print "Some Twitter error: " + str(detail)
                print name
                print str(cursor)
                if ("The URI requested is invalid" in str(detail)) or ("Unauthorized" in str(detail)):
                    print name
                    cursor=-1
                    return friendslist
                else:
                    sleep(300)

        # if ((friendslist != []) and (friendslist !=None)):
        #     for item in d["ids"]:
        #         if ( not (item in friendslist)):
        #             friendslist = friendslist + [item]
        #         else:
        #             cursor=-1
        #             break
        # elif friendslist == []:
        #     friendslist=friendslist+d["ids"]
        # elif friendslist==None:
        #     friendslist=d["ids"]

        friendslist=friendslist+d["ids"]
                    

        if cursor>0:
            sleep(7)
            friendslist=self.getFriends(name, friendslist, cursor)
        # else:
        return friendslist
        
