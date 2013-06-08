import sqlite3 as lite
import sys
from classtweetgetter import DBTweetGetter

mytweetgetter=DBTweetGetter(None, None)

con=lite.connect("tweetsdb.db")
cur=con.cursor()
ucon=lite.connect("userdb.db")
ucur=ucon.cursor()


tables=['htclimatechange','htclimate','htglobalwarming','ClimateChange','GlobalWarming']

names=[]
for item in tables:
    cur.execute("SELECT DISTINCT ScreenName FROM " + item)
    a=cur.fetchall()
    for item2 in a:
        names.append(item2[0])


already=[]
ucur.execute("SELECT ScreenName FROM usermap")
b=ucur.fetchall()
for item in b:
    already.append(item[0])

deleted=[]
i=0
l=len(names)
for name in names:
    i+=1
    if not (name in already):
        print str(i)+"/"+str(l)
        x=mytweetgetter.getIDfromUser(name)
        if x!= "FAIL":
            ucur.execute("INSERT INTO usermap VALUES('" +name+ "'," + x + ")" )
        else:
            deleted.append(name)
        already.append(name)


con.close()
ucon.commit()
ucon.close()
print deleted
