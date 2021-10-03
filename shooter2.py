from ursina import *
from random import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

#Build a floor
floor = Entity(collider = 'box',
               model = 'plane',
               scale = (100,1,100),
               color = color.white.tint(-0.1),
               texture = 'grass',
               texture_scale = (100,100))

#Create a First person controller (player)
player = FirstPersonController(model ='cube', gravity = 0.1, jump_height = 10)


target = Entity(model = 'sphere',
                collider = 'sphere',
                position = (100, randint(25,50),randint(-100,100)),
                scale = 5,
                color = color.yellow,
                dy = 0, dz = 0)

#create a candle that indicates time
candle = Entity(model = 'cube',
                collider = 'box',
                position = (50,10,50),
                scale = (1,20,1),
                color = color.yellow.tint(-0.3),)

loaded = False

#shot gun or sniper (long fast bullet)

#print out score on the screen

#add time when target hit, make bullets cost time

#LISTS:
bullets = []
frame_counter = 0
score = 0
bullet_counter = 0
gun = 'rifle'

def update():
    global frame_counter,score, bullet_counter, gun, loaded
    candle.y -= 0.01
    target.z += target.dz
    target.y += target.dy
    
    frame_counter += 1
    if frame_counter % 120 == 0:
        loaded = True
    if candle.y < -10:
        application.pause()
        mouse.locked = False
        
        
    for b in bullets:
        if gun == 'rifle':b.position += b.forward*13
        if gun == 'sniper':b.position += b.forward*30
        if gun == 'shotgun':b.position += b.forward*7
        if b.x > 180:
            if b in bullets:
                bullets.remove(b)
                destroy(b)
        
    t_col = target.intersects()
    if t_col.hit:
        target.position = (100, randint(25,50),randint(-25,25))
        score += 1
        target.dz = uniform(-0.2,0.2)
        target.dy = uniform(-0.2,0.2)
        text = Text(text = 'SCORE:'+str(score), origin=(4.65,-18.3))
        text.fade_out(0,2)
        #play around with these numbers
    if held_keys['1']:
        gun = 'rifle'
        camera.fov = 90
    if held_keys['2']:
        gun = 'sniper'
        camera.fov = 50
    if held_keys['3']:
        gun = 'shotgun'
        camera.fov = 90


#spawn bullets when we press left mouse
def input(key):
    global bullet_counter, rifle, loaded
    if key == 'left mouse down' and gun == 'rifle':
        bullet = Entity(model = 'sphere',
                        collider = 'sphere',
                        scale = (0.2,0.2,0.2),
                        color = color.black,
                        position = player.position + (0,1.8,0),
                        rotation_x = player.camera_pivot.rotation_x,
                        rotation_y = player.rotation_y)
        bullets.append(bullet)
        bullet_counter +=1
       #your task is to modify bullet to be elongated int the right direction
    if key == 'left mouse down' and gun == 'sniper':
        for i in range(5):
            bullet = Entity(model = 'cube',
                            collider = 'box',
                            scale = (0.2,0.2,0.2),
                            color = color.black,
                            position = player.position + player.camera_pivot.forward*i,
                            rotation_x = player.camera_pivot.rotation_x,
                            rotation_y = player.rotation_y)
            bullets.append(bullet)
        bullet_counter +=1
    if key == 'left mouse down' and gun == 'shotgun' and loaded == True:
        for i in range(15):
            bullet = Entity(model = 'sphere',
                            collider = 'sphere',
                            scale = (0.2,0.2,0.2),
                            color = color.black,
                            position = player.position + (0,1.8,0),
                            rotation_x = player.camera_pivot.rotation_x + uniform(-2,2), 
                            rotation_y = player.rotation_y + uniform(-2,2))
            bullets.append(bullet)
        loaded = False
        bullet_counter +=1
    if key == 'c':
        application.pause()
        mouse.locked = False

sky = Sky()
sky.texture = 'sky_sunset'
sky.color = color.cyan


app.run()