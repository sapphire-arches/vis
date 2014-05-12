from windowmanagement import create_window, main_loop
from globjects import VertexBufferObject, VertexAttribute, ShaderProgram
from color import hsv_to_rgb
from OpenGL.GL import *
from math import pi
import numpy as np
from numpy import sin, cos
from numpy.fft import fft
from sys import argv
from time import time
from pygame import mixer
import wave
from array import array

audio = wave.open(argv[1], 'r')
audio_length = audio.getnframes() / audio.getframerate()
full_audio = array('I', audio.readframes(audio.getnframes())).tolist()
full_audio = [x / (2 ** 32) - 0.5 for x in full_audio]
sample_rate = audio.getframerate()

colors = []

print("wav read finished, finding average")
print(sum(full_audio) / len(full_audio))

analysis_width = 128
num_buckets = 128
huedelta = 0.001
print("padding")
full_audio += [0] * analysis_width
full_audio = [0] * analysis_width + full_audio

def get_partial_index(array, idx):
    min_idx = int(idx)
    max_idx = min_idx
    if idx + 1 < len(array):
        max_idx = int(idx + 1)
    f = idx - min_idx
    return array[min_idx] * (1 - f) + f * array[max_idx]

def make_circle_point(angle, radius):
    return (cos(angle) * radius, sin(angle) * radius, 0)

def freq_index(x):
    return round(analysis_width * x / sample_rate)

def make_circle(inner_radius, outer_radius, steps, color=None):
    delta = 2 * pi / steps
    hue_delta = -100 / steps
    hue = -hue_delta * steps / 2
    saturation = 0.7
    value = 0.7
    points = []
    colors = []
    for i in range(0, steps):
        angle = i * delta
        color1 = color2 = None
        if color is None:
            color1 = hsv_to_rgb(hue            , saturation, value)
            color2 = hsv_to_rgb(hue + hue_delta, saturation, value)
        else:
            color1 = color
            color2 = color
        points += make_circle_point(angle        , inner_radius); colors +=  color1
        points += make_circle_point(angle + delta, outer_radius); colors +=  color2
        points += make_circle_point(angle        , outer_radius); colors +=  color1
        points += make_circle_point(angle        , inner_radius); colors +=  color1
        points += make_circle_point(angle + delta, inner_radius); colors +=  color2
        points += make_circle_point(angle + delta, outer_radius); colors +=  color2
        if i == steps / 2:
            hue_delta = -hue_delta
        hue += hue_delta
    return points, colors

def make_square(x, y, w, h, color):
    verts = []
    colors = [color] * 6
    verts += (x    , y    , 0)
    verts += (x + w, y    , 0)
    verts += (x    , y + h, 0)
    verts += (x + w, y    , 0)
    verts += (x + w, y + h, 0)
    verts += (x    , y + h, 0)
    return verts, colors

def build_verts(seg):
    global last_heights
    freq_analysis = fft(seg)
    freq_start = 4 #freq_index()
    freq_end = freq_index(20000)
    freqs = []
    for i in range(freq_start, freq_end):
        freqs.append((np.abs(freq_analysis[i] ** 2) / (freq_end - freq_start)) * (i + 1) / ( 2 * pi))
    verts = []
    colors = []
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
        buckets[i] = np.sqrt(buckets[i])

    buckets = freqs
    height = 50
    width = 800 / len(buckets)
    circle_points = 16
    max_index = len(buckets)
    if len(last_heights) == 0:
        last_heights = [0] * max_index
    heights = []
    for i in range(max_index):
        color = hsv_to_rgb(360 * i / max_index, 0.7, 0.7)
        height_increment = int(width)
        box_height = height_increment + height * buckets[i]
        box_height = height_increment * (box_height // height_increment)
        if box_height < last_heights[i]:
            last_heights[i] -= 1
            box_height = last_heights[i]
        heights.append(box_height)
        points, cols = make_square((i - max_index // 2) * width, 0, width, box_height, color)
        verts += points
        colors += cols
    last_heights = heights
    return VertexAttribute(verts), VertexAttribute(colors)

def resize(w, h):
    glLoadIdentity()
    glTranslate(0, -1, 0)
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

    verts,col = build_verts(full_audio[index - analysis_width // 2: index + analysis_width // 2])
#    cols = VertexAttribute(colors[0:len(verts) * 3])
    vbo.replace_data(verts, colors=col)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.bind()
    try:
      vbo.render()
    finally:
      shader.unbind()

create_window('plot', display=display, resize=resize)
last_heights = []
verts,cols = build_verts(full_audio[0:analysis_width])
vbo = VertexBufferObject(verts, colors=cols)
shader = ShaderProgram('shaders/basic.vert', 'shaders/basic.frag')
glClearColor(0, 0, 0, 0)
frame = 0

mixer.init()
mixer.music.load(argv[1])
mixer.music.play()

start_time = time()
main_loop()
