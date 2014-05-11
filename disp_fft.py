from pydub import AudioSegment
from windowmanagement import create_window, main_loop
from globjects import VertexBufferObject, VertexAttribute, ShaderProgram
from color import hsv_to_rgb
from OpenGL.GL import *
from math import pi
import numpy as np
from numpy.fft import fft
from sys import argv
from time import time

audio = AudioSegment.from_mp3(argv[1])
full_audio = []
for i in range(int(audio.frame_count())):
    full_audio.append(int.from_bytes(audio.get_frame(i), 'little') - 32768)

audio_length = 1000 * audio.frame_count() / audio.frame_rate

colors = []

num_buckets = 128
huedelta = 300 / num_buckets
analysis_width = 2048

def build_colors():
    colors = []
    for i in range(num_buckets - 1):
        color1 = hsv_to_rgb(i * huedelta, 0.7, 0.7)
        color2 = hsv_to_rgb((i + 1) * huedelta, 0.7, 0.7)
        colors += color1;
        colors += color2;
        colors += color1;
        colors += color1;
        colors += color2;
        colors += color2;
    return colors

def build_verts(seg):
#    freqs = np.abs(fft(seg))
#    freqs = freqs[0:len(freqs)//2]
    freqs = fft(seg).real
    freqs = np.abs(freqs[0:analysis_width // 16])
    verts = []
    # bucketify things
    buckets = []
    bucket_width = int(len(freqs) / num_buckets)
    if bucket_width <= 1:
        buckets = freqs
    else:
        for i in range(len(freqs) // bucket_width):
            buckets.append(sum(freqs[i * bucket_width : (i + 1) * bucket_width]))

    bucket_max = max(np.abs(buckets))

    buckets = [x / bucket_max for x in buckets]
    xdelta = 800 / len(buckets)
    height = 300
    for i in range(len(buckets) - 1):
        xbase = i * xdelta
        verts += (xbase         , 0                      , 0)
        verts += (xbase + xdelta, height * buckets[i + 1], 0)
        verts += (xbase         , height * buckets[i    ], 0)
        verts += (xbase         , 0                      , 0)
        verts += (xbase + xdelta, 0                      , 0)
        verts += (xbase + xdelta, height * buckets[i + 1], 0)
    return VertexAttribute(verts)

def resize(w, h):
    glLoadIdentity()
    glTranslate(-1, 0, 0)
    height_scale = w / h / 400
    glScale(2 / 800, height_scale, 1)
    glViewport(0, 0, w, h)

def display():
    global frame
    global start_time
    frame += 1
    tick = time()
    if tick - start_time > audio_length:
        tick = start_time
    index = int(len(full_audio) * (tick - start_time) / audio_length)
    if index == 0:
        print('song start')
    verts = build_verts(full_audio[index : index + analysis_width])
    vbo.replace_data(verts, colors=colors)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.bind()
    try:
      vbo.render()
    finally:
      shader.unbind()

create_window('plot', display=display, resize=resize)
colors = VertexAttribute(build_colors())
vbo = VertexBufferObject(build_verts(full_audio[0:analysis_width]), colors=colors)
shader = ShaderProgram('shaders/basic.vert', 'shaders/basic.frag')
glClearColor(0, 0, 0, 0)
frame = 0

start_time = time()

main_loop()
