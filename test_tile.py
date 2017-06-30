


import pyglet
from pyglet.window import key
from pyglet.gl import glClearColor

import cocos
from cocos import tiles, actions, layer

description = """
Loads a tmx map containing a tile layer and an object layer.
The tiles layer is rendered as black region with four green dots.

The debug view of the TmxObjectLayer is draw over that, with four objects
of type 'rect', 'ellipse', 'polygon', 'polyline'

The debug view only draws the Axis Aligned Bounding Box of each object.

You should see four green points covered by translucid white-ish rectangles,
roughly centered at each point. 
"""

def main():
    from cocos.director import director
    director.init(width=800, height=600, autoscale=False, resizable=True)
    glClearColor(255, 255, 255, 255)

    scroller = layer.ScrollingManager()
    maploaded = tiles.load('platform2.tmx')
    layer1 = maploaded["map1"]
    layer2 = maploaded["map2"]
    scroller.add(test_layer)
    object_layer = maploaded['test_object_layer']
    scroller.add(object_layer)
    main_scene = cocos.scene.Scene(scroller)
    print(test_layer.px_width , test_layer.px_height)
    scroller.set_focus(test_layer.px_width // 2, test_layer.px_height //2)

    director.run(main_scene)

if __name__ == '__main__':
    print(description)
    main()
