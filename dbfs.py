#Do directed breadth first search to complete path-length/path matrix
import networkx as nx
import numpy as np
import operator
import sys

# class BFSstep(object):
#     def __init__(self,node,curpath):
#         self.node=node
#         self.curpath=curpath
#     def step(self):
#         name=userdict[self.node]
#         try:
#             if (arraydict[gname][name][0]==len(self.curpath)):
#                 gl=arraydict[gname][name][1]
#                 gl+=[self.curpath]
#                 arraydict[gname][name]=(len(self.curpath), gl)
#             elif (arraydict[gname][name][0]==len(self.curpath)):
#                 arraydict[gname][name]=(len(self.curpath), [self.curpath])
                
#         except:
#             arraydict[gname][name]=(len(self.curpath), [self.curpath])
#         l=g.successors(self.node)
#         for item in l:
#             if not (item in self.curpath):
#                 newpath=list(self.curpath+[item])
#                 bfslist.append(BFSstep(item, newpath))


class BFSstep(object):
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

userdict={1:"marcherlord1",2:"juicexlx",3:"profofphysics",4:"john_symond",5:"johnwboyko",6:"isf_activist",7:"prophetfella",8:"valentinasos",9:"jenninocsg",10:"anewgreenearth",11:"eco_mellon",12:"iioannoulbs",14:"toryaardvark",15:"greenmanlife",16:"peter_ho",17:"al_perri",18:"avjoe_realdeal",19:"isf_global_net",20:"jane1776",21:"fingersflying",22:"quantum2050",23:"myworld2015",24:"freepublictrans",25:"robinhood1776",26:"faunkime",27:"theophany1",28:"mooseandskwerl",30:"netpresident",31:"agw_is_a_hoax",32:"bcfoodsecurity",33:"thrivingplanet",34:"timeclockman",35:"benwinslow",36:"iowenau",37:"hepworks",39:"prometheus2054",40:"nonsumdignus",41:"docrichard",42:"otiose94",43:"seahorse555",45:"dustt",46:"melissablancha6",47:"fernandezeugene",48:"cristiamrr",49:"brevissi",50:"kingscollegelib",51:"storyroute",52:"andybarton10",55:"wordsofpower",56:"bberwyn",57:"amsecproject",58:"mikeseager",59:"lffriedman",60:"fathertheo",61:"ronpaulnot4me",62:"greenmotorgroup",63:"skpatriot",64:"blizzybe",65:"bradleyjdibble",66:"morehouse64",67:"soshann",68:"russellcavanagh",69:"archweek",70:"ddagan",72:"coffeewarblers",73:"carlos_s01",74:"pdjmoo",75:"progressiveport",77:"anand_sivaram",78:"seetac7",79:"skyblue204",80:"climatechange_1",81:"darthvectivus",82:"thetrendisblue",83:"climatehotnews",84:"ausaction",85:"ormiga",86:"deepgreendesign",87:"paulhbeckwith",88:"havenr64",89:"evolvingcaveman",90:"gdthomp01",91:"empirical_bayes",92:"lubedupnoob",93:"snarkathon",94:"nspugh",95:"carbontaxscam",96:"enviroedgenews",97:"gogreenmotors",98:"gillgarmesh",99:"focusonprogress",100:"greenhome2011",101:"jackthelad1947",102:"justintempler",103:"therealnews365",104:"lynestel",105:"sailors_warning",106:"infocyde",107:"onahunttoday",108:"mtl4u2",109:"greenistweet",110:"karlos1705",111:"benwest",112:"ruisaldanha",114:"ddimick",115:"preciseblogs",116:"gogreencelebs",117:"allanmargolin",118:"iamgreenbean",120:"azofgwarming",122:"climaloop",124:"warming_global",125:"nrdc",126:"bentler",127:"wizquizman",128:"julia__reid",129:"junkscience",130:"asiseeitnow",131:"getglobe",132:"safeclimatecamp",133:"lumahaimike",134:"solleshunter",135:"nandauganda",136:"ecowatch",137:"climateresolve",138:"kings_cambridge",139:"windfallcentre",140:"decisionlab",141:"grahamdlovell",142:"javawinters",143:"merlyn43",144:"aladdintweets",145:"climatehawk1",146:"suzlette333",147:"zelo_street",149:"mlhagood",150:"global__warming",151:"redostoneage",152:"askgerbil",153:"mothincarnate",154:"usashopper",155:"vk3bbr",156:"all_a_twitt_r",158:"oparasitesingle",159:"weshopper",160:"maggie_pdx",161:"strategikas",162:"carlsiegrist",163:"whotnaught",164:"jonathan_drake",165:"ecomanleader",166:"johnzangas",167:"opentoinfo",168:"bjork55",169:"collinmaessen",170:"annemobile",171:"occupy_oklahoma",172:"sydnets",173:"preppersnews1",174:"lucalombroso",175:"y_10k",176:"cechr_uod",177:"brains3",178:"dawn9476",179:"boldrepublic",180:"anthonybritneff",181:"serenity13",182:"snafu_au",183:"empathynow",184:"50yearforecast",185:"escalatorover",186:"mamacorin",187:"tkjohndaniels",188:"realistic_view",189:"laurieload",190:"waxmanclimate",191:"charles_consult",192:"wisco",193:"anaelisafoto",194:"stjarnafranfall",195:"orach24463_cj",196:"hschwende",197:"qldaah",198:"respect65",199:"gerry6868",200:"perceiver1219",201:"zoerey",202:"mfearby",203:"snvredd",204:"ayeshavit",206:"polluterwatch",207:"karsenis",208:"thepoliticalhat",209:"greatbooks2read",210:"2dialogue",211:"jeffreylowes",212:"edwiebe",213:"sensanders",214:"noconsensus",216:"tadlette",218:"solhog",219:"agwcon",220:"ofigofficial",221:"aethan",222:"thebestchange",223:"wschnes",224:"jwspry",226:"christellar",227:"chdn14",228:"croakeyblog",229:"t_p_luxe",230:"femmekatz",231:"seedbomz4change",232:"datatect",233:"smbthomas",234:"revkin",236:"vinepsychic",237:"chrisogilviesnr",238:"mkeenan204",239:"carrie22202",241:"kaskadia",242:"bflo2lkn",243:"adekunlemao",244:"youevolving",246:"ianizzat",247:"wmagates",248:"ecointeractive",249:"billlinton1",250:"treehuggeruk",251:"johnrussell40",252:"nwohashtag",253:"guardiansustbiz",254:"sherronu",255:"0vigia",257:"nollyprott",258:"tavernkeepers",259:"dapro63",261:"energycollectiv",262:"simonfili",263:"sheila_info",264:"6esm",265:"kivunature",266:"readnthink90",267:"wtfrly",268:"climateactionbc",269:"seeker401",270:"donbeeman",271:"utahpolitics",272:"milesgrant",273:"big_norm",274:"bornonthebayou9",275:"upayr",276:"activist360",277:"vegemiteblues",278:"climatevmonitor",279:"schwild",280:"parkerzack",281:"mercyfist",282:"p_hannam",283:"greeneral",284:"ochsnews",285:"ooclimatechange",287:"foreffectivegov",288:"lyndsayfarlow",289:"rustygreen59",290:"sustainablewits",291:"thestevecohen",292:"teresaplatt",293:"flag_of_freedom",294:"doctorjoe56",295:"nodirectaction",296:"thedailyclimate",297:"debeauxos1",298:"michaelemann",299:"alex_verbeek",300:"wraithaz",301:"_andreaangulo_",302:"daz9162",303:"iluvco2",304:"carbonzero",306:"osmanakkoca",307:"global_policy",308:"macdade2",309:"carbonstory",310:"kazza_d",311:"morphizm",312:"gdthomp01_bkup",314:"brenthoare",315:"maritzaincali",316:"elizabethbold",317:"johnfosterway",318:"philipcjames",319:"4589roger",321:"comradearthur",322:"earth_newsrt",323:"moronwatch",324:"arhobley",325:"dana1981",326:"barkway",327:"gtmcg",328:"pbennett2253",329:"thewrightwingv2",330:"cobs4340",331:"vmpcott",332:"tavernbarkeep",333:"johnnya99",334:"ar7za",335:"johnmknox",336:"modditydodds",338:"mwt2008",339:"connect4climate",340:"dcarli",341:"dmlucky",342:"wrh_mike_rivero",343:"craigthomler",344:"agfelpaso",345:"paloring",346:"andrewdavid70",347:"holymosesy",348:"duncankeeling",349:"climate_con",350:"saveusnowdotorg",351:"pmgeezer",352:"takvera",353:"reachscale",354:"barrowice",355:"carbongate",356:"energyclimatede",357:"newenglandite",358:"r_cherwink",359:"mfalz01",360:"env1ronment",361:"capandtrade",362:"galileomovement",363:"fenbeagle",364:"iteration23",365:"yolibeans",367:"glowarmingtimes",368:"weadapt1",369:"politicolnews",370:"cartwitz",371:"ki_sekiya"}


