import socket
import pyglet
from GameObjects.Player import MyPlayer
from GameObjects import GameObject
from pyglet.window import key
from pyglet.window import mouse
import pickle
import random

def connect():
    name = input('Enter your name: a unique one may be assigned\n')

    s = socket.socket()
    s.connect((HOST,PORT))
    s.send(('00 '+name).encode())

    name = s.recv(1024).decode()
    if name[0:2] == '00':
        name = name[3:]
        print('Connected Successfully as %s!'%name)
    else:
        input('Something went wrong, press "enter" to try again')
        s,name = connect()

    return s,name

if __name__ == '__main__':
    
    HOST = 'ENTER YOUR IP HERE'
    PORT = 50007
    s,name = connect()

    window = pyglet.window.Window(height=1000,width=1000)
    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    player = MyPlayer(name,random.randrange(1000),random.randrange(1000),keys)
    #s.send(('01 %s %s %s %s'%(player.name,player.x,player.y,player.imagePath)).encode())

    drawObjects = {}
    
    def update(time):
        window.clear()

        msg = s.recv(1024).decode()
        if msg[0:2] == '01':
            msg = msg[3:]
            obs = msg.split('\n')
            for o in obs:
                o = o.split()
                if len(o) == 0: continue
                if o[0] not in drawObjects:
                    drawObjects[o[0]] = GameObject(o[0],int(o[1]),int(o[2]),o[3],drawLabels=True)
                else:
                    obj = drawObjects[o[0]]
                    obj.x = int(o[1])
                    obj.y = int(o[2])
                    obj.imagePath = o[3]
                
                
        player.drawSelf()
        
        for i in drawObjects:
            if drawObjects[i].name != player.name:
                drawObjects[i].drawSelf()

        msg = ('01 %s %s %s %s'%(player.name,player.x,player.y,player.imagePath)).encode()
        s.send(msg)

    pyglet.clock.schedule_interval(update,1/60)#1/60
    pyglet.app.run()
    s.close()
