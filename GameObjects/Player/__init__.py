import pyglet
from GameObjects import GameObject
from pyglet.window import key

class Player(GameObject.GameObject):

    def __init__(self,x,y,image,name,keys,**kwargs):
        super().__init__(x,y,image)

        self.name = name
        self.moveSpeed = 10

        self.keys = keys

    def _movement(self,keys):
        '''moves the players sprite'''
        if keys[key.D]:
            self.x += self.moveSpeed
        if keys[key.A]:
            self.x -= self.moveSpeed
        if keys[key.W]:
            self.y += self.moveSpeed
        if keys[key.S]:
            self.y -= self.moveSpeed


    def drawSelf(self):
        self._movement(self.keys)
        self._updateSprite()
        self.sprite.draw()
        
    
