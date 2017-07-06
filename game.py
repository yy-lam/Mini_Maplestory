import cocos, pyglet, constants, random
from cocos.layer import Layer, ScrollingManager, ScrollableLayer, ColorLayer
from cocos.sprite import Sprite
from cocos.actions import *
from cocos import mapcolliders
from cocos.particle_systems import *
from cocos.particle import *
from pyglet.window import key
from pyglet.window.key import symbol_string, KeyStateHandler
from pyglet.gl import glClearColor

       
class Player(Sprite):
    is_event_handler = True

    def __init__(self):
        
        super(Player, self).__init__(pyglet.image.load('Source/Boss1/stand_0.png'))
        self.rect = cocos.rect.Rect(0,0,21,150)
        self.rect.set_position((320, 740))
        self.anchor = self.rect.center
        self.position = self.rect.center
        # standing animation
        self.stand = []
        for i in range(8):
            image = pyglet.image.load('Source/Boss1/stand_%d.png' %i)
            self.stand.append(pyglet.image.AnimationFrame(image, 0.1))
        self.stand_left_anim = pyglet.image.Animation(self.stand)
        self.stand_right_anim = self.stand_left_anim.get_transform(flip_x=True)
        # walking animation
        self.move_left = []
        for i in range(8):
            image = pyglet.image.load('Source/Boss1/walk_%d.png' %i)
            self.move_left.append(pyglet.image.AnimationFrame(image, 0.1))
        self.move_left_anim = pyglet.image.Animation(self.move_left)
        self.move_right_anim = self.move_left_anim.get_transform(flip_x=True)
        # Jump
        self.jump_left_anim = pyglet.image.Animation([pyglet.image.AnimationFrame(
                         pyglet.image.load('Source/Boss1/jump_0.png'),1.5)]
                         )
        self.jump_right_anim = self.jump_left_anim.get_transform(flip_x=True)
        # Attack animation
        self.slash = []
        for i in range(1,17):
            image = pyglet.image.load('Source/Boss1/DKdragonSlash0_%d.png' %i)
            self.slash.append(pyglet.image.AnimationFrame(image, 0.12))
        self.slash_left_anim = pyglet.image.Animation(self.slash) 
        self.slash_right_anim = self.slash_left_anim.get_transform(flip_x=True)
        # set player's animation
        self.image = self.stand_left_anim

        #super(Player, self).__init__(self.anim)
        # Here is where the code starts to get different
        # Instead of text, I create a sprite object
        # Also unlike last time, I added the sprite to the object instead of making it local
        # This is useful if you want to access it in other functions, like I will show in the next tutorial
        # Then I add it to the layer, similar to the text
        
        # self.rect.center = (320, 240) = self.player.position
        self.jumping = False
        self.attacking = False
        self.direction = 'left'
        self.velocity = (0,0)
        self.on_ground = False
        self.move_speed = 300
        self.jump_speed = 500
        self.gravity = -800

        # Player's attributes
        self.hp = 200
        self.strength = 50
        
        
        # Attack Rect
        self.attack_rect = self.rect.copy()
        
        # And lastly I add it to the layer. Standard stuff   
    def on_ground(self):
        if self.direction == 'left':
            self.image = self.stand_left_anim
        else:
            self.image = self.stand_right_anim
    def update(self, dt):

        vx, vy = self.velocity
        vx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.move_speed
        
        vy += self.gravity * dt
        if self.on_ground and keyboard[key.S]:
            vy =  self.jump_speed
        # update velocity
        dx = vx * dt
        dy = vy * dt 
        last_rect = self.rect
        #last_rect = narrow(last_rect, 150)
        # build the tentative displaced rect
        new_rect = last_rect.copy()
        new_rect.x += dx
        new_rect.y += dy 


        #print("vx:", vx, "vy:", vy, "dx:", dx, "dy:", dy, "last:", last_rect,"new", new_rect)
        self.velocity = mapcollider.collide_map(platform, last_rect, 
                                                       new_rect, vx, vy)
        # account for hitting obstacles, which adjust new vx,vy
        self.rect = new_rect
        self.on_ground = (new_rect.y == last_rect.y)
        # Update player's attack rect
        if self.attacking:
            if self.direction == 'right':
                self.attack_rect = new_rect.copy()
                self.attack_rect.set_width(380)
            elif self.direction == 'left':
                self.attack_rect = new_rect.copy()
                self.attack_rect.set_width(380)
                self.attack_rect.x = new_rect.x -320
        self.position = new_rect.center
    
        #self.target.anchor = new_rect.center
        #print('position:', self.target.position, 'rect:', new_rect, 'anchor:', self.target.anchor)
        scroller.set_focus(*new_rect.center)

    def attack_reset(self):
        self.one_time_trigger1 = True
        self.one_time_trigger2 = True
        self.one_time_trigger3 = True
    def on_animation_end(self):
        if self.attacking:
            self.attacking = False
            self.image_anchor = (self.stand[0].image.width/2, 
                                   self.stand[0].image.height/2)
            
            self.attack_reset()
            #self.image_anchor = self.rect.midbottom
        if self.direction == 'left':
            self.image = self.stand_left_anim
        else:
            self.image = self.stand_right_anim
        self.attack_reset()

    def walk_right(self):
        self.direction = 'right'
        self.attacking = False
        self.attack_reset()
        self.image = self.move_right_anim
        self.image_anchor = (self.stand[0].image.width/2, 
                             self.stand[0].image.height/2)
    def walk_left(self):
        self.direction = 'left'
        self.attacking = False
        self.attack_reset()
        self.image = self.move_left_anim
        self.image_anchor = (self.stand[0].image.width/2, 
                             self.stand[0].image.height/2)

    def jump(self):
        self.attacking = False
        if self.direction == 'left':
            self.image = self.jump_left_anim
        elif self.direction == 'right':
            self.image = self.jump_right_anim

    def attack(self):
        if self.attacking == False:
            self.attacking = True
            if self.direction == 'left':
                self.image = self.slash_left_anim
                self.image_anchor = (400,156)
            else:
                self.image = self.slash_right_anim
                self.image_anchor = (150,158)

    def under_attack(self, diff):
    if self.one_time_trigger1:
        self.attacked = True
        hurt = int(diff*random.uniform(0.75,1.2))
        self.hp -= hurt
        # if self.hp <= 0:
        #     if self.direction == 'left':
        #         self.image = self.die_left_anim
        #     else:
        #         self.image = self.die_right_anim
        # else:
        #     if self.direction == 'left':
        #         self.image = self.hit_left_anim
        #     else:
        #         self.image = self.hit_right_anim
        (x, y) = (self.rect.center)
        hitpoint = HitPoint(hurt ,(x+25,y+60), False)
        self.parent.add(hitpoint, z=3)
        

        self.one_time_trigger1 = False


