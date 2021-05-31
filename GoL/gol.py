import pyglet
from pyglet.window import mouse
from pyglet.window import key
from pyglet.graphics import draw
from pyglet.gl import *
from itertools import chain
import numpy as np

WIDTH = 800
HEIGHT = 800
SCALE = 8

RUNNING = False

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

def gol():
    buffer = (GLubyte * (WIDTH * HEIGHT * 3))(0)
    glReadPixels(0, 0, WIDTH, HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, buffer)
    print(buffer)

def get_pixel_locations(x, y):
    base = (x // SCALE, y // SCALE)

    pixels = []

    for i in range(SCALE):
        for j in range(SCALE):
            pixels.append((base[0] * SCALE + i, base[1] * SCALE  + j))

    colors = [(255, 255, 255)] * len(pixels)

    return len(pixels), tuple(chain(*pixels)), tuple(chain(*colors))

@window.event
def on_mouse_press(x, y, button, modifiers):
    global RUNNING

    if not RUNNING:
        if button == mouse.LEFT:
            length, locations, colors = get_pixel_locations(x,y)
            draw(length, pyglet.gl.GL_POINTS, ('v2i', locations), ('c3B', colors))

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    global RUNNING

    if not RUNNING:
        if button == mouse.LEFT:
            length, locations, colors = get_pixel_locations(x,y)
            draw(length, pyglet.gl.GL_POINTS, ('v2i', locations), ('c3B', colors))

@window.event
def on_key_press(symbol, modifiers):
    global RUNNING

    if symbol == key.RETURN:
        if RUNNING:
            RUNNING = False
        else: 
            RUNNING = True
            gol()

pyglet.app.run()

