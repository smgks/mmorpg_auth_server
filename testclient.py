import socket

conn = socket.socket()
conn.connect(("127.0.0.1", 7070))
conn.send(b"reg pohodu rabotaet")
data = b""
tmp = conn.recv(1024)
while tmp:
    data += tmp
    tmp = conn.recv(1024)
print( data.decode("utf-8") )
conn.close()