Player.register_event_type('on_ground')

        

class Monster(Sprite):
    """docstring for Monster"""
    def __init__(self):
        super(Monster, self).__init__(pyglet.image.load('Source/OrangeMushroom/stand_0.png'))
        self.move = []
        for i in range(3):
            image = pyglet.image.load('Source/OrangeMushroom/move_%d.png' %i)
            self.move.append(pyglet.image.AnimationFrame(image, 0.3))
        self.move_left_anim = pyglet.image.Animation(self.move)
        self.move_right_anim = self.move_left_anim.get_transform(flip_x=True)
        self.stand = []
        for i in range(3):
            image = pyglet.image.load('Source/OrangeMushroom/stand_%d.png' %i)
            self.stand.append(pyglet.image.AnimationFrame(image, 1))
        self.stand_left_anim = pyglet.image.Animation(self.stand)
        self.stand_right_anim = self.stand_left_anim.get_transform(flip_x=True)
        
        self.hit = pyglet.image.load('Source/OrangeMushroom/hit1_0.png')
        self.hit_left_anim = pyglet.image.Animation([pyglet.image.AnimationFrame(
                                                self.hit, 0.25)]
                                               )
        self.hit_right_anim = self.hit_left_anim.get_transform(flip_x=True)
        self.die = []
        for i in range(3):
            image = pyglet.image.load('Source/OrangeMushroom/die1_%d.png' %i)
            self.die.append(pyglet.image.AnimationFrame(image, 0.3))
        self.die_left_anim = pyglet.image.Animation(self.die)
        self.die_right_anim = self.die_left_anim.get_transform(flip_x=True)

        self.image = self.move_left_anim
        self.rect = cocos.rect.Rect(0,0,60,55)
        self.rect.set_position((random.randint(0,1240),300))
        self.position = self.rect.center
        self.velocity = (0,0)
        self.direction = 'left'
        # AI decision : idle = 0, , patrol = 1, pursuit =2 , hit = 3
        self.status = 'patrol'
        self.attacked = False
        
        self.dir_to_player = 0
        self.nextDecisionTime = 3
        self.m = 0
        self.M = 0
        self.N = 1
        self.on_ground = False
        self.move_speed = 50
        self.gravity = -800
        self.alert = False
        # Used for pursuing target
        self.one_time_trigger = False
        # Used for being attacked
        self.one_time_trigger1 = True
        # 
        self.one_time_trigger2 = True
        self.one_time_trigger3 = True

        self.hp = 300
        self.strength = 10
        self.dead = False
        self.active = False
        self.do(FadeIn(3))

    def under_attack(self, diff):
        if self.one_time_trigger1:
            print(True, 'hit')
            self.attacked = True
            self.alert = True
            self.status = 'attacked'
            hurt = int(diff*random.uniform(0.75,1.2))
            self.hp -= hurt
            if self.hp <= 0:
                if self.direction == 'left':
                    self.image = self.die_left_anim
                else:
                    self.image = self.die_right_anim
            else:
                if self.direction == 'left':
                    self.image = self.hit_left_anim
                else:
                    self.image = self.hit_right_anim
            (x, y) = (self.rect.center)
            hitpoint = HitPoint(hurt ,(x+25,y+60), True)
            self.parent.add(hitpoint, z=3)
            

            self.one_time_trigger1 = False

        

    def update(self, dt):
        self.on_ground = True
        self.move_speed = 50
        self.gravity = -800
        self.nextDecisionTime -= dt
        vx, vy = self.velocity
        self.N = 1
        #print(self.nextDecisionTime)


        # AI decision:
        
            # Patrol
        if self.status=='patrol'  and (not self.attacked):
            if self.nextDecisionTime < 0:
                self.m = random.randint(0,100)
                t = random.uniform(1,5)
                if self.m > 0 and self.m <= 25 :
                    self.M = 1
                    self.image = self.move_right_anim
                    self.nextDecisionTime = t
                elif self.m >= 75:
                    self.M = -1
                    self.image = self.move_left_anim
                    self.nextDecisionTime = t
                else:
                    self.M = 0
                    self.image = self.stand_right_anim
                    self.nextDecisionTime = t
            # Idle
        elif self.status == 'idle':
            self.M = 0

        elif self.status == 'pursuit':
            self.M = self.dir_to_player 
            if self.one_time_trigger or (self.direction=='left' 
                                         and self.dir_to_player==1) or (
                                         self.direction=='right' 
                                         and self.dir_to_player==-1):
                if self.dir_to_player == 1:
                    self.image = self.move_right_anim
                    self.direction = 'right'
                elif self.dir_to_player == -1:
                    self.image = self.move_left_anim
                    self.direction = 'left'
                self.one_time_trigger = False
        #print(self.M, self.status,'attacked?', self.attacked)

        # Stop moving when hit
        if self.attacked:
            self.M = 0
        vx = self.move_speed * self.M
        vy += self.gravity * dt
        dx = vx * dt
        dy = vy * dt
        last_rect = self.rect
        new_rect = last_rect.copy()
        new_rect.x += dx
        new_rect.y += dy 
        self.velocity = mapcollider.collide_map(platform, last_rect, 
                                                       new_rect, vx, vy)
        if new_rect.left < 0 or new_rect.right > 1240:
            new_rect.x -= dx
        self.rect = new_rect
        self.position = new_rect.center
    def on_animation_end(self):
        if self.attacked:
            if self.direction == 'left':
                self.image = self.stand_left_anim
            else:
                self.image = self.stand_right_anim
            #self.status = 'idle'
            self.attacked = False
            self.one_time_trigger = True
            self.one_time_trigger1 = True
            if self.hp <= 0:
                self.dead = True

