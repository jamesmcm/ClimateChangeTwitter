import sqlite3 as lite
from random import shuffle
import sys
# import datetime
print "Welcome to the manual user tagging of Twitter users."
print "Please tag the users as either:\n* Climate activists (A):  Those who believe in man-made climate change.\n* Skeptics (G): Those who do not believe in man-made climate change.\n* Neutral (N): If they appear neutral.\n* Unknown (U): If their tweets appear irrelevant."
print "You can quit and resume this process by typing 'quit' and then restarting the program, using the same name."
print "Please ignore characters like \\uXXX - these are just unicode characters which have been removed. If the tweets is unreadable then classify the user as Unknown."
print("Please enter your name:")
name=raw_input().lower()
name=name.replace(".","")
name=name.replace(",","")
name=name.replace(" ","")
name=name.replace("'","")
name=name.replace("@","")
name=name.replace("_","")
name=name.replace("-","")
# now = datetime.datetime.now()
# timestr=now.strftime("%d_%m_%H%M")
checkedusers=[]

nondesc=["", " ", "\n", "FAIL", "AIL", None]


userlist=["healthebay","marcherlord1","juicexlx","sharpestjim","profofphysics","john_symond","johnwboyko","isf_activist","prophetfella","valentinasos","jenninocsg","eco_mellon","iioannoulbs","checkoutspy","toryaardvark","greenmanlife","peter_ho","al_perri","bukumbooee","ddimick","jane1776","fingersflying","quantum2050","myworld2015","freepublictrans","robinhood1776","theophany1","cave_dweller31","iteration23","agw_is_a_hoax","bcfoodsecurity","thrivingplanet","timeclockman","benwinslow","iowenau","hepworks","1111_castle","heartlandinst","prometheus2054","nonsumdignus","docrichard","wulalowe","otiose94","amadeus8888","seahorse555","thestevenoracle","dustt","melissablancha6","fernandezeugene","cristiamrr","brevissi","kingscollegelib","storyroute","andybarton10","justturnright","stonepaperprose","presstitution","wordsofpower","bberwyn","amsecproject","mikeseager","arhobley","fathertheo","ronpaulnot4me","greenmotorgroup","blizzybe","bradleyjdibble","capandtrade","soshann","russellcavanagh","peopleandplanet","archweek","ddagan","coffeewarblers","carlos_s01","pdjmoo","progressiveport","smithnn8","chelseafanindo","anand_sivaram","seetac7","skyblue204","climatechange_1","darthvectivus","thetrendisblue","climatehotnews","quantumfires","ausaction","ormiga","implowshun","deepgreendesign","paulhbeckwith","havenr64","evolvingcaveman","gdthomp01","empirical_bayes","johnkeily1","nspugh","carbontaxscam","enviroedgenews","gogreenmotors","bulmkt","unshackleus","gillgarmesh","focusonprogress","greenhome2011","jackthelad1947","justintempler","therealnews365","lynestel","sailors_warning","infocyde","onahunttoday","mtl4u2","greenistweet","simongah","karlos1705","benwest","ruisaldanha","avjoe_realdeal","kernos501","preciseblogs","allanmargolin","higgsboson4","iamgreenbean","stephenrockf","openermedia","climaloop","marcysummer","warming_global","nrdc","bentler","wizquizman","julia__reid","junkscience","observer2isback","asiseeitnow","getglobe","safeclimatecamp","lumahaimike","lubedupnoob","solleshunter","nandauganda","ecowatch","climateresolve","ecoclimatesolut","kings_cambridge","windfallcentre","decisionlab","tiredpappy","grahamdlovell","javawinters","usgcrp","merlyn43","aladdintweets","love2unique","climatehawk1","suzlette333","zelo_street","old_norm","agwargentina","mlhagood","global__warming","redostoneage","askgerbil","mothincarnate","vk3bbr","all_a_twitt_r","rebootingfuture","pitbull_dale305","oparasitesingle","weshopper","maggie_pdx","strategikas","carlsiegrist","whotnaught","jonathan_drake","ecomanleader","johnzangas","opentoinfo","bjork55","collinmaessen","annemobile","occupy_oklahoma","sydnets","preppersnews1","lucalombroso","y_10k","cechr_uod","csrwire","brains3","dawn9476","boldrepublic","anthonybritneff","sustainablewits","snafu_au","empathynow","50yearforecast","escalatorover","mamacorin","tkjohndaniels","realistic_view","laurieload","waxmanclimate","charles_consult","wisco","anaelisafoto","stjarnafranfall","dcarli","mikedsomerville","hschwende","qldaah","respect65","gerry6868","perceiver1219","zoerey","_leshawn","mcwbr","mfearby","snvredd","ayeshavit","polluterwatch","karsenis","thepoliticalhat","greatbooks2read","billieraven","2dialogue","jeffreylowes","edwiebe","nartured","sensanders","noconsensus","newstruthliz","tadlette","pvincell","aloha_analytics","solhog","goodgreenguru","agwcon","ofigofficial","aethan","thebestchange","wschnes","jwspry","criticalreading","christellar","chdn14","croakeyblog","femmekatz","imagine4756","seedbomz4change","datatect","smbthomas","revkin","dulcyj","vinepsychic","saskboy","chrisogilviesnr","mkeenan204","carrie22202","econewstoronto","kaskadia","bflo2lkn","adekunlemao","youevolving","ayogelutwae","ianizzat","wmagates","ecointeractive","billlinton1","treehuggeruk","ruralgrubby","twiggjohn","johnrussell40","nwohashtag","guardiansustbiz","sherronu","0vigia","indiefriend_","nollyprott","tavernkeepers","dapro63","greenlocal175","energycollectiv","simonfili","sheila_info","6esm","kivunature","readnthink90","wtfrly","padbrit","climateactionbc","seeker401","donbeeman","outerspacepi","milesgrant","bornonthebayou9","upayr","activist360","maddog4u_1st","danfmto","alex_verbeek","vegemiteblues","climatevmonitor","schwild","parkerzack","oscare2000","mercyfist","p_hannam","barrowice","greeneral","ooclimatechange","kuffodog","foreffectivegov","lyndsayfarlow","rustygreen59","thestevecohen","jpgseva","weadapt1","idontcopit","teresaplatt","flag_of_freedom","doctorjoe56","nodirectaction","thedailyclimate","debeauxos1","voicemymind","michaelemann","christopherwr11","wraithaz","_andreaangulo_","daz9162","iluvco2","carbonzero","orangekick","osmanakkoca","global_policy","macdade2","carbonstory","uscan","kazza_d","morphizm","gdthomp01_bkup","tomodell","brenthoare","johnfosterway","biggator5","philipcjames","4589roger","nzblackcapsp305","comradearthur","earth_newsrt","moronwatch","barkway","gtmcg","pbennett2253","axeco2tax","thewrightwingv2","cobs4340","vmpcott","johnnya99","ar7za","johnmknox","modditydodds","communizine","mwt2008","connect4climate","orach24463_cj","dmlucky","wrh_mike_rivero","craigthomler","agfelpaso","paloring","andrewdavid70","holymosesy","duncankeeling","eco_melon","climate_con","saveusnowdotorg","earthvitalsigns","pmgeezer","takvera","reachscale","nafeezahmed","carbongate","energyclimatede","r_cherwink","mfalz01","env1ronment","morehouse64","yourearthshare","galileomovement","fenbeagle","tavernbarkeep","yolibeans","capecarbon","glowarmingtimes","dontcopitusa","carlaivey","cartwitz","ki_sekiya"]

