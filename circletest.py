from windowmanagement import create_window, main_loop
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np

shader = None
vertex_buffer = None

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shaders.glUseProgram(shader)
    try:
        vertex_buffer.bind()
        try:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointerf(vertex_buffer)
            glDrawArrays(GL_TRIANGLES, 0, 9)
        finally:
            vertex_buffer.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
    finally:
        shaders.glUseProgram(0)

def init():
    global shader
    global vertex_buffer
    glClearColor(1.0, 1.0, 0.0, 0.0)
    vert_shader = shaders.compileShader("""#version 120
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}""".encode('ascii'), GL_VERTEX_SHADER)
    frag_shader = shaders.compileShader("""#version 120
void main() {
    gl_FragColor = vec4(0, 1, 0, 1);
}""".encode('ascii'), GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vert_shader, frag_shader)
    arr = np.array([ [ 0, 1, 0 ], [ -1,-1, 0 ], [ 1,-1, 0 ], [ 2,-1, 0 ], [ 4,-1, 0 ], [ 4, 1, 0 ], [ 2,-1, 0 ], [ 4, 1, 0 ], [ 2, 1, 0 ], ], 'f')
    vertex_buffer = vbo.VBO(arr)

create_window("circles", display=display)
init()
main_loop()
