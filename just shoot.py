from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
#create a player
player = FirstPersonController(model = 'cube', collider = 'box', jump_height = 3, gravity = 0.5, speed = 5, health = 100)
floor = Entity(collider = 'box',model = 'plane',scale = (100,1,100),texture = 'white_cube',texture_scale = (100,100),color = color.white.tint(-0.1))
bullets = []

def update():
    global bullets
    print(print(player.camera_pivot.rotation_x))
#BULLET HANDLING    
    for b in bullets:
        b.position += b.forward*5
     
#WHAT HAPPENDS WHEN YOU CLICK MOUSE LEFT
def input(key):
    global bullets
    if key == 'left mouse down':
        bullet = Entity(model = 'cube',
                        collider = 'box',
                        scale = (0.2,0.2,0.2),
                        color = color.green,
                        rotation_y = player.rotation_y,
                        rotation_x = player.camera_pivot.rotation_x,
                        x = player.x,
                        y = player.y + 1,
                        z = player.z)
        bullets.append(bullet)
         
app.run()