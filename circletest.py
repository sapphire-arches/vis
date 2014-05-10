from windowmanagement import create_window, main_loop
from globjects import VertexBufferObject, VertexAttribute, ShaderProgram
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from math import pi
from numpy import sin, cos
from color import hsv_to_rgb
import numpy as np

shader = None
vertex_buffer = None

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.bind()
    try:
      vertex_buffer.render()
    finally:
      shader.unbind()

def make_circle_point(angle, radius):
    return (cos(angle) * radius, sin(angle) * radius, 0)

def make_circle(inner_radius, outer_radius, steps):
    delta = 2 * pi / steps
    hue_delta = -100 / steps
    hue = -hue_delta * steps / 2
    saturation = 0.7
    value = 0.7
    points = []
    colors = []
    for i in range(0, steps):
        angle = i * delta
        color1 = hsv_to_rgb(hue            , saturation, value)
        color2 = hsv_to_rgb(hue + hue_delta, saturation, value)
        points += make_circle_point(angle        , inner_radius); colors +=  color1
        points += make_circle_point(angle + delta, outer_radius); colors +=  color2
        points += make_circle_point(angle        , outer_radius); colors +=  color1
        points += make_circle_point(angle        , inner_radius); colors +=  color1
        points += make_circle_point(angle + delta, inner_radius); colors +=  color2
        points += make_circle_point(angle + delta, outer_radius); colors +=  color2
        if i == steps / 2:
            hue_delta = -hue_delta
        hue += hue_delta
    return VertexBufferObject(VertexAttribute(points), colors=VertexAttribute(colors))

def resize(w, h):
    glLoadIdentity()
    glScale(1 / w, 1 / h, 1)
    glViewport(0, 0, w, h)

def init():
    global shader
    global vertex_buffer
    clear_color = hsv_to_rgb(0.99, 0.1, 0.7)
    glClearColor(clear_color[0], clear_color[1], clear_color[2], 0.0)
    shader = ShaderProgram('shaders/basic.vert', 'shaders/basic.frag')
    vertex_buffer = make_circle(100, 200, 32)

create_window("circles", display=display, resize=resize)
init()
main_loop()
