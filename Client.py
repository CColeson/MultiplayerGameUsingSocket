import socket
import pyglet
from GameObjects.Player import MyPlayer
from GameObjects import GameObject
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import glTranslatef,glScalef
import pickle
import random

def connect():
    n = input('Enter your name: a unique one may be assigned, \ninvalid characters will be removed.\n')
    n = n.split(' ')
    name = ''
    for i in n:
        name += i
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

def moveCams():
    global moveCam
    camX = window.width // 2
    camY = window.height // 2
    if moveCam == True:
        while camX != player.x:
            #print("moving camx")
            if player.x < camX:
                camX -= 1
                glTranslatef(1,0,0)
            else:
                camX += 1
                glTranslatef(-1,0,0)
            
        while camY != player.y:
            #print("moving camy")
            if player.y < camY:
                camY -= 1
                glTranslatef(0,1,0)
            else:
                camY += 1
                glTranslatef(0,-1,0)
        #print("Done")
        moveCam = False

def addToList(msg):
    global drawObjects
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

def deleteFromList(msg):
    global drawObjects
    msg = msg[3:]
    del drawObjects[msg]

def update(time):
    window.clear()
    
    moveCams()

    msg = s.recv(1024).decode()
    if msg[0:2] == '01':
        addToList(msg)
            
    player.drawSelf()
    
    for i in drawObjects:
        if drawObjects[i].name != player.name:
            drawObjects[i].drawSelf()

    msg = ('01 %s %s %s %s'%(player.name,player.x,player.y,player.imagePath)).encode()
    s.send(msg)

if __name__ == '__main__':

    currMouseScrollY = 0
    
    
    
    HOST = 'HOST'
    PORT = 50007
    s,name = connect()

    window = pyglet.window.Window(height=1000,width=1000)
    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    player = MyPlayer(name,random.randrange(1000),random.randrange(1000),keys)
    print("x: %s y: %s"%(player.x,player.y))
    moveCam = True
    

    drawObjects = {}

    pyglet.clock.schedule_interval(update,1/60)#1/60
    pyglet.app.run()
    s.close()
