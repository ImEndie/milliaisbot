import psycopg2
from vars import PG_URI

def get_all():
    conn = psycopg2.connect(PG_URI)
    cur=conn.cursor()
    cur.execute('SELECT chat_id FROM Persons;')
    l=cur.fetchall()
    cur.close()
    conn.close()
    return l

def get_count():
    conn = psycopg2.connect(PG_URI)
    cur=conn.cursor()
    cur.execute('SELECT chat_id FROM Persons;')
    l=cur.fetchall()
    cur.close()
    conn.close()
    return len(l)

def ins(chat_id):
    conn = psycopg2.connect(PG_URI)
    cur=conn.cursor()
    id=str(chat_id)
    cur.execute("""SELECT * FROM Persons
WHERE chat_id='%s';"""%id)
    user=cur.fetchone()
    if user:
        cur.close()
        conn.close()
        return
    cur.execute("""INSERT INTO Persons (chat_id)
VALUES ('%s');"""%(id))
    conn.commit()
    cur.close()
    conn.close()