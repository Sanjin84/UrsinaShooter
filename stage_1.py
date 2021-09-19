#import stuff
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import *

app = Ursina()

#create a player
player = FirstPersonController(model = 'cube', collider = 'box', jump_height = 3, gravity = 0.5, speed = 5, health = 100)
#player.cursor.scale = 0.1
#create a floor and 2 walls
floor = Entity(collider = 'box',
               model = 'plane',
               scale = (100,1,100),
               texture = 'white_cube',
               texture_scale = (100,100),
               color = color.white.tint(-0.1),
               health = 10000000)
wall = Entity(collider = 'box', model = 'cube',scale = (2,100,100),position = (50,0,0),
              texture = 'brick',texture_scale = (50,50),color = color.gray, health = 10000000)
wall2 = Entity(collider = 'box', model = 'cube',scale = (2,100,100),position = (-50,0,0),
              texture = 'brick',texture_scale = (50,50),color = color.gray, health = 10000000)

counter = 0
bullets = []
obstacles = []


def update():
    global counter, bullets, obstacles
    counter += 1
    
#OBSTACLE CREATION
    if counter % 100 == 0:
        obstacle = Entity(model = 'cube',
                collider = 'box',
                scale = (2,2,2),
                color = color.yellow,
                position = (50 ,randint(1,3), randint(-50,50)),
                dz = 0, dx = -0.02,
                texture = 'brick',
                health = 1)
        obstacles.append(obstacle)

#BULLET HANDLING    
    for b in bullets:
        b_hit_info = b.intersects()
        b.position += b.forward*5
        
        if b_hit_info.hit:
            if b_hit_info.entity in obstacles or b_hit_info.entity == wall:
                b_hit_info.entity.health -= 1
            bullets.remove(b)
            destroy(b, delay = 0.1)

#OBSTACLE MOVEMENT AND BULLET COLLISION
    for obstacle in obstacles:
        ob_hit = obstacle.intersects()
        obstacle.x += obstacle.dx
        if obstacle.health <= 0:
            obstacle.color =  color.yellow.tint(-0.5)
            obstacle.dx = 0
        if obstacle.health < 0:
            obstacles.remove(obstacle)
            destroy(obstacle)
            
#FREEZE AND EXIT WHEN YOU PRESS C            
    if held_keys['c']:
        application.pause()
        mouse.locked = False
        

#WHAT HAPPENDS WHEN YOU CLICK MOUSE LEFT
def input(key):
    global bullets
    if key == 'left mouse down':
        bullet = Entity(model = 'cube',
                    collider = 'box',
                    scale = (0.1,0.1,0.1),
                    color = color.green,
                    rotation_x = player.camera_pivot.rotation_x,
                    rotation_y = player.rotation_y,
                    rotation_z = player.rotation_z,
                    x = player.x,
                    y = player.y+1.9,
                    z = player.z)
        bullets.append(bullet)
         
app.run()