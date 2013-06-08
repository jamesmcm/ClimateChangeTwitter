import sqlite3 as lite
tcon=lite.connect("userdb.db")
tcur=tcon.cursor()
mintime=1358090418
con=lite.connect("tempdb.db")
cur=con.cursor()

def escapes(s):
    f=s[0]
    s=s[1:-1]
    s=s.replace(r'"', r'\"')
    if f=='"':
        s=s.replace(r"'", r"\'")

    s=s.replace(r"\'", r"''")
    s="'"+s+"'"
    return s

#tcur.execute("CREATE TABLE descriptions(ScreenName TEXT, Description TEXT)")

cur.execute("SELECT * FROM descriptions")
d=cur.fetchall()

for item in d:
    print("INSERT INTO descriptions VALUES('"+item[0]+"',"+escapes(repr(item[1])[1:]) + ")")
    tcur.execute("INSERT INTO descriptions VALUES('"+item[0]+"',"+escapes(repr(item[1])[1:]) + ")")

tcon.commit()
tcon.close()
con.close()
