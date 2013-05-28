#Parser to colour tags
#Parse usertag file, make dictionary
#Go through GML file, put all users in clusters - either activist, skeptic or not tagged or neither
#Currently: G: Skeptic, A: Activist, L:Other, X: Untagged
import sys

d={}
f=open("usertags.txt","r")
for line in f:
    l=line.replace("\n","")
    l=l.split(",")
    d[l[0].lower()]=l[1].lower()

f.close()
#print d
#TODO Add code for loading multiple dictionaries, dealing with differences, etc.
#Successfully loaded dictionary

#Parse GML
f=open("naivertnewhtclimatechange.gml","r")
gml=f.read()
f.close()

print "GML loaded successfully"
lind=gml.find("label")
while lind != -1:
    sn=gml.index('"', lind)+1
    fn=gml.index('"', sn+1)
    name=gml[sn:fn]
    try:
        val=d[name.lower()]
    except:
        val='x'
    gml=gml[:fn+2]+'    HC2 "' + val + '"\n'+gml[fn+2:]
    lind=gml.find("label",fn)

f=open("taggednaivertnewhtclimatechange.gml", "w")
f.write(gml)
f.close()
