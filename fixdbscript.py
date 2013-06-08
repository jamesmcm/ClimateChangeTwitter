import sqlite3 as lite
import sys
import string

valid_characters = string.ascii_letters
valid_characters += string.digits
valid_characters += '_'


con = lite.connect("tweetsdb.db")
cur=con.cursor()

tablename="GlobalWarming"

cur.execute("SELECT Id, Tweet FROM " + tablename + " WHERE IsRetweet=1 AND RetweetSource=''")
l= cur.fetchall()

for item in l:
    text=item[1]
    if text[0:2] == "RT":
        isretweet="1"
        s=text
        try:
            atindex=s.index("@")
            breakif=False
        except:
            breakif=True

        if breakif==False:
            keepgoing=True
            i=1
            while keepgoing==True:
                try:
                    if not (s[atindex+i] in valid_characters):
                        keepgoing=False
                        endindex=i
                    else:
                        i+=1
                except:
                    keepgoing=False
                    endindex=i
            source=s[atindex+1:atindex+endindex]
            tweet=s[atindex+endindex+1:]
            tweet=tweet.replace("'","''")
            #print "UPDATE htclimatechange SET RetweetSource='" + source +"' WHERE Id="+str(item[0])
            #print "UPDATE htclimatechange SET RetweetTweet='" + tweet +"' WHERE Id="+str(item[0])
            cur.execute("UPDATE " + tablename + " SET RetweetSource='" + source +"' WHERE Id="+str(item[0]))
            cur.execute("UPDATE " + tablename + " SET RetweetTweet='" + tweet +"' WHERE Id="+str(item[0]))


con.commit()
con.close()

            
# UPDATE htclimatechange SET RetweetSource='Merlyn43' WHERE Id=291937292879294464;
# UPDATE htclimatechange SET RetweetTweet=' \"National Legislation Key to Combating Climate Change\" - http://t.co/vzKl3ipA - shared from @TaptuGreen #climatechange' WHERE Id=291937292879294464;