class HitPoint(cocos.batch.BatchableNode):
    """docstring for HitPoint"""
    def __init__(self, num, pos, is_player):
        super(HitPoint, self).__init__()
        self.Red = []
        self.Violet = []
        self.hitNum = []
        for i in range(10):
            image = pyglet.image.load('Source/number/NoRed1_%d.png' %i)
            self.Red.append(image)
        for i in range(10):
            image = pyglet.image.load('Source/number/NoRed1_%d.png' %i)
            self.Red.append(image)
        x, y = pos

        while num > 0:
            n = num%10
            if is_player == True:
                digit = Sprite(self.Red[n])
            else:
                digit = Sprite(self.Violet[n])
            digit.position = (x, y)

            self.add(digit)
            digit.do((MoveBy((0, 25), duration = 1) | FadeOut(1)) + 
                     CallFunc(self.kill))
            x -= 37
            num = num // 10


    # def draw(self):
    #     for i in self.hitNum:
    #         i.blit(100,100, 100)

        


class Level1(ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super(Level1, self).__init__()

        text = cocos.text.Label("Mini MapleStory", anchor_x='center',
                                anchor_y='center')
        text.position = (cocos.director.director._window_virtual_width/2, 
                        cocos.director.director._window_virtual_height/2)
        image = pyglet.resource.image('bg/henesys.png')
        bg = Sprite(image)
        bg.image_anchor = (0,-68)
        bg.scale_x = 1.34
        
        self.add(bg)
        self.add(text)

# def narrow(rect, delta):
#     left = rect.get_left()
#     width = rect.get_right() - rect.get_left()
#     bottom = rect.get_bottom()
#     height = rect.get_top() - rect.get_bottom()
#     left += delta
#     width -= 2*delta
#     return cocos.rect.Rect(left, bottom, width, height)
class GameLayer(ScrollableLayer):
    """docstring for GameLayer"""
    is_event_handler = True
    def __init__(self):
        super(GameLayer, self).__init__()
        self.monster_batch = cocos.batch.BatchNode()
        self.add(self.monster_batch)
        for n in range(20):
            self.monster_batch.add(Monster())
        self.player = Player()
        self.add(self.player)
        self.L = Meteor()
        self.L.size = 45.0
        self.L.speed = 10
        self.L.tangential_accel = 30
        self.L.gravity = Point2(0.00, 0.00)
        self.add(self.L)
        #self.player.do(PlayerAction())
        #self.monster_action = MonsterAction()
        #self.monster.do(self.monster_action)
        self.schedule(self.update)
    def collision_detect(self, A, B):
        if A.right < B.left or A.left > B.right or A.top < B.bottom or A.bottom > B.top:
            return False
        else:
            return True
    def distance(self, A, B):
        distance = A.rect.center[0] - B.rect.center[0]
        if distance < 0:
            distance *= -1
        return distance
                         
    def update(self, dt):
        self.player.update(dt)
        self.L.position = self.player.position
        for (z, monster) in self.monster_batch.children:
            if isinstance(monster, Monster):
                if monster.dead:
                    monster.kill()
                monster.update(dt)   
                if self.collision_detect(self.player.attack_rect, 
                                         monster.rect) and self.player.attacking:
                    strength_diff = self.player.strength - monster.strength
                    if self.player._frame_index == 3:
                        monster.under_attack(strength_diff)
                    elif self.player._frame_index == 7:
                        monster.under_attack(strength_diff)
                    elif self.player._frame_index == 15:
                        monster.under_attack(strength_diff)
                if monster.alert:

                    distance = self.distance(self.player, monster)
                    if distance < 500 and distance > 30:    
                        n = int(self.player.rect.center[0] > monster.rect.center[0])
                        if n == 0:
                            n = -1
                        elif n == 1:
                            n = 1
                        monster.dir_to_player = n
                        monster.status = 'pursuit'
                    # elif self.distance(self.player, monster) < 30:
                    #     monster.status = 'idle'
                    # elif distance <= 30:
                    #     monster.status = 'idle'
                    else:
                        monster.status = 'patrol'

        #print(self.monster.status)

    

        


if __name__ == "__main__":
    global keyboard, scroller
    cocos.director.director.init(width=constants.SCREEN_WIDTH, 
        height=constants.SCREEN_HEIGHT, fullscreen=False, resizable=True)
    mapcollider = mapcolliders.RectMapCollider(velocity_on_bump='slide')
    maploaded = cocos.tiles.load_tmx('maploaded2.tmx')
    platform = maploaded['platform']
    level1 = Level1()
    gamelayer = GameLayer()

    scroller = ScrollingManager()
    
    #scroller.add(level1)
    scroller.add(platform)
    
    
    scroller.add(gamelayer)
    main_scene = cocos.scene.Scene()
    scroller.set_focus(gamelayer.player.position[0], gamelayer.player.position[1])

    #main_scene.add(level1, z=0)
    #main_scene.add(ColorLayer(0, 0, 0, 0), z=0)
    main_scene.add(scroller, z=1)
    main_scene.add(level1, z=0)
    keyboard = KeyStateHandler()
    cocos.director.director.window.push_handlers(keyboard)
    def on_key_press(key, modifier):
        if symbol_string(key) == "EXIT":
            pyglet.app.exit()
        if symbol_string(key) == 'RIGHT':
            gamelayer.player.walk_right()
        if symbol_string(key) == 'LEFT':
            gamelayer.player.walk_left()
        if symbol_string(key) == 'S':
            gamelayer.player.jump()
        if symbol_string(key) == 'A':
            gamelayer.player.attack()
     
        if symbol_string(key) == 'R':
            gamelayer.player.rect.set_center((300,400))

                # player.rect.right = 
                #player.image_anchor = player.position
    # Update
    #pyglet.clock.schedule(gamelayer.check_attack)
    cocos.director.director.window.push_handlers(on_key_press)
    cocos.director.director.run(main_scene)
