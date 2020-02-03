import pyglet

class GameObject:

    def __init__(self,name,x,y,image,drawLabels=False,group=None):

        self.name = name
        
        self.imagePath = image
        self.image = pyglet.image.load(image) #image representing the gameobject in the room

        self.image.anchor_x = self.image.width // 2 #anchors the image by its center
        self.image.anchor_y = self.image.height // 2

        self.width = self.image.width
        self.height = self.image.height

        self.x = int(x)
        self.y = int(y)

        self.batch = pyglet.graphics.Batch()

        self.sprite = pyglet.sprite.Sprite(self.image,self.x,self.y,group=group,batch=self.batch)

        self.label = None
        if drawLabels == True:
            self.label = pyglet.text.Label(name,
                                           font_size=24,
                                           x = self.x,
                                           y = self.y + self.height + 10,
                                           anchor_x='center',anchor_y='center',
                                           batch = self.batch)
    def _drawSelf(self):
        ''' deprecated as now the game will use batches;
            but could still be used'''
        self._updateSprite()
        self.sprite.draw()

    def drawSelf(self):
        self._updateSprite()
        self.batch.draw()

    def _updateSprite(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        if self.label != None:
            self.label.x = self.x
            self.label.y = self.y + self.height + 10