#olduserlist=["marcherlord1","juicexlx","profofphysics","john_symond","johnwboyko","isf_activist","prophetfella","valentinasos","jenninocsg","anewgreenearth","eco_mellon","iioannoulbs","checkoutspy","toryaardvark","greenmanlife","peter_ho","al_perri","avjoe_realdeal","isf_global_net","jane1776","fingersflying","quantum2050","myworld2015","freepublictrans","robinhood1776","faunkime","theophany1","mooseandskwerl","cave_dweller31","netpresident","agw_is_a_hoax","bcfoodsecurity","thrivingplanet","timeclockman","benwinslow","iowenau","hepworks","1111_castle","prometheus2054","nonsumdignus","docrichard","otiose94","seahorse555","thestevenoracle","dustt","melissablancha6","fernandezeugene","cristiamrr","brevissi","kingscollegelib","storyroute","andybarton10","stonepaperprose","presstitution","wordsofpower","bberwyn","amsecproject","mikeseager","lffriedman","fathertheo","ronpaulnot4me","greenmotorgroup","skpatriot","blizzybe","bradleyjdibble","morehouse64","soshann","russellcavanagh","archweek","ddagan","alicecharles","coffeewarblers","carlos_s01","pdjmoo","progressiveport","chelseafanindo","anand_sivaram","seetac7","skyblue204","climatechange_1","darthvectivus","thetrendisblue","climatehotnews","ausaction","ormiga","deepgreendesign","paulhbeckwith","havenr64","evolvingcaveman","gdthomp01","empirical_bayes","lubedupnoob","snarkathon","nspugh","carbontaxscam","enviroedgenews","gogreenmotors","gillgarmesh","focusonprogress","greenhome2011","jackthelad1947","justintempler","therealnews365","lynestel","sailors_warning","infocyde","onahunttoday","mtl4u2","greenistweet","karlos1705","benwest","ruisaldanha","carlaivey","ddimick","preciseblogs","gogreencelebs","allanmargolin","iamgreenbean","sobatborneo","azofgwarming","openermedia","climaloop","marcysummer","warming_global","nrdc","bentler","wizquizman","julia__reid","junkscience","asiseeitnow","getglobe","safeclimatecamp","lumahaimike","solleshunter","nandauganda","ecowatch","climateresolve","kings_cambridge","windfallcentre","decisionlab","grahamdlovell","javawinters","merlyn43","aladdintweets","climatehawk1","suzlette333","zelo_street","agwargentina","mlhagood","global__warming","redostoneage","askgerbil","mothincarnate","usashopper","vk3bbr","all_a_twitt_r","pitbull_dale305","oparasitesingle","weshopper","maggie_pdx","strategikas","carlsiegrist","whotnaught","jonathan_drake","ecomanleader","johnzangas","opentoinfo","bjork55","collinmaessen","annemobile","occupy_oklahoma","sydnets","preppersnews1","lucalombroso","y_10k","cechr_uod","brains3","dawn9476","boldrepublic","anthonybritneff","serenity13","snafu_au","empathynow","50yearforecast","escalatorover","mamacorin","tkjohndaniels","realistic_view","laurieload","waxmanclimate","charles_consult","wisco","anaelisafoto","stjarnafranfall","orach24463_cj","hschwende","qldaah","respect65","gerry6868","perceiver1219","zoerey","mfearby","snvredd","ayeshavit","jj_mcneal","polluterwatch","karsenis","thepoliticalhat","greatbooks2read","2dialogue","jeffreylowes","edwiebe","sensanders","noconsensus","newstruthliz","tadlette","aloha_analytics","solhog","agwcon","ofigofficial","aethan","thebestchange","wschnes","jwspry","criticalreading","christellar","chdn14","croakeyblog","t_p_luxe","femmekatz","seedbomz4change","datatect","smbthomas","revkin","dulcyj","vinepsychic","chrisogilviesnr","mkeenan204","carrie22202","econewstoronto","kaskadia","bflo2lkn","adekunlemao","youevolving","ayogelutwae","ianizzat","wmagates","ecointeractive","billlinton1","treehuggeruk","johnrussell40","nwohashtag","guardiansustbiz","sherronu","0vigia","indiefriend_","nollyprott","tavernkeepers","dapro63","greenlocal175","energycollectiv","simonfili","sheila_info","6esm","kivunature","readnthink90","wtfrly","climateactionbc","seeker401","donbeeman","utahpolitics","milesgrant","big_norm","bornonthebayou9","upayr","activist360","vegemiteblues","climatevmonitor","schwild","parkerzack","mercyfist","p_hannam","greeneral","ochsnews","ooclimatechange","kuffodog","foreffectivegov","lyndsayfarlow","rustygreen59","sustainablewits","thestevecohen","teresaplatt","flag_of_freedom","doctorjoe56","nodirectaction","thedailyclimate","debeauxos1","michaelemann","alex_verbeek","wraithaz","_andreaangulo_","daz9162","iluvco2","carbonzero","orangekick","osmanakkoca","global_policy","macdade2","carbonstory","kazza_d","morphizm","gdthomp01_bkup","tomodell","brenthoare","maritzaincali","elizabethbold","johnfosterway","philipcjames","4589roger","nzblackcapsp305","comradearthur","earth_newsrt","moronwatch","arhobley","dana1981","barkway","gtmcg","pbennett2253","thewrightwingv2","cobs4340","vmpcott","tavernbarkeep","johnnya99","ar7za","johnmknox","modditydodds","communizine","mwt2008","connect4climate","dcarli","dmlucky","wrh_mike_rivero","craigthomler","agfelpaso","paloring","andrewdavid70","holymosesy","duncankeeling","climate_con","saveusnowdotorg","pmgeezer","takvera","reachscale","barrowice","carbongate","energyclimatede","newenglandite","r_cherwink","mfalz01","env1ronment","capandtrade","galileomovement","fenbeagle","iteration23","yolibeans","capecarbon","glowarmingtimes","weadapt1","politicolnews","cartwitz","ki_sekiya"]

