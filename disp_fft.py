from windowmanagement import create_window, main_loop
from globjects import VertexBufferObject, VertexAttribute, ShaderProgram
from color import hsv_to_rgb
from OpenGL.GL import *
from math import pi
import numpy as np
from numpy.fft import fft
from sys import argv
from time import time
from pygame import mixer
import wave

audio = wave.open(argv[1], 'r')
full_audio = []
audio_length = audio.getnframes() / audio.getframerate()
for i in range(audio.getnframes()):
    full_audio.append((int.from_bytes(audio.readframes(1), 'little') / 2 ** 32) - 0.5)

colors = []

print("wav read finished, finding average")
print(sum(full_audio) / len(full_audio))

analysis_width = 1024
num_buckets = analysis_width
huedelta = 300 / num_buckets
full_audio += [0] * analysis_width

def build_colors(num_quads):
    colors = []
    for i in range(num_quads):
        color1 = hsv_to_rgb(i * huedelta, 0.7, 0.7)
        color2 = hsv_to_rgb((i + 1) * huedelta, 0.7, 0.7)
        colors += color1;
        colors += color2;
        colors += color1;
        colors += color1;
        colors += color2;
        colors += color2;
    return colors

def get_partial_index(array, idx):
    min_idx = int(idx)
    max_idx = min_idx
    if idx + 1 < len(array):
        max_idx = int(idx + 1)
    f = idx - min_idx
    return array[min_idx] * f + (1 - f) * array[max_idx]

def build_verts(seg):
    freqs = fft(seg)
    freqs = np.abs(freqs[1:len(freqs) // 2])
    np.savetxt('freqs.txt', freqs)
    verts = []
    # bucketify things
    buckets = []
    bucket_width = len(freqs) / num_buckets
    idx = 0
    for i in range(num_buckets):
        buckets.append(0)
        for j in range(int(bucket_width)):
            buckets[i] += freqs[i * int(bucket_width) + j]
        if int(bucket_width) == 0:
            buckets[i] += get_partial_index(freqs, len(freqs) * i / num_buckets)

    bucket_max = max(np.abs(buckets))

    buckets = [x / bucket_max for x in buckets]
    xdelta = 800 / (len(buckets) - 1)
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
    glTranslate(-1, -1, 0)
    height_scale = w / h / 400
    glScale(2 / 800, height_scale, 1)
    glViewport(0, 0, w, h)

def display():
    global frame
    global start_time
    frame += 1
    index = int(len(full_audio) * mixer.music.get_pos() / audio_length / 1000)
    if index == 0:
        print('song start')

    verts = build_verts(full_audio[index : index + analysis_width])
    cols = VertexAttribute(colors[0:len(verts) * 3])
    vbo.replace_data(verts, colors=cols)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.bind()
    try:
      vbo.render()
    finally:
      shader.unbind()

create_window('plot', display=display, resize=resize)
colors = build_colors(num_buckets)
verts = build_verts(full_audio[0:analysis_width])
cols = VertexAttribute(colors[0:3*len(verts)])
vbo = VertexBufferObject(verts, colors=VertexAttribute(colors[0:3*len(verts)]))
shader = ShaderProgram('shaders/basic.vert', 'shaders/basic.frag')
glClearColor(0, 0, 0, 0)
frame = 0

mixer.init()
mixer.music.load(argv[1])
mixer.music.play()

start_time = time()
main_loop()
