from visuals import Visual
from visuals.generic import make_square
from util.color import hsv_to_rgb
import numpy as np

class Bars(Visual):
    def __init__(self):
        self._last_heights = []
        self._recent_max = 0.0

    def get_verts(self, w, h, freqs):
        s = max(freqs)
        if s > self._recent_max:
            self._recent_max = s
        for i in range(len(freqs)):
            freqs[i] /= self._recent_max
        verts = []
        colors = []
        height = (1 / 1.1) * h
        width = w / len(freqs)
        circle_points = 16
        max_index = len(freqs)
        if len(self._last_heights) == 0:
            self._last_heights = [0] * max_index
        heights = []
        for i in range(max_index):
            color = hsv_to_rgb(360 * i / max_index, 0.7, 0.7)
            height_increment = int(width)
            box_height = height_increment + height * freqs[i]
            box_height = height_increment * (box_height // height_increment)
            if box_height < self._last_heights[i]:
                diff = self._last_heights[i] - box_height
                box_height = self._last_heights[i] - np.sqrt(diff)
            heights.append(box_height)
            points, cols = make_square(i * width, 0, width, box_height, color)
            verts += points
            colors += cols
        self._last_heights = heights
        return verts, colors
