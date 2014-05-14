from util.windowmanagement import create_window, main_loop
from util.globjects import VertexBufferObject, VertexAttribute, ShaderProgram
from util.color import hsv_to_rgb
from visuals import visuals
from visuals.generic import make_square
from OpenGL.GL import *
from math import pi
import numpy as np
from numpy.fft import fft
from sys import argv
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

analysis_width = 1024
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

def freq_index(x):
    return round(analysis_width * x / sample_rate)

def build_verts(seg):
    global selected_visual
    global window_height, window_width
    freq_analysis = fft(seg)
    # select for piano fundimentals
    freq_start = freq_index(30)
    freq_end = freq_index(4000)
    freqs = []
    for i in range(freq_start, freq_end):
        # see http://en.wikipedia.org/wiki/Spectral_estimation and http://en.wikipedia.org/wiki/Periodogram
        sample = np.abs(freq_analysis[i] ** 2) / (analysis_width * (analysis_width / 2))
        sample = sample * (i + 1) / (2 * pi)
        freqs.append(sample)
    return selected_visual.get_verts(window_width, window_height, freqs)

def resize(w, h):
    global window_width, window_height
    window_width = w
    window_height = h
    glLoadIdentity()
    glTranslate(-1, -1, 0)
    glScale(2 / w, 2 / h, 1)
    glViewport(0, 0, w, h)

def display():
    global frame
    global window_height, window_width
    frame += 1
    completion = (mixer.music.get_pos() / 1000 % audio_length) / audio_length
    index = int(len(full_audio) * completion)
    if index == 0:
        print('song start')

    verts,col = build_verts(full_audio[index - analysis_width // 2: index + analysis_width // 2])
    v, c = make_square(0, window_height - 15, completion * window_width, 15, hsv_to_rgb(15, 0.2, 0.7))
    verts += v
    col += c
    vbo.replace_data(VertexAttribute(verts), colors=VertexAttribute(col))
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.bind()
    try:
      vbo.render()
    finally:
      shader.unbind()

create_window('plot', display=display, resize=resize)
window_width = 800
window_height = 600
selected_visual = visuals['circle']()
verts,cols = build_verts(full_audio[0:analysis_width])
vbo = VertexBufferObject(VertexAttribute(verts), colors=VertexAttribute(cols))
shader = ShaderProgram('shaders/basic.vert', 'shaders/basic.frag')
glClearColor(0, 0, 0, 0)
frame = 0

mixer.init()
mixer.music.load(argv[1])
mixer.music.play(loops=-1)

main_loop()
