import sqlite3

def run_sql(sql: str):
    con = sqlite3.connect("users.db")

    cur = con.cursor()

    res = cur.execute(sql)
    
    data = res.fetchall()
    
    con.commit()

    return data
