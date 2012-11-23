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
            self.save()
            sleep(10)

    def save(self):
        now = datetime.datetime.now()
        timestr=now.strftime("%d_%m_%H%M")
        fname="twitterdata_query="+self.query+"_time="+timestr+"_lastid="+str(self.maxid)+".pkl"
        picklefile=open(fname, "w")
        pickle.dump(self.twitterdict,picklefile)
        picklefile.close()
        if self.filename!=None:
            try:
                os.remove(self.filename)
            except Exception as detail:
                print "Unable to remove file: " + str(self.filename)+". Error message: " +str(detail)
        self.filename=fname
                
        

