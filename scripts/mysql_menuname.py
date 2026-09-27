import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="root",
    database="navigator_21",
    cursorclass=pymysql.cursors.DictCursor,
)
with conn.cursor() as cur:
    cur.execute(
        "SELECT pageid, pagename, menuname, pagetitle FROM bill_pages WHERE pageparid=15 AND pagename LIKE 'praktik%' LIMIT 5"
    )
    for row in cur.fetchall():
        print(row)
