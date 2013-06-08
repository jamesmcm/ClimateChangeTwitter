import sqlite3 as lite

def intersect(a, b):
     return list(set(a) & set(b))


con = lite.connect("tweetsdb.db")
cur=con.cursor()
mintime=1358090418
cur.execute("SELECT DISTINCT ScreenName FROM htagw WHERE ConvertedTime>"+str(mintime) + " AND IsRetweet=0")
cagw=cur.fetchall()
lagw=[]
for item in cagw:
    lagw.append(item[0])

cur.execute("SELECT DISTINCT ScreenName FROM htclimatechange WHERE ConvertedTime>"+str(mintime) + " AND IsRetweet=0")
chtcc=cur.fetchall()
lhtcc=[]
for item in chtcc:
    lhtcc.append(item[0])


cur.execute("SELECT DISTINCT ScreenName FROM htglobalwarming WHERE ConvertedTime>"+str(mintime) + " AND IsRetweet=0")
chtgw=cur.fetchall()
lhtgw=[]
for item in chtgw:
    lhtgw.append(item[0])

iagwhtcc=intersect(lagw,lhtcc)
print "Intersecting: " + str(len(iagwhtcc)) +" from " + str(len(lagw)) + " users in #agw, and " + str(len(lhtcc)) + " users in #climatechange"


iagwhtgw=intersect(lagw,lhtgw)
print "Intersecting: " + str(len(iagwhtgw)) +" from " + str(len(lagw)) + " users in #agw, and " + str(len(lhtgw)) + " users in #globalwarming"

ihtcchtgw=intersect(lhtcc,lhtgw)
print "Intersecting: " + str(len(ihtcchtgw)) +" from " + str(len(lhtcc)) + " users in #climatechange, and " + str(len(lhtgw)) + " users in #globalwarming"
