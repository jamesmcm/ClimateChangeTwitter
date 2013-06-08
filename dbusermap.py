import sqlite3 as lite
import sys
from classtweetreader import TweetReader
myreader=TweetReader(filename="twitterdata_query=Climate_Change_time=16_01_1707_lastid=290237605872816128.pkl")
d=myreader.twitterdict

ucon = lite.connect('userdb.db')
ucur = ucon.cursor()

# ucur.execute("CREATE TABLE usermap(ScreenName TEXT, UserId INT)")
screened=[]
ucur.execute("SELECT ScreenName FROM usermap")
a=ucur.fetchall()
for item in a:
    screened.append(item[0])




for item in d.keys():
    if not (d[item]["screen_name"] in screened):
        ucur.execute("INSERT INTO usermap VALUES('" + d[item]["screen_name"]  + "'," + d[item]["user_id_str"] + ")" )
        screened.append(d[item]["screen_name"])
# tcon=lite.connect('tweetsdb.db')
# tcur=tcon.cursor()
# tcur.execute("SELECT ScreenName FROM htclimatechange")
# d=tcur.fetchall()



# for item in d:
#     if not (item[0] in screened):
        
#         screened.append(item[0])

ucon.commit()
ucon.close()
