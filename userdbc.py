import pickle
import sqlite3 as lite



f=open("usersdict_twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl","r")
d=pickle.load(f)
f.close()

con = lite.connect('userdb.db')

cur = con.cursor()

#cur.execute("CREATE TABLE followers(ScreenName TEXT, FollowerId INT)")
#cur.execute("CREATE TABLE friends(ScreenName TEXT, FriendId INT)")

for item in d.keys():
    for follower in d[item]["followers_list"]:
        cur.execute("INSERT INTO followers VALUES('" + item + "'," + str(follower) + ")" )
    for friend in d[item]["friends_list"]:
        cur.execute("INSERT INTO friends VALUES('" + item + "'," + str(friend) + ")" )


con.commit()
con.close()
