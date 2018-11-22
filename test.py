import socket
import sqlite3
import uuid


print(uuid.uuid4().hex.__str__().__len__())

connectedDB = sqlite3.connect("C:\\Users\\Veto\\Мои документы\\newdb.sqlite")
cursor = connectedDB.cursor()

sock = socket.socket()
sock.bind(("127.0.0.1", 7070))
sock.listen(5)


def send_answer(conn, data=""):
    data = data.encode("utf-8")
    conn.send(data)

def getUIDorRegister(conn, data):
    mode, login, password = map(str, data.split(" "))
    if (mode == 'reg'):
        tempUID = uuid.uuid4().hex.__str__()
        sql = "INSERT INTO users (login, pass, uid) VALUES ('%s','%s','%s')" % (login, password, tempUID)
        print(sql)
        try:
            cursor.execute(sql)
            connectedDB.commit()
            mode = 'login'
        except:
            send_answer(conn, data='le')    #login exist
    if (mode == 'login'):
        sql = "SELECT uid FROM users WHERE login = '%s' AND pass = '%s'" % (login, password)
        cursor.execute(sql)
        try:
            results = cursor.fetchall()[0][0]
            send_answer(conn, data=results)
        except:
            send_answer(conn, data='bl' + (' ' * 30))   #bad login


try:
    while 1:
        conn, addr = sock.accept()
        print("New connection from " + addr[0])
        try:
            data = conn.recv(1024)
            print(data.decode("utf-8"))
            getUIDorRegister(conn, data.decode("utf-8"))
        except:
            send_answer(conn, data="Er" + (' ' * 30))   #Error
        finally:
            conn.close()
finally:
    sock.close()

connectedDB.close()