graphs=["gwconvew2pc4fixlabels.gml"]

for f in graphs:
    fi=open(f,"r")
    s=""
    for line in fi:
        if not "value" in line:
            s+=line
    fi.close()
    f2=open("nw"+f,"w")
    f2.write(s)
    f2.close()
