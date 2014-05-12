from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from collections import Iterable, Sequence
import numpy as np

def _type_check(val, errormessage, *types):
    for type_ in types:
        if not isinstance(val, type_):
            raise TypeError(errormessage % (str(val)))

class VertexAttribute(Iterable):
    def __init__(self, data, components=3):
        _type_check(data, "Data must be iterable and a sequence but is of type %s", Iterable, Sequence)
        self._data = data
        self._is_sequence = isinstance(data[0], Sequence)
        if self._is_sequence:
            self._length = len(data)
        else:
            if not len(data) % components == 0:
                raise ValueError("Number of data elements %d is not evenly divisible by number of components %d", (len(data), components))
            self._length = len(data) // components
            self.components = components

    def __getitem__(self, i):
        if i < 0 or i >= self._length:
            raise IndexError("Index out of range (%d / %d)" % (i, self._length))
        if self._is_sequence:
            return self._data[i]
        else:
            return self._data[i * self.components : (i + 1) * self.components]

    def __len__(self):
        return self._length

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

class VertexBufferObject:
    def _build_data(self, positions, colors):
        if not isinstance(positions, VertexAttribute):
            raise TypeError("positions must be a VertexAttribute (is %s)" % type(positions))
        if colors is not None and not isinstance(colors, VertexAttribute):
            raise TypeError("Colors must be an instance of VertexAttribute (is %s)" % type(colors))
        data = None
        if colors is not None:
            if not len(colors) == len(positions):
                raise ValueError("Colors and positions are unequal lengths (%d : %d)" % (len(colors), len(positions)))

            data_backing = []
            for i in range(len(positions)):
                data_backing += positions[i]
                data_backing += colors[i]
            data = np.array(data_backing, 'f')
        else:
            data = np.array(positions._data, 'f')
        return data

    def __init__(self, positions, colors=None, mode=GL_TRIANGLES):
        self._has_color = colors is not None

        data = self._build_data(positions, colors)

        self._mode = mode
        self._vbo = vbo.VBO(data)
        self._length = len(positions)

    def replace_data(self, positions, colors=None):
        self._has_color = colors is not None
        self._vbo.set_array(self._build_data(positions, colors))

    def render(self):
        self._vbo.bind()
        data_size = 0
        if self._has_color:
            data_size = 24
        else:
            data_size = 12
        try:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, data_size, self._vbo)
            if self._has_color:
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(3, GL_FLOAT, data_size, self._vbo + 12)
            glDrawArrays(self._mode, 0, self._length)
        finally:
            self._vbo.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
            if self._has_color:
                glDisableClientState(GL_COLOR_ARRAY)


class ShaderProgram:
    def __init__(self, vert, frag):
        vert_source = open(vert).read().encode('ascii')
        frag_source = open(frag).read().encode('ascii')
        vert_shader = shaders.compileShader(vert_source, GL_VERTEX_SHADER)
        frag_shader = shaders.compileShader(frag_source, GL_FRAGMENT_SHADER)
        self.program = shaders.compileProgram(vert_shader, frag_shader)

    def bind(self):
        shaders.glUseProgram(self.program)

    def unbind(self):
        shaders.glUseProgram(0)