skeptics=["marcherlord1","profofphysics","prophetfella","toryaardvark","peter_ho","jane1776","fingersflying","mooseandskwerl","agw_is_a_hoax","timeclockman","prometheus2054","nonsumdignus","seahorse555","thestevenoracle","brevissi","mikeseager","ronpaulnot4me","skpatriot","morehouse64","russellcavanagh","carlos_s01","seetac7","skyblue204","darthvectivus","havenr64","gdthomp01","carbontaxscam","gillgarmesh","justintempler","therealnews365","infocyde","karlos1705","preciseblogs","wizquizman","julia__reid","junkscience","asiseeitnow","lumahaimike","mlhagood","redostoneage","vk3bbr","whotnaught","jonathan_drake","annemobile","y_10k","brains3","boldrepublic","realistic_view","orach24463_cj","gerry6868","mfearby","ayeshavit","jj_mcneal","thepoliticalhat","greatbooks2read","noconsensus","aloha_analytics","agwcon","thebestchange","jwspry","chdn14","smbthomas","nwohashtag","sherronu","0vigia","nollyprott","dapro63","simonfili","readnthink90","wtfrly","seeker401","donbeeman","big_norm","bornonthebayou9","parkerzack","lyndsayfarlow","nodirectaction","iluvco2","kazza_d","gdthomp01_bkup","tomodell","comradearthur","gtmcg","pbennett2253","thewrightwingv2","vmpcott","johnnya99","johnmknox","wrh_mike_rivero","agfelpaso","climate_con","pmgeezer","barrowice","carbongate","mfalz01","galileomovement","fenbeagle"]

