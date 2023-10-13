import os, sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    path = os.getcwd()

    f = open(path+'/data.sql')
    script = f.read()

    cur.executescript(script)

    cur.execute('select * from app_article')

    for row in cur.fetchmany(2):
        print(row)

finally:
    f.close()
    conn.close()