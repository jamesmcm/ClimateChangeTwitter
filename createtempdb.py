import sqlite3 as lite
from classtweetgetter import DBTweetGetter
import string
from time import sleep
import sys
def escapes(s):
    f=s[0]
    s=s[1:-1]
    s=s.replace(r'"', r'\"')
    if f=='"':
        s=s.replace(r"'", r"\'")

    s=s.replace(r"\'", r"''")
    s="'"+s+"'"
    return s

tcon=lite.connect("tweetsdb.db")
tcur=tcon.cursor()
mintime=1358090418
con=lite.connect("diffusersetcdb.db")
cur=con.cursor()
cur.execute("CREATE TABLE tweets(ScreenName TEXT, Tweet TEXT)")
cur.execute("CREATE TABLE descriptions(ScreenName TEXT, Description TEXT)")

mytweetgetter=DBTweetGetter(None, None)

userlist=['bottonT', 'bethanyjayne_o9', 'james12h', 'marclanders', 'ss0alexander', 'jholuvu', 'lucid_serenity', 'aashishmusic', 'lachecard', 'ombuscool', 'nurdan_dirik', 'orlandovips', 'cochran_sarah', 'erdemturgan', 'wowpitbull', 'sonymusicmexico', 'juan20da', 'mountainspop', 'ldesherl', 'hayleysellick', 'viewpointmelb', 'peped6', '0hastronaut', 'kateescorey', 'tiamauli', 'ridwaancn', 'obsessionwill', '7daniel_ronaldo', 'gatewaypundit', 'keylacabanillas', 's_cebi_o', 'tarndeep_virdi', 'pauldoogood', 'aem4444', 'larindaguedes', 'mbleez', 'june_stoyer', 'eifever', 'anshumminhas', 'joseaparicio90', 'just2opine', 'motiffmusic', 'juanmaganmusic', 'drsarahsviews', 'annedinning', 'omilynn', 'c_harris82', 'kencaldeira', 'sensato', 'acminaj95', 'weez100_', 'yungrugga_', 'climate_sceptic', 'serega_markov', 'pitbull', 'ladyseastar', 'robcarrollmusic', 'pecaito1', 'fanspitbull', 'yoloswag_1d', 'juufaria', 'liaginn', 'abcnews', 'pitpelez', 'jrcats9', 'jadorepitbull1', 'tylerhavocderek', 'wbsustaindev', 'magnoliazoe', 'mattd1188', 'konvictjapan', 'mee_mee94', 'brandondyunga', 'enrique_09', 'call_me_rico_', 'jbiebertlove', 'shinrinohousoku', 'thomasdeusex', 'pitarmandofan', 'marisag5', 'doctorkarl', 'awsome305', 'arleenvargas', 'lisadesherlia', 'maaijlover', 'kamtoriumi', 'missdebra32', 'imydal', 'connieangela', 'chloew231195', 'caringenough', '1d_uhotbeasts', 'pitfan305', 'nubsenvgmowatch', 'thesecondgoing', 'syrenica', 'questionsfirst', 'bertie8689', 'mrleonardobass', 'mvm__mvm', 'qfinance_', 'michelesimili', 'wganapini', 'dcmiccheck', 'suzannewaldman', 'greendems', 'tmc_tolbert', 'my_enrique', 'ruthietom', 'cdanilda', 'junestoyer', 'batinozturk', 'goldennuggetac', 'damlaomput', 'miguelvazquezc', 'batchelorann', 'mindfulgreen', 'terryrudd1964', 'mariogagliardi4', 'ecoleaders', 'forpoljournal', 'caretoclick', '_heymamitas_', 'welovepit', 'bertom83', 'paula_pitbull', 'johndvincent12', 'meaniegmd', 'reallyarudeboy', 'nellywagner', 'organicview', 'gabriella_maria', 'rosecamacho13', 'todomaru123', 'caesarpeace', 'dudethinking', 'andrw100', 'norways1dfan', 'leonidosaurio', 'arwenandsmokey', 'forlautner', 'hoopcikilopp', 'jesusrm14', 'theorganicview']

z=0
length=len(userlist)
for user in userlist:
    cur.execute("SELECT * FROM descriptions WHERE ScreenName='"+str(user)+"'")
    dt=cur.fetchall()

    z+=1
    print str(z) + "/" + str(length)
    if len(dt)==0 and user!='hateless_speech':
        print user
        d=[]
        tcur.execute("SELECT ScreenName, Tweet FROM htclimatechange WHERE ScreenName='"+user+"' COLLATE NOCASE AND ConvertedTime > "+ str(mintime))
        d+=tcur.fetchall()
        tcur.execute("SELECT ScreenName, Tweet FROM htglobalwarming WHERE ScreenName='"+user+"' COLLATE NOCASE AND ConvertedTime > "+ str(mintime))
        d+=tcur.fetchall()
        tcur.execute("SELECT ScreenName, Tweet FROM htagw WHERE ScreenName='"+user+"' COLLATE NOCASE AND ConvertedTime > "+ str(mintime))
        d+=tcur.fetchall()
        if len(d)==0:
            print "ERROR! " + user
        for item in d:
            #print "INSERT INTO tweets VALUES('"+str(item[0])+"',"+escapes(repr(item[1])[1:]) + ")"
            cur.execute("INSERT INTO tweets VALUES('"+str(item[0])+"',"+escapes(repr(item[1])[1:]) + ")" )

        #description=mytweetgetter.getUserDescription(user)
        #cur.execute("INSERT INTO descriptions VALUES('"+user+"',"+escapes(repr(description)[1:]) + ")" )
        cur.execute("INSERT INTO descriptions VALUES('"+user+"','IGNORE' )" )
        con.commit()
        #sleep(60)
con.commit()
con.close()
tcon.close()
