#import stuff
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import *

app = Ursina()



#create a player
player = FirstPersonController(model = 'cube', collider = 'box', jump_height = 10, gravity = 0.1, speed = 10, health = 100, height = 5)  

#player.cursor.scale = 0.1
#create a floor and 2 walls
floor = Entity(collider = 'box',
               model = 'plane',
               scale = (100,1,100),
               texture = 'white_cube',
               texture_scale = (100,100),
               color = color.white.tint(-0.1),
               health = 10000000)

bot = Entity(model = 'cube',
    collider = 'box',
    scale = (2,4,2),
    color = color.yellow,
    position = (randint(1,20) ,1, randint(-50,50)),
    texture = 'white_cube',
    health = 2,
    visible = False)
e_gun = Entity(parent=bot, model='cube', color=color.gray, scale= (0.5,0.1,4), position=(0.3,0.0,-0.5), collider='box') 

wall = Entity(collider = 'box', model = 'cube',scale = (2,100,100),position = (50,0,0), texture = 'sky_sunset', health = 10000000)
wall2 = Entity(collider = 'box', model = 'cube',scale = (2,100,100),position = (-50,0,0), texture = 'sky_default', health = 100)

counter = 0
bullets = []
enemies = []
loaded = False
kill_count=0


bot_exists = False

def update():
    global counter, bullets, enemies,loaded, kill_count, bot_exists
    counter += 1

#BOT CREATION
    if player.health < 0:
        application.pause()
        mouse.locked = False
        Text(text = 'GAME OVER,KILL COUNT: '+str(kill_count), scale=2, origin=(0,0), background=True, color=color.blue)

    if counter == 1000:
        print('BOT CREATED')
        bot_exists = True
        bot.visible = True
    if bot_exists: 
        bot.look_at(player)
    if counter > 1000 and counter % 60==0:
        bot_bullet = Entity(model = 'cube',
                            collider = 'box',
                            scale = (0.3,0.3,0.3),
                            color = color.red,
                            rotation_y = bot.rotation_y,
                            position = bot.position + (0,-1,0),
                            speed = 5,
                            id = 'bot')  
        bot_bullet.look_at(player)                
        bullets.append(bot_bullet)
    
#enemy CREATION
    if counter % 300 == 0:
        loaded = True
        enemy = Entity(model = 'cube',
                collider = 'box',
                d_rot_y = 0,
                size = randint(1,5),
                color = color.yellow,
                position = (50 ,randint(10,30), randint(-50,50)),
                texture = 'reflection_map_3')
        enemy.scale = (enemy.size,enemy.size,enemy.size)
        enemy.dx = -0.2/enemy.size
        enemy.dy = (0.2/enemy.size)*uniform(-0.1,0.1)
        enemy.health = enemy.size*2 + 1
        enemies.append(enemy)

#BULLET HANDLING    
    for b in bullets:
        b_hit_info = b.intersects()
        b.position += b.forward*b.speed
        
        if b_hit_info.hit:
            if b_hit_info.entity in enemies or b_hit_info.entity == wall:
                b_hit_info.entity.health -= 1
        if b_hit_info.entity == player and b.id =='bot':
            player.health -= 2
            m = Text(text = 'HIT, HEALTH: '+str(player.health), scale=2, origin=(0,0), color=color.red)
            m.fade_out(0,1)
            if b in bullets:
                bullets.remove(b)
            destroy(b)
        elif b.x > 100 or b.x <-100 or b.z>100 or b.z<-100 or b.y >100 or b.y<-100:
            if b in bullets:
                bullets.remove(b)
            destroy(b, delay = 0.1)

#enemy MOVEMENT AND BULLET COLLISION
    for enemy in enemies:
        enemy.x += enemy.dx
        enemy.y += enemy.dy
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


#WHAT HAPPENDS WHEN YOU CLICK MOUSE LEFT
def input(key):
    global bullets, loaded

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
        
    if key == 'right mouse down' and loaded:
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
                        speed =10,
                        id = 'player')
            bullets.append(bullet)
        loaded = False

sky = Sky()         
app.run()

#HAppy day