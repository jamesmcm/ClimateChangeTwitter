import sqlite3 as lite
import time
import datetime

con=lite.connect("tweetsdb.db")
cur=con.cursor()
ct=1358090418

def countrecords():
    t=0
    cur.execute("SELECT COUNT(*) FROM htglobalwarming WHERE ConvertedTime > " + str(ct))
    d=cur.fetchall()
    t+=d[0][0]
    cur.execute("SELECT COUNT(*) FROM htclimatechange WHERE ConvertedTime > " + str(ct))
    d=cur.fetchall()
    t+=d[0][0]
    cur.execute("SELECT COUNT(*) FROM htagw WHERE ConvertedTime > " + str(ct))
    d=cur.fetchall()
    t+=d[0][0]
    print t


def calcoverlap():
    cur.execute("SELECT DISTINCT ScreenName FROM htglobalwarming WHERE ConvertedTime > " + str(ct))
    ugw=cur.fetchall()
    cur.execute("SELECT DISTINCT ScreenName FROM htclimatechange WHERE ConvertedTime > " + str(ct))
    ucc=cur.fetchall()
    cur.execute("SELECT DISTINCT ScreenName FROM htagw WHERE ConvertedTime > " + str(ct))
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

    
if __name__ == "__main__":
    #countrecords()
    calcoverlap()
