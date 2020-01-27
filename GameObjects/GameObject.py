import pyglet
class GameObject:
    
    def __init__(self,x,y,image):
        
        self.image = pyglet.image.load(image)
        
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        self.width = self.image.width
        self.height = self.image.height
        
        self.x = x
        self.y = y

        self.sprite = pyglet.sprite.Sprite(self.image,self.x,self.y)

    def drawSelf(self):
        self._updateSprite()
        self.sprite.draw()

    def _updateSprite(self):
        self.sprite.x = self.x
        self.sprite.y = self.y

        
        
