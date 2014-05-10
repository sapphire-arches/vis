from pydub import AudioSegment
from windowmanagement import create_window, main_loop
from globjects import VertexBufferObject, VertexAttribute, ShaderProgram
from color import hsv_to_rgb
from OpenGL.GL import *
from math import pi
import numpy as np
from numpy.fft import fft
from sys import argv

audio = AudioSegment.from_mp3(argv[1])
seg = [x - 127.5 for x in audio._data]
print("loaded sound, running fft")
freqs = np.abs(fft(seg))
freqs = freqs[0:len(freqs)//2]
print("fft completed")

# bucketify things
buckets = []
num_buckets = 1024
bucket_width = int(len(freqs) / num_buckets)
for i in range(len(freqs) // bucket_width):
    buckets.append(sum(freqs[i * bucket_width : (i + 1) * bucket_width]))

bucket_max = max(buckets)

buckets = [x / bucket_max for x in buckets]

verts = []
colors = []

xdelta = 800 / len(buckets)
huedelta = 2 * pi / 32

for i in range(len(buckets) - 1):
    xbase = i * xdelta
#    color1 = (1, 1, 1)
#    color2 = (1, 1, 1)
    color1 = hsv_to_rgb(i * huedelta, 0.7, 0.7)
    color2 = hsv_to_rgb((i + 1) * huedelta, 0.7, 0.7)
    verts += (xbase         , 0                   , 0); colors += color1;
    verts += (xbase + xdelta, 600 * buckets[i + 1], 0); colors += color2;
    verts += (xbase         , 600 * buckets[i    ], 0); colors += color1;
    verts += (xbase         , 0                   , 0); colors += color1;
    verts += (xbase + xdelta, 0                   , 0); colors += color2;
    verts += (xbase + xdelta, 600 * buckets[i + 1], 0); colors += color2;

def resize(w, h):
    glLoadIdentity()
    glTranslate(-1, -1, 0)
    height_scale = w / h / 400
    glScale(2 / 800, height_scale, 1)
    glViewport(0, 0, w, h)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.bind()
    try:
      vbo.render()
    finally:
      shader.unbind()

create_window('plot', display=display, resize=resize)

vbo = VertexBufferObject(VertexAttribute(verts), colors=VertexAttribute(colors))
shader = ShaderProgram('shaders/basic.vert', 'shaders/basic.frag')
glClearColor(0, 0, 0, 0)

main_loop()
