import sqlite3


"""def chk_conn(conn):
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


connection = sqlite3.connect('spotifystats.db')

print(chk_conn(connection))"""


connection = sqlite3.connect('spotifystats.db')


cursor = connection.cursor()

cursor.execute(
    "INSERT INTO USERS (username,password,user_id) VALUES ('ajuneja','koolzo','13445594594394')")
connection.commit()
