import pickle

filenames=["twitterdata_query=Climate_Change_time=15_12_2310_lastid=279335849756344319.pkl","twitterdata_query=#climatechange_time=15_12_2324_lastid=279330404547309567.pkl","twitterdata_query=#globalwarming_time=15_12_2332_lastid=279347060677951488.pkl","twitterdata_query=Global_Warming_time=15_12_2351_lastid=279350620694134784.pkl","twitterdata_query=#climate_time=15_12_2358_lastid=279345094207873023.pkl"]
#filename="twitterdata_query=#climatechange_time=21_11_1741_lastid=269835693721792511.pkl"
for filename in filenames:
    picklefile=open(filename, "r")
    twitterdict=pickle.load(picklefile)
    picklefile.close()
    for item in twitterdict.keys():
        i=0
        while i < len(twitterdict[item]["hashtags"]):
            if "http://" in twitterdict[item]["hashtags"][i]:
                twitterdict[item]["urls"].append(twitterdict[item]["hashtags"][i])
                twitterdict[item]["hashtags"].pop(i)
            else:
                i+=1

    picklefile=open(filename, "w")
    pickle.dump(twitterdict,picklefile)
    picklefile.close()
