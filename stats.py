import sqlite3 as lite
import time
import datetime

con=lite.connect("tweetsdb.db")
cur=con.cursor()
ct=1358090418
maxtime=1369923484
def countrecords():
    l=[]
    t=0
    cur.execute("SELECT COUNT(*) FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    t+=d[0][0]
    l.append(d[0][0])
    cur.execute("SELECT COUNT(*) FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    t+=d[0][0]
    l.append(d[0][0])
    cur.execute("SELECT COUNT(*) FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    t+=d[0][0]
    l.append(d[0][0])
    print t
    print l

def countretweets():
    l=[]
    t=0
    cur.execute("SELECT COUNT(*) FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) +" AND IsRetweet=1")
    d=cur.fetchall()
    t+=d[0][0]
    l.append(d[0][0])
    cur.execute("SELECT COUNT(*) FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) +" AND IsRetweet=1")
    d=cur.fetchall()
    t+=d[0][0]
    l.append(d[0][0])
    cur.execute("SELECT COUNT(*) FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) +" AND IsRetweet=1")
    d=cur.fetchall()
    t+=d[0][0]
    l.append(d[0][0])
    print t
    print l


def countmentions():
    l=[]
    t=0
    cur.execute("SELECT Tweet FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) +" AND IsRetweet=0")
    d=cur.fetchall()
    c=0
    for item in d:
        if ("@" in item[0]) and (not ("RT:" in item[0])):
            c+=1
            t+=1
    l.append(c)
    cur.execute("SELECT Tweet FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) +" AND IsRetweet=0")
    d=cur.fetchall()
    c=0
    for item in d:
        if ("@" in item[0]) and (not ("RT:" in item[0])):
            c+=1
            t+=1
    l.append(c)
    cur.execute("SELECT Tweet FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) +" AND IsRetweet=0")
    d=cur.fetchall()
    c=0
    for item in d:
        if ("@" in item[0]) and (not ("RT:" in item[0])):
            c+=1
            t+=1
    l.append(c)
    print t
    print l




    

def countusers():
    t=0
    l=[]
    cur.execute("SELECT DISTINCT ScreenName FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    l.append(len(d))
    cur.execute("SELECT DISTINCT ScreenName FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    l.append(len(d))
    cur.execute("SELECT DISTINCT ScreenName FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    l.append(len(d))
    print l
    print sum(l)


def tweetsperuser(tablename):
    t=0
    l=[]
    l2=[]
    dic={}
    cur.execute("SELECT ScreenName FROM "+tablename+" WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    d=cur.fetchall()
    for item in d:
        l2.append(item[0])

    for item in l2:
        if not (item in dic.keys()):
            dic[item]=l2.count(item)

    lf=[]
    for item in dic.keys():
        lf.append(dic[item])

    return lf

        
def calcoverlapusers():
    cur.execute("SELECT DISTINCT ScreenName FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    ugw=cur.fetchall()
    cur.execute("SELECT DISTINCT ScreenName FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    ucc=cur.fetchall()
    cur.execute("SELECT DISTINCT ScreenName FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    uagw=cur.fetchall()

    ccgw=set(ucc).intersection( set(ugw) )
    print "Users Intersection between #climatechange and #globalwarming:"
    #print str(len(ccgw))+"/"+str(len(ugw)+len(ucc)-len(ccgw)) +", " + str(float(float(len(ccgw))/(len(ugw)+len(ucc)-len(ccgw)))*100) + "%"
    print str(len(ccgw))

    ccagw=set(ucc).intersection( set(uagw) )
    print "Users Intersection between #climatechange and #agw:"
    #print str(len(ccagw))+"/"+str(len(ucc)+len(uagw)-len(ccagw)) +", " + str(float(float(len(ccagw))/(len(ucc)+len(uagw)-len(ccagw)))*100) + "%"
    print str(len(ccagw))
    
    gwagw=set(ugw).intersection( set(uagw) )
    print "Users Intersection between #globalwarming and #agw:"
    #print str(len(gwagw))+"/"+str(len(ugw)+len(uagw)-len(gwagw)) +", " + str(float(float(len(gwagw))/(len(ugw)+len(uagw)-len(gwagw)))*100) + "%"
    print str(len(gwagw))
def calcoverlaptweets():
    cur.execute("SELECT DISTINCT Id FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    ugw=cur.fetchall()
    cur.execute("SELECT DISTINCT Id FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    ucc=cur.fetchall()
    cur.execute("SELECT DISTINCT Id FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    uagw=cur.fetchall()

    ccgw=set(ucc).intersection( set(ugw) )
    print "Tweets Intersection between #climatechange and #globalwarming:"
    #print str(len(ccgw))+"/"+str(len(ugw)+len(ucc)-len(ccgw)) +", " + str(float(float(len(ccgw))/(len(ugw)+len(ucc)-len(ccgw)))*100) + "%"
    print str(len(ccgw))
    
    ccagw=set(ucc).intersection( set(uagw) )
    print "Tweets Intersection between #climatechange and #agw:"
    #print str(len(ccagw))+"/"+str(len(ucc)+len(uagw)-len(ccagw)) +", " + str(float(float(len(ccagw))/(len(ucc)+len(uagw)-len(ccagw)))*100) + "%"
    print str(len(ccagw))

    gwagw=set(ugw).intersection( set(uagw) )
    print "Tweets Intersection between #globalwarming and #agw:"
    #print str(len(gwagw))+"/"+str(len(ugw)+len(uagw)-len(gwagw)) +", " + str(float(float(len(gwagw))/(len(ugw)+len(uagw)-len(gwagw)))*100) + "%"
    print str(len(gwagw))

def calcoverlapretweets():
    cur.execute("SELECT DISTINCT Id FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) + " AND IsRetweet=1")
    ugw=cur.fetchall()
    cur.execute("SELECT DISTINCT Id FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) + " AND IsRetweet=1")
    ucc=cur.fetchall()
    cur.execute("SELECT DISTINCT Id FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) + " AND IsRetweet=1")
    uagw=cur.fetchall()

    ccgw=set(ucc).intersection( set(ugw) )
    print "Retweets Intersection between #climatechange and #globalwarming:"
    #print str(len(ccgw))+"/"+str(len(ugw)+len(ucc)-len(ccgw)) +", " + str(float(float(len(ccgw))/(len(ugw)+len(ucc)-len(ccgw)))*100) + "%"
    print str(len(ccgw))
    
    ccagw=set(ucc).intersection( set(uagw) )
    print "Retweets Intersection between #climatechange and #agw:"
    #print str(len(ccagw))+"/"+str(len(ucc)+len(uagw)-len(ccagw)) +", " + str(float(float(len(ccagw))/(len(ucc)+len(uagw)-len(ccagw)))*100) + "%"
    print str(len(ccagw))

    gwagw=set(ugw).intersection( set(uagw) )
    print "Retweets Intersection between #globalwarming and #agw:"
    #print str(len(gwagw))+"/"+str(len(ugw)+len(uagw)-len(gwagw)) +", " + str(float(float(len(gwagw))/(len(ugw)+len(uagw)-len(gwagw)))*100) + "%"
    print str(len(gwagw))


def calcoverlapmentions():
    cur.execute("SELECT DISTINCT Id, Tweet FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) + " AND IsRetweet=0")
    ugwp=cur.fetchall()
    cur.execute("SELECT DISTINCT Id, Tweet FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) + " AND IsRetweet=0")
    uccp=cur.fetchall()
    cur.execute("SELECT DISTINCT Id, Tweet FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime) + " AND IsRetweet=0")
    uagwp=cur.fetchall()

    ugw=[]
    ucc=[]
    uagw=[]
    for item in ugwp:
        if ("@" in item[1]) and (not ("RT:" in item[1])):
            ugw.append(item[0])
    for item in uccp:
        if ("@" in item[1]) and (not ("RT:" in item[1])):
            ucc.append(item[0])
    for item in uagwp:
        if ("@" in item[1]) and (not ("RT:" in item[1])):
            uagw.append(item[0])


    ccgw=set(ucc).intersection( set(ugw) )
    print "Mentions Intersection between #climatechange and #globalwarming:"
    #print str(len(ccgw))+"/"+str(len(ugw)+len(ucc)-len(ccgw)) +", " + str(float(float(len(ccgw))/(len(ugw)+len(ucc)-len(ccgw)))*100) + "%"
    print str(len(ccgw))
    
    ccagw=set(ucc).intersection( set(uagw) )
    print "Mentions Intersection between #climatechange and #agw:"
    #print str(len(ccagw))+"/"+str(len(ucc)+len(uagw)-len(ccagw)) +", " + str(float(float(len(ccagw))/(len(ucc)+len(uagw)-len(ccagw)))*100) + "%"
    print str(len(ccagw))

    gwagw=set(ugw).intersection( set(uagw) )
    print "Mentions Intersection between #globalwarming and #agw:"
    #print str(len(gwagw))+"/"+str(len(ugw)+len(uagw)-len(gwagw)) +", " + str(float(float(len(gwagw))/(len(ugw)+len(uagw)-len(gwagw)))*100) + "%"
    print str(len(gwagw))


def calcgini3(l):
    l.sort()
    n=len(l)
    topsum=0
    bottomsum=n*sum(l)
    for i in range(len(l)):
        topsum+=(i+1)*l[i]
    topsum=topsum*2
    term2=float(n+1)/n
    
    G=(float(topsum)/bottomsum) - term2
    print G
    
if __name__ == "__main__":
    #countrecords()
    countusers()
    calcoverlapusers()    
    countrecords()
    calcoverlaptweets()
    countretweets()
    calcoverlapretweets()
    countmentions()
    calcoverlapmentions()
    #calcgini3(tweetsperuser("htclimatechange"))
    #calcgini3(tweetsperuser("htglobalwarming"))
    #calcgini3(tweetsperuser("htagw"))
