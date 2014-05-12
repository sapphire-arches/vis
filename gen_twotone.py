import wave
from numpy import sin
from sys import argv
from array import array
from math import pi

samp_rate = int(argv[1])
length = int(argv[2])
freqs = []
for i in range(3, len(argv)):
    freqs.append(int(argv[i]))

constants = [(2 * pi * x / samp_rate) for x in freqs]

out = wave.open('test.wav', 'w')
out.setnchannels(1)
out.setsampwidth(4)
out.setframerate(samp_rate)

data = array('I')
for i in range(samp_rate * length):
    val = 0.0
    for c in constants:
        val += sin(c * i)
    if i % samp_rate == 0:
        print(i)
    val /= 2 * len(constants)
    val += 0.5
    data.append(int(2 ** 32 * val))

out.writeframes(data)
