import socket
import pyglet
from GameObjects.Player import Player
from pyglet.window import key
from pyglet.window import mouse


def createConnection():
    name = input('Enter your name\n')

    HOST = '192.168.1.98'
    PORT = 50007
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    s.send(bytes((name+' WANTS TO CONNECT').encode()))

    accepted = 0
    while accepted == 0:
        r = s.recv(1024).decode()
        if r == 'ACCEPTED':
            accepted = 1
        if r == 'REFUSED':
            accepted = -1
            
        r = None

    if accepted == -1:
        input("Please choose a different name and try again")
        exit()

    print("Connected Successfully")

    return name,s

def updateDrawList(recieved):
    global drawList
    recieved = recieved.split('\n')
    for i in recieved:
        i = i[3:].split()
        if len(i) != 0 and i[0] != name:
            if i[0] in drawList:
                drawList[i[0]].x = int(i[1])
                drawList[i[0]].y = int(i[2])
            else:
                drawList[i[0]] = Player(int(i[1]),int(i[2]),'GameObjects/Player/player.png',i[0],keys)

    
if __name__ == "__main__":
    
    name,s = createConnection()

    window = pyglet.window.Window(height=1000,width=1000)
    keys = key.KeyStateHandler()
    window.push_handlers(keys)
    
    drawList = {}
    drawList[name] = Player(0,0,'GameObjects/Player/player.png',name,keys)
    myPlayer = drawList[name]
    

    def update(time):
        global drawList
        window.clear()

        rec = str(s.recv(1024).decode('utf-8'))

        if rec[0:2] =='01':
           updateDrawList(rec)
                        
        for i in drawList:
            drawList[i].drawSelf()
        s.send(('02 %s %s %s'%(myPlayer.name,myPlayer.x,myPlayer.y)).encode())
            
    pyglet.clock.schedule_interval(update,1/60)#1/60
    pyglet.app.run()
    s.close()
        
    
