import cocos, pyglet, constants
from cocos.layer import Layer, ScrollingManager, ScrollableLayer, ColorLayer
from cocos.sprite import Sprite
from cocos.actions import MoveTo, MoveBy, JumpBy
from cocos import mapcolliders
from pyglet.window import key
from pyglet.window.key import symbol_string, KeyStateHandler

class PlayerAction(cocos.actions.Action):

    """docstring for PlayerAction"""
    def __init__(self):
        super(PlayerAction, self).__init__()
        self.on_ground = True
        self.move_speed = 200
        self.jump_speed = 200
        self.gravity = 0
    def start(self):
        self.target.velocity = (0,0)

    def step(self, dt):
        super(PlayerAction, self).step(dt)
        vx, vy = self.target.velocity
        vx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.move_speed
        vy = (keyboard[key.UP] - keyboard[key.DOWN]) * self.jump_speed
        vy += self.gravity * dt
        # update velocity
        dx = vx * dt
        dy = vy * dt 
        last_rect = self.target.rect
        #last_rect = narrow(last_rect, 150)
        # build the tentative displaced rect
        new_rect = last_rect.copy()
        new_rect.x += dx
        new_rect.y += dy 
        # account for hitting obstacles, which adjust new vx,vy
        self.target.position = new_rect.center
        self.target.rect = new_rect
        #scroller.set_focus(*new_rect.center)
        #scroller.set_focus(self.target.x, self.target.y)
            

class Player(Sprite):
    is_event_handler = True
    def __init__(self):
        super(Player, self).__init__(pyglet.image.load('Source/OrangeMushroom/stand_0.png'))
        self.move = []
        for i in range(3):
            image = pyglet.image.load('Source/OrangeMushroom/move_%d.png' %i)
            self.move.append(pyglet.image.AnimationFrame(image, 0.25))
        self.move_left_anim = pyglet.image.Animation(self.move)
        self.move_right_anim = self.move_left_anim.get_transform(flip_x=True)
        self.stand = []
        for i in range(3):
            image = pyglet.image.load('Source/OrangeMushroom/stand_%d.png' %i)
            self.stand.append(pyglet.image.AnimationFrame(image, 1))
        self.stand_left_anim = pyglet.image.Animation(self.stand)
        self.stand_right_anim = self.stand_left_anim.get_transform(flip_x=True)
        
        self.hit = pyglet.image.load('Source/OrangeMushroom/hit1_0.png')
        self.hit_anim = pyglet.image.Animation([pyglet.image.AnimationFrame(
                                                self.hit, 0.25)]
                                               )

        self.image = self.stand_left_anim
        # Here is where the code starts to get different
        # Instead of text, I create a sprite object
        # Also unlike last time, I added the sprite to the object instead of making it local
        # This is useful if you want to access it in other functions, like I will show in the next tutorial
        # Then I add it to the layer, similar to the text
        self.velocity = (0,0)
        self.position = 320, 240
        self.rect = cocos.rect.Rect(0,0,60,55)        
        # self.rect.center = (320, 240) = self.player.position
        self.jumping = False
        # And lastly I add it to the layer. Standard stuff

if __name__ == "__main__":
    global keyboard, scroller
    cocos.director.director.init(width=constants.SCREEN_WIDTH, 
        height=constants.SCREEN_HEIGHT, fullscreen=False, resizable=True)

    player_layer = ScrollableLayer()
    player = Player()
    player_layer.add(player)
    player.do(PlayerAction())
    scroller = ScrollingManager()

    scroller.add(player_layer)
    main_scene = cocos.scene.Scene()
    scroller.set_focus(player.position[0], player.position[1])

    #main_scene.add(level1, z=0)
    #main_scene.add(ColorLayer(0, 0, 0, 0), z=0)
    main_scene.add(scroller, z=1)
    #main_scene.add(level1, z=2)
    keyboard = KeyStateHandler()
    cocos.director.director.window.push_handlers(keyboard)
    def on_key_press(key, modifier):
        if symbol_string(key) == "EXIT":
            cocos.director.director.window.close()
            pyglet.app.exit()
    cocos.director.director.window.push_handlers(on_key_press)
    cocos.director.director.run(main_scene)
