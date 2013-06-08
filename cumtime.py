import sqlite3 as lite
import time
import datetime

def convertTime(timestring):
        #Fri Nov 16 22:31:39 +0000 2012
        lts=timestring.split(" ")
        tt=lts[3].split(":")
        monthdict={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        dt=datetime.datetime(int(lts[5]), int(monthdict[lts[1]]), int(lts[2]),int(tt[0]),int(tt[1]),int(tt[2]))
        return int(time.mktime(dt.timetuple()))

con=lite.connect("tweetsdb.db")
cur=con.cursor()

#for #agw from Sunday 20Jan -> Thurs 07Feb
#tstart="Sun Jan 20 00:00:00 +0000 2013"
#tend="Thurs Feb 07 00:00:00 +0000 2013"

#htclimatechange
#tstart='Sat Dec 01 00:00:00 +0000 2012'
tend='Wed May 29 00:00:00 +0000 2013'

#ct=convertTime(tstart)
ct=1358090418
ctm=1358090418

def cumusers(tablename):
	global ct
	global ctm	
	ctend=convertTime(tend)
	usernums=[]
	times=[]
	while ct<ctend:
	    cur.execute("SELECT DISTINCT ScreenName FROM "+tablename+" WHERE ConvertedTime < " + str(ct) + " AND ConvertedTime > " + str(ctm))
	    d=cur.fetchall()
	    usernums.append(len(d))
	    times.append(ct)
	    ct+=86400

	print len(times)
	f=open("usernumdata"+tablename+"3.txt","w")
	for i in range(len(usernums)):
	    f.write(str(times[i]) + "\t"+ str(usernums[i])+"\n")
	f.close()

def cumtweets(tablename):
	global ct
	global ctm
	ctend=convertTime(tend)
	usernums=[]
	times=[]
	while ct<ctend:
	    cur.execute("SELECT DISTINCT Id FROM "+tablename+" WHERE ConvertedTime < " + str(ct) + " AND ConvertedTime > " + str(ctm))
	    d=cur.fetchall()
	    usernums.append(len(d))
	    times.append(ct)
	    ct+=86400

	print len(times)
	f=open("tweetnumdata"+tablename+"3.txt","w")
	for i in range(len(usernums)):
	    f.write(str(times[i]) + "\t"+ str(usernums[i])+"\n")
	f.close()

def activity(tablename):
	global ct
	global ctm
	
	ct+=86400
	ctend=convertTime(tend)
	usernums=[]
	times=[]
	while ct<ctend:
	    cur.execute("SELECT DISTINCT Id FROM "+tablename+" WHERE ConvertedTime < " + str(ct) + " AND ConvertedTime > " + str(ctm))
	    d=cur.fetchall()
	    usernums.append(len(d))
	    times.append(ct)
	    ct+=86400
	    ctm+=86400

	print len(times)
	f=open("acttweetdata"+tablename+"3.txt","w")
	for i in range(len(usernums)):
	    f.write(str(times[i]) + "\t"+ str(usernums[i])+"\n")
	f.close()

#To get cumulative tweet number
# cur.execute("SELECT ConvertedTime FROM htclimatechange")
# da=cur.fetchall()
# print da
# con.close()

# l=[]
# for item in da:
#     l.append(int(item[0]))

# #make dictionary
# d={}
# for item in l:
#     if item in d:
#         d[item]+=1
#     else:
#         d[item]=1


# f=open("cumtimedata.dat", "w")



# for key in sorted(d.iterkeys()):
#     f.write("%i\t%i\n" % (key, d[key]))
    
# f.close()


# dat1 <- read.table("cumtimedata.dat")
# cdat1 <- cumsum(dat1$V2)
# plot(dat1$V1, cdat1)
cumtweets("htclimatechange")
