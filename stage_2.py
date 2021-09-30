#import stuff
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import *

app = Ursina()



#create a player
player = FirstPersonController(model = 'cube', collider = 'box', jump_height = 10, gravity = 0.1, speed = 10, health = 100)

rifle_gun = Entity(parent=camera, model='sphere', color=color.black, origin_y=-0.5, scale= (0.2,0.5,2.5), position=(0,-1,2), collider='box')
shot_gun = Entity(parent=camera, model='cube', color=color.black, origin_y=-1, scale= (0.4,0.2,2), position=(0,-1,2), collider='box',visible=False)
        
#player.cursor.scale = 0.1
#create a floor and 2 walls
floor = Entity(collider = 'box',
               model = 'plane',
               scale = (100,1,100),
               texture = 'white_cube',
               texture_scale = (100,100),
               color = color.white.tint(-0.1),
               health = 10000000)
wall = Entity(collider = 'box', model = 'cube',scale = (2,100,100),position = (50,0,0), texture = 'sky_sunset', health = 10000000)
wall2 = Entity(collider = 'box', model = 'cube',scale = (2,100,100),position = (-50,0,0), texture = 'sky_default', health = 100)

counter = 0
bullets = []
enemies = []
loaded = False
kill_count=0

def update():
    global counter, bullets, enemies,loaded,kill_count
    counter += 1

#enemy CREATION
    if counter % 300 == 0:
        loaded = True
        enemy = Entity(model = 'cube',
                collider = 'box',
                d_rot_y = 0,
                size = randint(1,5),
                color = color.yellow,
                position = (50 ,randint(1,20), randint(-50,50)),
                texture = 'reflection_map_3')
        enemy.scale = (enemy.size,enemy.size,enemy.size)
        enemy.dx = -0.2/enemy.size
        enemy.health = enemy.size*2 + 1
        enemies.append(enemy)

#BULLET HANDLING    
    for b in bullets:
        b_hit_info = b.intersects()
        b.position += b.forward*b.speed
        
        if b_hit_info.hit:
            if b_hit_info.entity in enemies or b_hit_info.entity == wall:
                
                b_hit_info.entity.health -= 1
            elif b_hit_info.entity in bullets:
                pass
            else:
                bullets.remove(b)
                destroy(b, delay = 0.1)
        if b.x > 100 or b.x <-100 or b.z>100 or b.z<-100 or b.y >100 or b.y<-100:
            if b in bullets:
                bullets.remove(b)
            destroy(b, delay = 0.1)
            

#enemy MOVEMENT AND BULLET COLLISION
    for enemy in enemies:
        ob_hit = enemy.intersects()
        enemy.x += enemy.dx
        if enemy.health <= 2:
            enemy.color =  color.yellow.tint(-0.5)
            enemy.dx = 0
            enemy.rotation_x +=1
            enemy.rotation_y +=1
            enemy.rotation_z +=1
        if enemy.health < 0:
            Animation('assets/explosion', position=enemy.position,
                scale=enemy.size*3, fps=15,loop=False, autoplay=True,rotation_x = player.rotation_x,rotation_y = player.rotation_y,
                    rotation_z = player.rotation_z,)

            enemies.remove(enemy)
            destroy(enemy)
            kill_count+=1
            killdown(kill_count)
            
          
#FREEZE AND EXIT WHEN YOU PRESS C            
    if held_keys['c']:
        application.pause()
        mouse.locked = False
        Text(text = 'Kill Count: '+str(kill_count), scale=2, origin=(0,0), background=True, color=color.blue)
        
    if held_keys['e']:
        player.y += 0.5

def killdown(kill_count):
    if len(str(kill_count)) == 1: counter = 'Kill Count: '+ '00' + str(kill_count)
    if len(str(kill_count)) == 2: counter = 'Kill Count: '+ '0' + str(kill_count)
    if len(str(kill_count)) == 3: counter = 'Kill Count: ' + str(kill_count)
    count = Text(text = counter, origin=(4.65,-18.3),color=color.white, background=True)
    count.fade_out(0,2.5)
    
#WHAT HAPPENDS WHEN YOU CLICK MOUSE LEFT
def input(key):
    global bullets, loaded

    if key == 'left mouse down':
        shot_gun.visible = False
        rifle_gun.visible = True
        bullet = Entity(
                    model = 'cube',
                    collider = 'box',
                    scale = (0.1,0.1,0.1),
                    color = color.green,
                    rotation_x = player.camera_pivot.rotation_x,
                    rotation_y = player.rotation_y,
                    rotation_z = player.rotation_z,
                    x = player.x,
                    y = player.y+1.9,
                    z = player.z,
                    speed = 25)
        bullets.append(bullet)
        

   

    if key == 'right mouse down' and loaded:
        shot_gun.visible=True
        rifle_gun.visible = False
        for i in range(0,20):
            bullet = Entity(
                        model = 'cube',
                        collider = 'box',
                        scale = (0.1,0.1,0.1),
                        color = color.green,
                        rotation_x = uniform(-2,2) + player.camera_pivot.rotation_x,
                        rotation_y = uniform(-2,2) + player.rotation_y,
                        rotation_z = uniform(-2,2) + player.rotation_z,
                        x = player.x ,
                        y = player.y+ 1.9,
                        z = player.z,
                        speed =10)
            bullets.append(bullet)
        loaded = False
         
sky = Sky()         
app.run()

#HAppy day