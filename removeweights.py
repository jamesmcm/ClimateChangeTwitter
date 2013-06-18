graphs=["tnewrthtccew8comp4.gml","tnewrthtagwew4comp4.gml","tnewrtgwew4comp4.gml","thtgwconvew4pc6.gml","thtccconvew4pc6.gml","thtagwconvew2pc6.gml"]

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
