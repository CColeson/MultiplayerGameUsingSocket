import pyglet
from GameObjects import GameObject
from pyglet.window import key
from pyglet.gl import glTranslatef
class MyPlayer(GameObject):

    def __init__(self,name,x,y,keys,**kwargs):
        image = 'GameObjects/Player/player.png'
        super().__init__(name,x,y,image)

        self.name = name
        self.moveSpeed = 10
        self.keys = keys


    def _movement(self,keys):
        '''moves the players sprite'''
        
        if keys[key.D]:
            self.x += self.moveSpeed
            pyglet.gl.glTranslatef(-self.moveSpeed,0,0)
        if keys[key.A]:
            self.x -= self.moveSpeed
            pyglet.gl.glTranslatef(self.moveSpeed,0,0)
        if keys[key.W]:
            self.y += self.moveSpeed
            pyglet.gl.glTranslatef(0,-self.moveSpeed,0)
        if keys[key.S]:
            self.y -= self.moveSpeed
            pyglet.gl.glTranslatef(0,self.moveSpeed,0)

            
    def _drawSelf(self):
        '''deprecated, instead draw the batch inherited by the superclass'''
        self._movement(self.keys)
        self._updateSprite()
        self.sprite.draw()

    def drawSelf(self):
        self._movement(self.keys)
        self._updateSprite()
        self.batch.draw()

class ServerPlayer:
    #players given to the client by the server
    def __init__(self,name,x,y,imagePath):
        self.name = name
        self.x = x
        self.y = y
        self.imagePath = imagePath

