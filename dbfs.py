#Do directed breadth first search to complete path-length/path matrix
import networkx as nx
import numpy as np
import operator
import sys

class BFSstep(object):
    ''' Class for directed Breadth First Search steps - gets successors for current node, and stores paths to these nodes'''
    def __init__(self,node,curpath):
        self.node=node
        self.curpath=curpath
        self.changedself=False
    def step(self):
        self.changedself=False
        name=userdict[self.node]
        arraydict[gname][name]=(len(self.curpath), self.curpath)
        l=g.successors(self.node)
        for item in l:
            if item in unseennodes:
                if self.changedself==False:
                    self.node=item
                    self.curpath+=[item]
                    bfslist.append(self)
                    self.changedself=True
                else:
                    newpath=list(self.curpath+[item])
                    bfslist.append(BFSstep(item, newpath))
                unseennodes.remove(item)

skeptics=[]
activists=[]
userdict={}
def fixnegative(x):
    global s
    if x==-1:
        return len(s)
    else:
        return x

fs=["fixgwconvgc.gml"]
#fs=["convagwgc.gml","convgwgc.gml","htccconvgc.gml"]
#gmlf="finalffagw.gml"
#Read GML

#parse gml file to remove unnecessary lines which break networkx
for gmlf in fs:
    f=open(gmlf,"r")
    s=f.read()
    f.close()

    f=open(gmlf,"r")
    inbra=False
    z=""
    for line in f:
        if "graphics" in line:
            inbra=True
        elif ("]" in line) and inbra==True:
            inbra=False
        elif inbra==True or ("Strongly-ConnectedID" in line):
            pass
        else:
            z+=line

    f.close()
    f2=open("pl"+gmlf,"w")
    f2.write(z)
    f2.close()

    g=nx.read_gml("pl"+gmlf)
    pos=0

    while True:
        try:
            p1=s.index("label",pos)
        except:
            break
        p2=s.index('"',p1+7)
        name=s[p1+7:p2]
        i1=s.rfind('id ',pos,p1)
        i2=s.index('\n',i1)
        id1=s[i1+3:i2]
        #print name
        u=s.find("label",p1+7)
        u=fixnegative(u)
        #change HC2
        h=s.index("HC2",p1)
        c=s[h+5]
        pos=p1+7
        #print name, c, id1
        userdict[int(id1)]=name
        if c=="a":
            activists.append(name)
        elif c=="g":
            skeptics.append(name)



            #print userdict
            #sys.exit()
    bfslist=[]
    nodelist=g.nodes()
    #Select only activists
    # i=0
    # while i<len(nodelist):
    #     if not (userdict[nodelist[i]] in activists):
    #         g.remove_node(nodelist[i])
    #         nodelist.pop(i)

    #     else:
    #         i+=1

    sdegreedist={}
    pdegreedist={}
    tdegreedist={}

    for node in nodelist:
        s=g.successors(node)
        p=g.predecessors(node)

        try:
            sdegreedist[len(s)]+=1
        except:
            sdegreedist[len(s)]=1
        try:
            pdegreedist[len(p)]+=1
        except:
            pdegreedist[len(p)]=1
        try:
            tdegreedist[(len(s)+len(p))]+=1
        except:
            tdegreedist[(len(s)+len(p))]=1
    print gmlf
    print "Degree distributions"
    print "Follower degree distribution"
    print sdegreedist
    print "Friend degree distribution"
    print pdegreedist
    print "Total degree distribution"
    print tdegreedist

    # array dict= user: all users reachable by user
    # Note we are only including reachable users
    arraydict={}
    for item in nodelist:
        arraydict[userdict[item]]={}

    rlist=[]
    z=0
    for gnode in nodelist:
        z+=1
        #print str(z) + "/" + str(len(nodelist))
        unseennodes=list(nodelist)
        gname=userdict[gnode]
        bfslist.append(BFSstep(gnode,[gnode]))
        while (len(bfslist)!=0):
            (bfslist.pop(0)).step()
            #print(len(bfslist))
        rlist.append(len(unseennodes))
        #print rlist
    aalist=[]
    aslist=[]
    salist=[]
    sslist=[]
    globallist=[]
    for user in arraydict.keys():
        if user in activists:
            for item in arraydict[user].keys():
                globallist+=[arraydict[user][item][0]]
                if item in activists:
                    aalist+=[arraydict[user][item][0]]
                elif item in skeptics:
                    aslist+=[arraydict[user][item][0]]
        elif user in skeptics:
            for item in arraydict[user].keys():
                globallist+=[arraydict[user][item][0]]
                if item in activists:
                    salist+=[arraydict[user][item][0]]
                elif item in skeptics:
                    sslist+=[arraydict[user][item][0]]
        else:
            for item in arraydict[user].keys():
                globallist+=[arraydict[user][item][0]]


    print "Number of skeptics: " + str(len(skeptics)) + ", number of activists: " + str(len(activists)) + ", Total number of users: " + str(len(userdict.keys()))
    print "Path lengths"
    print "Globally:"
    print "Mean: " + str(np.mean(globallist)) +", Standard deviation: " + str(np.std(globallist)) + ", Number of paths: " + str(len(globallist)) + ", Standard error: " +str(np.std(globallist)/np.sqrt(len(globallist)))
    print "Activist-Activist:"
    print "Mean: " + str(np.mean(aalist)) +", Standard deviation: " + str(np.std(aalist)) + ", Number of paths: " + str(len(aalist)) + ", Standard error: " +str(np.std(aalist)/np.sqrt(len(aalist)))
    print "Activist-Skeptic:"
    print "Mean: " + str(np.mean(aslist)) +", Standard deviation: " + str(np.std(aslist))+ ", Number of paths: " + str(len(aslist)) + ", Standard error: " +str(np.std(aslist)/np.sqrt(len(aslist)))
    print "Skeptic-Activist:"
    print "Mean: " + str(np.mean(salist)) +", Standard deviation: " + str(np.std(salist))+ ", Number of paths: " + str(len(salist)) + ", Standard error: " +str(np.std(salist)/np.sqrt(len(salist)))
    print "Skeptic-Skeptic:"
    print "Mean: " + str(np.mean(sslist)) +", Standard deviation: " + str(np.std(sslist))+ ", Number of paths: " + str(len(sslist)) + ", Standard error: " +str(np.std(sslist)/np.sqrt(len(sslist)))

    #Calculate fraction of shortest paths in which each user is present, rank by betweenness
    #print str(len(arraydict.keys()))
    #print str(len(arraydict["moronwatch"].keys()))
    nlist=[]



    #For each user go through entire array counting how many paths user is present in, for every possible path
    
    betweennessdaa={}
    betweennessdas={}
    betweennessdsa={}
    betweennessdss={}
    q=0
    llng=len(nodelist)
    bign=[0,0,0,0]
    for user in nodelist:
        q+=1
        #print str(q) + "/" + str(llng)
        b=[0,0,0,0]
        n=[0,0,0,0]
        #aa,as,sa,ss
        for i in arraydict.keys():
            for j in arraydict[i].keys():

                if (i in activists):
                    if (j in activists):
                        n[0]+=1
                    elif (j in skeptics):
                        n[1]+=1
                elif (i in skeptics):
                    if (j in activists):
                        n[2]+=1
                    elif (j in skeptics):
                        n[3]+=1

                if user in arraydict[i][j][1]:
                    if (i in activists):
                        if (j in activists):
                            b[0]+=1
                        elif (j in skeptics):
                            b[1]+=1
                    elif (i in skeptics):
                        if (j in activists):
                            b[2]+=1
                        elif (j in skeptics):
                            b[3]+=1
                # ll=arraydict[i][j][1]
                # for l in ll:
                #     n+=1
                #     if user in l:
                #         b+=1
        print n
        for z in range(4):
            try: 
                b[z]=float(b[z])/float(n[z])
            except:
                pass
        betweennessdaa[userdict[user]]=b[0]
        betweennessdas[userdict[user]]=b[1]
        betweennessdsa[userdict[user]]=b[2]
        betweennessdss[userdict[user]]=b[3]

    #print nlist

    print "Betweenness"
    print "Activist-Activist"
    sorteddict = sorted(betweennessdaa.iteritems(), key=operator.itemgetter(1))
    sorteddict.reverse()
    print (sorteddict[0:9])
    print "Activist-Skeptic"
    sorteddict = sorted(betweennessdas.iteritems(), key=operator.itemgetter(1))
    sorteddict.reverse()
    print (sorteddict[0:9])
    print "Skeptic-Activist"
    sorteddict = sorted(betweennessdsa.iteritems(), key=operator.itemgetter(1))
    sorteddict.reverse()
    print (sorteddict[0:9])
    print "Skeptic-Skeptic"
    sorteddict = sorted(betweennessdss.iteritems(), key=operator.itemgetter(1))
    sorteddict.reverse()
    print (sorteddict[0:9])

