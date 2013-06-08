import sqlite3 as lite
from random import shuffle
from classtweetgetter import DBTweetGetter
f=open("temp.txt","r")
l=f.read()
l=l.split(",")
userlist=l
#userlist =["climatehawk1", "moronwatch"]
mytweetgetter=DBTweetGetter(None, None)
validchars=['A','G','L','a','g','l']
con=lite.connect("tweetsdb.db")
cur=con.cursor()
logfile=open("usertags.txt","a")
for user in userlist:
    #Get blurb
    #get sample of tweets from main databases
    #Webpage? Check user info
    #Display data, log result, make sure works okay
    print ("Username: " + str(user))
    tweets=[]
    description=mytweetgetter.getUserDescription(user)
    cur.execute("SELECT DISTINCT Tweet FROM htclimatechange WHERE ScreenName='"+str(user)+"' COLLATE NOCASE")
    temp=cur.fetchall()
    for item in temp:
        tweets.append(item)
    cur.execute("SELECT DISTINCT Tweet FROM htglobalwarming WHERE ScreenName='"+str(user)+"' COLLATE NOCASE")
    temp=cur.fetchall()
    for item in temp:
        tweets.append(item)
    cur.execute("SELECT DISTINCT Tweet FROM htagw WHERE ScreenName='"+str(user)+"' COLLATE NOCASE")
    temp=cur.fetchall()
    for item in temp:
        tweets.append(item)
    shuffle(tweets)
    if len(tweets)<11:
        lim=len(tweets)
    else:
        lim=10
    print("Description:")
    print(description)
    print("Recent Tweets:")
    for i in range(lim):
        print(tweets[i])

    # Get user input
    print("Is " + user +" an activist (A), skeptic (G), or unknown (L)?")
    stry=True
    while stry==True:
        minput=raw_input()
        if (minput in validchars):
            stry=False
        else:
            print("Please enter a valid selection: activist (A), skeptic (G), or unknown (L):")
    logfile.write(user+","+minput+"\n")
    logfile.flush()
    
    print "------------"
    
#Need to work out how to insert results in to clustering
