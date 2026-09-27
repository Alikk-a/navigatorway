import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="root",
    database="navigator_21",
)
with conn.cursor() as cur:
    cur.execute(
        "SELECT pageparid, COUNT(1) FROM bill_pages GROUP BY pageparid ORDER BY 2 DESC LIMIT 15"
    )
    print("counts", cur.fetchall())
    for pid in (5, 7, 11, 13, 3):
        cur.execute(
            "SELECT COUNT(1) FROM bill_pages WHERE pageparid=%s",
            (pid,),
        )
        print(pid, cur.fetchone()[0])