#userlist=userlist[0:10]

shuffle(userlist)
validchars=['a','g','n', 'u', 'more', "'more'", "quit", "'quit'"]
con=lite.connect("combinedusersdb.db")
cur=con.cursor()
try:
    logfile=open("usertags"+name+".txt","r+")
#Add way of resuming from file
    t=logfile.read()
except:
    t=None
    logfile=open("usertags"+name+".txt","w")    
#print t
if t !=None and t!="":
    g=(t.split("\n"))
    for line in g:
        if "," in line:
            checkedusers.append((line.split(","))[0])

n=0
#print checkedusers
for user in userlist:
    #Get blurb
    #get sample of tweets from main databases
    #Webpage? Check user info
    #Display data, log result, make sure works okay
    morecount=0
    if not (user in checkedusers):
        n+=1
        print "###########################"
        print ("Username: " + str(user))
        tweets=[]
        cur.execute("SELECT Description FROM descriptions WHERE ScreenName='"+str(user)+"'")
        z=cur.fetchall()
        description=z[0][0]
        cur.execute("SELECT DISTINCT Tweet FROM tweets WHERE ScreenName='"+str(user)+"' COLLATE NOCASE")
        temp=cur.fetchall()
        for item in temp:
            tweets.append(item)
        shuffle(tweets)
        if len(tweets)<11:
            lim=len(tweets)
            dstr="all tweets"
            morepos=False
        else:
            lim=10
            dstr="10 of "+str(len(tweets)) +" tweets"
            morepos=True
        print("Description:")
        if description in nondesc:
            print("No description provided.")
        else:
            print(description)
        print("Recent Tweets:")
        for i in range(lim):
            print(tweets[i][0])
        # Get user input
        print "-------------------------------------"    
        print("Showing "+ dstr +". Is " + user +" an activist (A), skeptic (G), neutral (N), or unknown (U)?\nType 'more' to see more tweets if possible, or 'quit' to quit and resume later. User " + str(n+len(checkedusers)) +"/" + str(len(userlist)))
        stry=True
        while stry==True:
            minput=raw_input().lower()
            if (minput in validchars):
                if (minput=="quit") or (minput=="'quit'"):
                    logfile.close()
                    sys.exit("Goodbye. Please resume this process later by using the same name: " + str(name))
                if (minput!="more") and (minput!="'more'"):
                    stry=False
                else:
                    if morepos==True:
                        morecount+=1
                        if len(tweets[(morecount*10):])<11:
                            lim=len(tweets[(morecount*10):])
                            morepos=False
                            dstr="all tweets"
                        else:
                            lim=10
                            dstr= str(10*(morecount+1)) +" of "+str(len(tweets)) +" tweets"
                        for i in range(lim):
                            print(tweets[(morecount*10)+i])
                        print("Showing "+ dstr +". Is " + user +" an activist (A), skeptic (G), neutral (N), or unknown (U)? Or type 'more' to see more tweets if possible.")
                    else:
                        print("Cannot print more tweets. Please enter a valid selection:  activist (A), skeptic (G), neutral (N), or unknown (U):")
            else:
                print("Please enter a valid selection:  activist (A), skeptic (G), neutral (N), or unknown (U):")
        logfile.write(user+","+minput+"\n")
        logfile.flush()

logfile.close()
print "Finished. Thanks for your work."
    
#Need to work out how to insert results in to clustering
