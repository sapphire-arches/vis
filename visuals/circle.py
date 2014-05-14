from visuals import Visual
from visuals.generic import make_circle_segment
from util.color import hsv_to_rgb
from numpy import sqrt, pi

def _interpolate(x1, x2, f):
    return x1 * (1 - f) + x2 * f

class Circle(Visual):
    def __init__(self):
        self._last_heights = []
        self._recent_max = 0.0

    def get_verts(self, w, h, freqs):
        s = max(freqs)
        if s > self._recent_max:
            self._recent_max = s
        for i in range(len(freqs)):
            freqs[i] /= self._recent_max
        if len(self._last_heights) == 0:
            self._last_heights = [0] * len(freqs)
        heights = []
        verts = []
        colors = []

        inner_radius = h / 10

        height = (1 / 1.1) * h
        height_increment = inner_radius
        angle_delta = 2 * pi / len(freqs)

        for i in range(len(freqs)):
            color1 = hsv_to_rgb(_interpolate(0, 360, (i / len(freqs))), 0.7, 0.7)
            color2 = hsv_to_rgb(_interpolate(0, 360, ((i + 1) / len(freqs))), 0.7, 0.7)
            seg_height = inner_radius + height_increment * freqs[i]
            #seg_height = height_increment * (seg_height // height_increment)
            if seg_height < self._last_heights[i]:
                diff = self._last_heights[i] - seg_height
                seg_height = self._last_heights[i] - sqrt(diff)
            heights.append(seg_height)
            angle = 2 * pi * i / len(freqs)
            points, cols = make_circle_segment(angle, angle_delta, inner_radius, seg_height, color1, color2)
            for j in range(len(points) // 3):
                points[j * 3    ] += w / 2
                points[j * 3 + 1] += h / 2
            verts += points
            colors += cols
        self._last_heights = heights
        return verts, colors