activists=["juicexlx","john_symond","johnwboyko","isf_activist","valentinasos","jenninocsg","anewgreenearth","eco_mellon","iioannoulbs","greenmanlife","avjoe_realdeal","isf_global_net","quantum2050","myworld2015","freepublictrans","robinhood1776","faunkime","theophany1","cave_dweller31","netpresident","bcfoodsecurity","thrivingplanet","iowenau","hepworks","1111_castle","docrichard","otiose94","dustt","melissablancha6","fernandezeugene","cristiamrr","storyroute","andybarton10","wordsofpower","bberwyn","amsecproject","lffriedman","fathertheo","greenmotorgroup","blizzybe","bradleyjdibble","soshann","archweek","ddagan","alicecharles","coffeewarblers","pdjmoo","progressiveport","anand_sivaram","climatechange_1","thetrendisblue","climatehotnews","ausaction","deepgreendesign","paulhbeckwith","evolvingcaveman","empirical_bayes","lubedupnoob","snarkathon","nspugh","enviroedgenews","gogreenmotors","focusonprogress","greenhome2011","jackthelad1947","lynestel","sailors_warning","onahunttoday","mtl4u2","greenistweet","benwest","ruisaldanha","ddimick","gogreencelebs","allanmargolin","iamgreenbean","azofgwarming","openermedia","climaloop","marcysummer","warming_global","nrdc","bentler","getglobe","safeclimatecamp","solleshunter","nandauganda","ecowatch","climateresolve","kings_cambridge","windfallcentre","decisionlab","grahamdlovell","javawinters","merlyn43","aladdintweets","climatehawk1","suzlette333","zelo_street","global__warming","askgerbil","mothincarnate","all_a_twitt_r","oparasitesingle","weshopper","maggie_pdx","strategikas","carlsiegrist","ecomanleader","johnzangas","opentoinfo","bjork55","collinmaessen","occupy_oklahoma","sydnets","lucalombroso","cechr_uod","dawn9476","anthonybritneff","serenity13","snafu_au","empathynow","50yearforecast","escalatorover","mamacorin","laurieload","waxmanclimate","charles_consult","wisco","anaelisafoto","stjarnafranfall","hschwende","qldaah","respect65","perceiver1219","zoerey","snvredd","polluterwatch","karsenis","2dialogue","edwiebe","sensanders","newstruthliz","tadlette","solhog","ofigofficial","aethan","wschnes","criticalreading","christellar","croakeyblog","t_p_luxe","femmekatz","seedbomz4change","datatect","revkin","vinepsychic","chrisogilviesnr","mkeenan204","carrie22202","econewstoronto","kaskadia","bflo2lkn","adekunlemao","youevolving","ianizzat","ecointeractive","billlinton1","treehuggeruk","johnrussell40","guardiansustbiz","greenlocal175","energycollectiv","sheila_info","6esm","kivunature","climateactionbc","milesgrant","upayr","activist360","vegemiteblues","climatevmonitor","mercyfist","p_hannam","ochsnews","ooclimatechange","kuffodog","foreffectivegov","rustygreen59","sustainablewits","thestevecohen","doctorjoe56","thedailyclimate","debeauxos1","michaelemann","alex_verbeek","wraithaz","_andreaangulo_","daz9162","carbonzero","orangekick","osmanakkoca","global_policy","macdade2","carbonstory","morphizm","brenthoare","maritzaincali","elizabethbold","johnfosterway","philipcjames","4589roger","earth_newsrt","moronwatch","arhobley","dana1981","barkway","cobs4340","ar7za","communizine","mwt2008","connect4climate","dcarli","dmlucky","craigthomler","paloring","andrewdavid70","holymosesy","duncankeeling","saveusnowdotorg","takvera","reachscale","energyclimatede","newenglandite","r_cherwink","env1ronment","capandtrade","iteration23","yolibeans","glowarmingtimes","weadapt1","politicolnews","cartwitz"]

