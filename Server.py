import socket
import threading
import random
from GameObjects.Player import ServerPlayer
import pickle

def addToList(msg):
    global objectList
    name = msg[3:]
    while name in objectList: #while the name is not unique
        #add a random string to the end of the name to ensure uniqueness (its either this or hashing)
        name += '_' + str(random.randrange(100,200))
        
    objectList[name] = ServerPlayer(name,0,0,'GameObjects/Player/player.png')#TODO: Server representation of object, or game representation, that way it could be pickled
    conn.send(("00 "+name).encode())
    return name

def recievePlayerObject(msg):
    global objectList

    player = msg[3:].split(' ')
    player = ServerPlayer(player[0],player[1],player[2],player[3])
    objectList[player.name] = player

def onClientConnect(conn,addr,threadIndex):
    name = '' #unique client name
    connected = True
    while connected:

        try:
            msg = conn.recv(1024).decode()
        except:
            connected = False

        if msg[0:2] == '00':
            name = addToList(msg)

        if msg[0:2] == '01':
            recievePlayerObject(msg)

        msg = '01 '
        for o in objectList:
            msg += '%s %s %s %s\n'%(objectList[o].name,objectList[o].x,
                                    objectList[o].y,objectList[o].imagePath)
        try:
            conn.send(msg.encode())
        except:
            connected = False
        
    conn.close()
    del objectList[name]
    threads.pop(threadIndex)
    print("%s disconnected"%name)






if __name__ == '__main__':
    HOST = ''
    PORT = 50007

    s = socket.socket()

    objectList = {} #list of connected players

    s.bind((HOST,PORT))
    s.listen()

    threads = []#thread list, stores all connections to server
    threadIndex = 0
    while True:
        conn,addr = s.accept()
        t = threading.Thread(target=onClientConnect,args=(conn,addr,threadIndex))
        t.start()
        threads.append(t)
        threadIndex += 1
