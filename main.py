import pyglet
from GameObjects.Player import Player

window = pyglet.window.Window(height=1000,width=1000)
player = Player(100,100,'GameObjects/Player/player.png')

def update(time):
    window.clear()
    player.drawSelf()


pyglet.clock.schedule_interval(update,1/120)
pyglet.app.run()
    
