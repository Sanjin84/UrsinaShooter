#import stuff
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import *

app = Ursina()



#create a player
player = FirstPersonController(model = 'cube', collider = 'box', jump_height = 10, gravity = 0.1, speed = 10, health = 100)

rifle_gun = Entity(parent=camera, model='cube', color=color.gray, origin_y=-0.5, scale= (0.5,0.5,2), position=(0,-1,2), collider='box')
shot_gun = Entity(parent=camera, model='cube', color=color.gray, origin_y=-0.5, scale= (1,0.2,2), position=(0,-1,2), collider='box',visible=False)
      

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

BOT = Entity(model = 'cube',
                collider = 'box',
                scale = (2,4,2),
                color = color.yellow,
                position = (randint(1,20) ,1, randint(-50,50)),
                texture = 'white_cube',
                health = 2)
e_gun = Entity(parent=BOT, model='cube', color=color.gray, scale= (0.5,0.1,2), position=(0.3,0.3,-0.5), collider='box') 



counter = 0
bullets = []
e_bullets=[]
enemies = []
loaded = False
kill_count=0




def update():
    global counter, bullets, enemies,loaded,kill_count
    counter += 1

#BOT CREATION
    BOT.rotation_x = player.rotation_x
    BOT.rotation_y = player.rotation_y
    BOT.rotation_z = player.rotation_z   
    
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
            if b_hit_info.entity in enemies or b_hit_info.entity == wall or b_hit_info.entity == BOT:
                
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

    for e in e_bullets:
        e_hit_info = e.intersects()
        e.position += e.back*e.speed
        if e_hit_info.hit:
            if e_hit_info.entity == player:
                print("hit")
                application.pause
          
        #destroy(e, delay = 2)
        

#enemy MOVEMENT AND BULLET COLLISION
    for enemy in enemies:
        enemy.x += enemy.dx
        if enemy.health <= 2:
            enemy.color =  color.yellow.tint(-0.5)
            enemy.dx = 0
            enemy.rotation_x +=1
            enemy.rotation_y +=1
            enemy.rotation_z +=1
        if enemy.health < 0:
            Animation('assets/explosion', position=enemy.position,
                scale=5, fps=15,loop=False, autoplay=True,rotation_x = player.rotation_x,rotation_y = player.rotation_y,
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
    count = Text(text = 'Kill Count: '+str(kill_count), origin=(4,-10),color=color.white)
    count.fade_out(0,2)

def shoot():
    e_bullet = Entity(
                        model = 'cube',
                        collider = 'box',
                        scale = (0.1,0.1,0.1),
                        color = color.red,
                        rotation_x = BOT.rotation_x,
                        rotation_y = BOT.rotation_y,
                        rotation_z = BOT.rotation_z,
                        x = BOT.x,
                        y = BOT.y+0.1,
                        z = BOT.z,
                        speed = 0.5)
    e_bullets.append(e_bullet)
    seq = invoke(shoot, delay=0.5)
    if mouse.locked == False:
        seq.kill()

shoot()

#WHAT HAPPENDS WHEN YOU CLICK MOUSE LEFT
def input(key):
    global bullets, loaded

    if key == '1':
        shot_gun.visible=False
        rifle_gun.visible = True
        player.rifle = rifle_gun
    if key == '2':
        rifle_gun.visible = False
        shot_gun.visible=True 
        

    if key == 'left mouse down':
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
        
       
   

    if key == 'right mouse down' and loaded and shot_gun.visible==True:
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

