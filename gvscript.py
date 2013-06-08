f=open("fullrt.gv", "r")
t=f.read()
f.close()

#nodes 2 lines
#edges 1 line
#get list of times only node times matter
#search for "\ttime"
k= t.split(";")

for i in range( len(k)):
    k[i]=k[i].split("\n")

for i in range(len(k)):
    for j in range(len(k[i])):
        k[i][j]=k[i][j].split("\t")


times=[]
for item in k:
    try:
        times.append(int(item[2][2][6:-1]))
    except:
        pass
# print str(max(times) - min(times))
times.sort()
namedict={}
timedict={}

for item in k:
    try:
        #print str(item[0][1])
        namedict[str(item[0][1])]=item[0][2][7:-1]
        #print str(item[0][3][7:-1])
    except:
        try:
            #print str(item[1][1])
            if item[1][2][2:6]=="name":
                namedict[str(item[1][1])]=item[1][2][7:-1]
                #print str(item[1][3][7:-1])
        except:
            pass

timedict[int(k[0][1][2][5:-1])]=[k[0][0][2][7:-1]]
for item in k:
    try:
        if timedict.has_key(int(item[2][2][5:-1]))==True:
            timedict[int(item[2][2][5:-1])].append(item[1][2][7:-1])
        else:
            timedict[int(item[2][2][5:-1])]=[item[1][2][7:-1]]
    except Exception as detail:
        #print detail
        pass

k[0][0][1]=namedict[str(k[0][0][1])]
for z in range(len(k)):
    try:
        if len(k[z][1][1].split(" "))>1:
            l=k[z][1][1].split(" ")
            l[0]=namedict[str(l[0])]
            l[2]=namedict[str(l[2])]
            k[z][1][1]='"'+l[0]+'" '+l[1]+' "'+l[2]+'"'
        else:
            k[z][1][1]='"'+namedict[str(k[z][1][1])]+'"'
    except:
        pass



times=timedict.keys()
times.sort()
ctime={}
s='digraph asde91 {\n\tranksep=.75; size = "7.5,7.5";\n\t{\n\t\tnode [shape=plaintext, fontsize=16];\n\t\t'
mintime=times[0]
for z in range(len(times)):
    times[z]=times[z]-mintime
for z in range(len(times)):
    t=times[z]
    d=t/(24*60*60)
    t=t%(24*60*60)
    h=t/(60*60)
    t=t%(60*60)
    m=t/(60)
    s1=t%60
    s+='"'+str(d)+'d'+str(h)+'h'+str(m)+'m'+str(s1)+'s" -> '
    ctime[times[z]]='"'+str(d)+'d'+str(h)+'h'+str(m)+'m'+str(s1)+'s"'
s=s[:-4]
s+=';\n}\nnode [shape=box];\n'
for z in range(len(times)):
    d='{ rank = same; '+ctime[times[z]]+'; '
    for item in timedict[times[z]+mintime]:
        d+='"'+item+'"; '
    d+='}\n'
    s+=d


q=""
for item in k:
    for item2 in item:
        for item3 in item2:
            q+=str(item3)+"\t"
        q=q[:-1]
        q+="\n"
    q=q[:-1]
    q+=";"

output= (s+q)[:-1]+"}"
output=output.replace('""', '"')
print output
# curmin=100000000
# for z in range(len(times)-1):
#     if (times[z+1]-times[z])<curmin and (times[z+1]-times[z])!=0:
#         curmin=times[z+1]-times[z]
# print curmin

#just use time ids for ranks, ignore scale
