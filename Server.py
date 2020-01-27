import socket
import _thread
from GameObjects.ServerObject import ServerObject
import random
import time

def sendShit(conn):
    pos = ''
    for j in playerList:
        i = playerList[j]
        pos += '01 %s %s %s\n'%(i.name,i.x,i.y)
    conn.send(pos.encode())

def wantsConnection(conn,msg):
    global playerList
    name = msg.split()[0]
    if name in playerList:
        conn.send(b"REFUSED")
        return False
    else:
        conn.send(b"ACCEPTED")
        playerList[name] = ServerObject(random.randrange(0,1000),
                                        random.randrange(0,1000),name)
def updatePlayerList(msg):
    global playerList
    msg = msg[3:].split()
    if len(msg) != 0:
        playerList[msg[0]].x = int(msg[1])
        playerList[msg[0]].y = int(msg[2])
    
def onNewClient(conn,addr):
    name = ''
    while True:
  
        msg = conn.recv(1024).decode()
        if 'WANTS TO CONNECT' in msg:
            m = wantsConnection(conn,msg)
            if m == False: break
        if msg[0:2] == '02':
            updatePlayerList(msg)
        msg = None
        
        sendShit(conn)
        
    conn.close()
    del playerList[name]

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

playerList = {}

s.bind ((HOST, PORT))
s.listen()


while True:
    conn,addr = s.accept()
    _thread.start_new_thread(onNewClient,(conn,addr))

    data = None
            
            
