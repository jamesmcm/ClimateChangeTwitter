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
    print "Intersection between #climatechange and #globalwarming:"
    print str(len(ccgw))+"/"+str(len(ugw)+len(ucc)-len(ccgw)) +", " + str(float(float(len(ccgw))/(len(ugw)+len(ucc)-len(ccgw)))*100) + "%"

    ccagw=set(ucc).intersection( set(uagw) )
    print "Intersection between #climatechange and #agw:"
    print str(len(ccagw))+"/"+str(len(ucc)+len(uagw)-len(ccagw)) +", " + str(float(float(len(ccagw))/(len(ucc)+len(uagw)-len(ccagw)))*100) + "%"

    gwagw=set(ugw).intersection( set(uagw) )
    print "Intersection between #globalwarming and #agw:"
    print str(len(gwagw))+"/"+str(len(ugw)+len(uagw)-len(gwagw)) +", " + str(float(float(len(gwagw))/(len(ugw)+len(uagw)-len(gwagw)))*100) + "%"

def calcoverlaptweets():
    cur.execute("SELECT DISTINCT Id FROM htglobalwarming WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    ugw=cur.fetchall()
    cur.execute("SELECT DISTINCT Id FROM htclimatechange WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    ucc=cur.fetchall()
    cur.execute("SELECT DISTINCT Id FROM htagw WHERE ConvertedTime > " + str(ct) +" AND ConvertedTime < " + str(maxtime))
    uagw=cur.fetchall()

    ccgw=set(ucc).intersection( set(ugw) )
    print "Intersection between #climatechange and #globalwarming:"
    print str(len(ccgw))+"/"+str(len(ugw)+len(ucc)-len(ccgw)) +", " + str(float(float(len(ccgw))/(len(ugw)+len(ucc)-len(ccgw)))*100) + "%"

    ccagw=set(ucc).intersection( set(uagw) )
    print "Intersection between #climatechange and #agw:"
    print str(len(ccagw))+"/"+str(len(ucc)+len(uagw)-len(ccagw)) +", " + str(float(float(len(ccagw))/(len(ucc)+len(uagw)-len(ccagw)))*100) + "%"

    gwagw=set(ugw).intersection( set(uagw) )
    print "Intersection between #globalwarming and #agw:"
    print str(len(gwagw))+"/"+str(len(ugw)+len(uagw)-len(gwagw)) +", " + str(float(float(len(gwagw))/(len(ugw)+len(uagw)-len(gwagw)))*100) + "%"



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
    #calcoverlaptweets()
    countrecords()
    countretweets()
    countmentions()
    #countusers()
    #calcgini3(tweetsperuser("htclimatechange"))
    #calcgini3(tweetsperuser("htglobalwarming"))
    #calcgini3(tweetsperuser("htagw"))
