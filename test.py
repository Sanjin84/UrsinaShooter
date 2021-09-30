from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
#create a player
player = FirstPersonController(model = 'cube',collider = 'box')

floor = Entity(collider = 'box',
               model = 'plane',
               scale = (100,1,100),
               texture = 'white_cube',
               texture_scale = (100,100),
               color = color.white.tint(-0.1))

app.run()