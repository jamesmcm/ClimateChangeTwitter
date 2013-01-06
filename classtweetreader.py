import pickle
import operator
import string
from twython import Twython


class TweetReader(object):
    def __init__(self, filename=None, dict=None):
        if filename==None and dict!=None:
            self.twitterdict=dict
        else:
            picklefile=open(filename,"r")
            self.twitterdict=pickle.load(picklefile)
            self.filename=filename
            picklefile.close()
        self.valid_characters = string.ascii_letters
        self.valid_characters += string.digits
        self.valid_characters += '_'

    def printWordCount(self, minimum=0):
        worddict={}

        for item in self.twitterdict.keys():
            line=self.twitterdict[item]["text"]
            line=line.replace(".","")
            line=line.replace(",","")
            line=line.replace(":","")
            line=line.replace("\n","")
            line=line.replace("?","")


            words=line.split(" ")
            for word in words:
                word=word.lower()
                if not (word in ['about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could', 'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here', 'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in', 'into', 'is', 'isnt', 'it', 'its', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours ', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'were', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves', '', '&amp;', '2', 'can', ')', '(', '-', 'via', '|', 'a']):
                    try:
                        worddict[word]+=1
                    except:
                        worddict[word]=1

        #Delete items with count under minimum
        for item in worddict.items():
            if item[1]<minimum:
                del worddict[item[0]]
        #Make sorted representation
        sorteddict = sorted(worddict.iteritems(), key=operator.itemgetter(1))
        print sorteddict
        return worddict

    def printHashtagCount(self, minimum=0):
        hashtagdict={}

        for item in self.twitterdict.keys():
            nonduplist=[]
            for htag in self.twitterdict[item]["hashtags"]:
                if not (htag in nonduplist):
                    nonduplist.append(htag)

            
            for hashtag in nonduplist:
                try:
                    hashtagdict[hashtag]+=1
                except:
                    hashtagdict[hashtag]=1

        for item in hashtagdict.items():
            if item[1]<minimum:
                del hashtagdict[item[0]]
        sorteddict = sorted(hashtagdict.iteritems(), key=operator.itemgetter(1))
        print sorteddict
        return hashtagdict
        
    def getRetweets(self):

        #Return dict of poster name, source name, tweet and time
        returnlist=[]
        for item in self.twitterdict.keys():
            if self.twitterdict[item]["text"][0:2] == "RT":
                s=self.twitterdict[item]["text"]
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

                    returnlist.append({"text":s[atindex+endindex+1:],"screen_name": self.twitterdict[item]["screen_name"], "created_at": self.twitterdict[item]["created_at"], "source_screen_name":s[atindex+1:atindex+endindex], "id_str":str(item)})

        return returnlist

    #Get usernames
    def getUsernames(self, minimum=0):
        usersdict={}
        for item in self.twitterdict.keys():
            try:
                usersdict[self.twitterdict[item]["screen_name"]]+=1
            except:
                usersdict[self.twitterdict[item]["screen_name"]]=1

        for item in usersdict.items():
            if item[1]<minimum:
                del usersdict[item[0]]

        return usersdict

    def purgeDead(self, userdict):
        for item in self.twitterdict.keys():
            if not ( self.twitterdict[item]["screen_name"] in userdict.keys()):
                del self.twitterdict[item]


    def sortDict(self, dict1):
        sorteddict = sorted(dict1.iteritems(), key=operator.itemgetter(1))
        return sorteddict


    def save(self, filename=None):
        if filename==None:
            filename=self.filename
        
        picklefile=open(filename,"w")
        pickle.dump(self.twitterdict,picklefile)
        picklefile.close()

    def loadDict(self, filename):
        pfile=open(filename, "r")
        dict=pickle.load(pfile)
        pfile.close()
        return dict

    def getUserIDMap(self):
        idmap={}
        for item in self.twitterdict.keys():
            idmap[self.twitterdict[item]["user_id_str"]]=self.twitterdict[item]["screen_name"]
        return idmap

    def getScreenNameMap(self):
        idmap={}
        for item in self.twitterdict.keys():
            idmap[self.twitterdict[item]["screen_name"]]=self.twitterdict[item]["user_id_str"]
        return idmap

    def convertTime(self, timestring):
        #Fri Nov 16 22:31:39 +0000 2012
        lts=timestring.split(" ")
        tt=lts[3].split(":")
        monthdict={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        dt=datetime.datetime(int(lts[5]), int(monthdict[lts[1]]), int(lts[2]),int(tt[0]),int(tt[1]),int(tt[2]))
        return int(time.mktime(dt.timetuple()))