#Read GML
g=nx.read_gml("oldcombinedusergc.gml")

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
print "Degree distributions"
print "Follower degree distribution"
print sdegreedist
print "Friend degree distribution"
print pdegreedist
print "Total degree distribution"
print tdegreedist


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


print "Number of skeptics: " + str(len(skeptics)) + ", number of activists: " + str(len(activists))
print "Path lengths"
print "Globally:"
print "Mean: " + str(np.mean(globallist)) +", Standard deviation: " + str(np.std(globallist)) + ", Number of paths: " + str(len(globallist))
print "Activist-Activist:"
print "Mean: " + str(np.mean(aalist)) +", Standard deviation: " + str(np.std(aalist)) + ", Number of paths: " + str(len(aalist))
print "Activist-Skeptic:"
print "Mean: " + str(np.mean(aslist)) +", Standard deviation: " + str(np.std(aslist))+ ", Number of paths: " + str(len(aslist))
print "Skeptic-Activist:"
print "Mean: " + str(np.mean(salist)) +", Standard deviation: " + str(np.std(salist))+ ", Number of paths: " + str(len(salist))
print "Skeptic-Skeptic:"
print "Mean: " + str(np.mean(sslist)) +", Standard deviation: " + str(np.std(sslist))+ ", Number of paths: " + str(len(sslist))

#Calculate fraction of shortest paths in which each user is present, rank by betweenness
#print str(len(arraydict.keys()))
#print str(len(arraydict["moronwatch"].keys()))
nlist=[]

# betweennessd={}
# for user in nodelist:
#     b=0
#     n=0
#     for i in arraydict.keys():
#         for j in arraydict[i].keys():
#             n+=1
#             if user in arraydict[i][j][1]:
#                 b+=1
            
#             # ll=arraydict[i][j][1]
#             # for l in ll:
#             #     n+=1
#             #     if user in l:
#             #         b+=1
#     b=float(b)/float(n)
#     betweennessd[userdict[user]]=b
#     nlist.append(n)


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
            # if (i in activists) and (j in activists):
            #     n[0]+=1
            # elif (i in activists) and (j in skeptics):
            #     n[1]+=1
            # elif (i in skeptics) and (j in activists):
            #     n[2]+=1
            # elif (i in skeptics) and (j in skeptics):
            #     n[3]+=1

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
    for z in range(4):
        bign[z]+=n[z]
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
print "Total number of paths: " + str(bign[0])
print (sorteddict[0:9])
print "Activist-Skeptic"
sorteddict = sorted(betweennessdas.iteritems(), key=operator.itemgetter(1))
sorteddict.reverse()
print "Total number of paths: " + str(bign[1])
print (sorteddict[0:9])
print "Skeptic-Activist"
sorteddict = sorted(betweennessdsa.iteritems(), key=operator.itemgetter(1))
sorteddict.reverse()
print "Total number of paths: " + str(bign[2])
print (sorteddict[0:9])
print "Skeptic-Skeptic"
sorteddict = sorted(betweennessdss.iteritems(), key=operator.itemgetter(1))
sorteddict.reverse()
print "Total number of paths: " + str(bign[3])
print (sorteddict[0:9])

