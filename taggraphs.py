import sys
tagfiles=["usertagstom.txt","usertagschris.txt","usertagsotherchris.txt","usertagssteve.txt","usertagsotheralastair.txt","usertagsalastair.txt","usertagsothertom.txt","usertagslastchris.txt","usertagslastalastair.txt","usertagslasttom.txt","usertagsetctestetc.txt"]

#backup graphs first

def findmajority(l):
    #Actually don't use this, instead rely on unanimity
    #convert to set
    sl=set(l)
    max=0
    cl=None
    for item in set(l):
        if l.count(item)>max:
            max=l.count(item)
            cl=item
    return cl

def checkuna(l):
    if l.count(l[0])==len(l):
        return l[0]
    else:
        return "?"


#Have a activist ,g skeptic ,n neutral,u other then ? disputed, x untagged
ud={}
for fi in tagfiles:
    f=open(fi,"r")
    for line in f:
        l=line.split(",")
        if l[0] in ud.keys():
            ud[l[0]].append(l[1][0])
        else:
            ud[l[0]]=[l[1][0]]

fd={}
#could use a map here
for item in ud.keys():
    fd[item]=checkuna(ud[item])

#print fd
# c=0
# for item in fd.keys():
#     if fd[item]=="u":
#         c+=1
# print str(c) + "/" + str(len(fd.keys()))

# sys.exit()

graphs=["fixgwconvew2pc4.gml"]
#,"newfriendfollowerhtccwgt35.gml","newfriendfollowerhtgwgt12.gml"]
#graphs=["newrthtccew8comp4.gml"]
#Somehow write to work with graphs already with tags, and without

def fixnegative(x):
    global s
    if x==-1:
        return len(s)
    else:
        return x


for graph in graphs:
    #find label
    #try to find HC2 between next label or end
    #Either replace HC2 or add in HC2 with new tags
    f=open(graph, "r")
    s=f.read()
    f.close()
    pos=0
    n=[]

    while True:
        try:
            p1=s.index("label",pos)
        except:
            break
        p2=s.index('"',p1+7)
        name=s[p1+7:p2]
        #print name
        u=s.find("label",p1+7)
        u=fixnegative(u)
        if "HC2" in s[p1:u]:
            #change HC2
            h=s.index("HC2",p1)
            try:
                s=s[0:h+4]+'"'+fd[name]+'"'+s[h+7:]
            except:
                #n.append(name)
                print name
            #s=s[0:h+4]+'"T"'+s[h+7:]
        else:
            #add HC2
            s=s[0:p2+1]+'\n    HC2 "'+fd[name]+'"'+s[p2+1:]
            pass

        pos=p1+7
        #print n
    #sys.exit()
    f=open("t"+graph, "w")
    f.write(s)
    f.close()
        
