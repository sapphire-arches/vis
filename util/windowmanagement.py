from OpenGL.GLUT import glutInit, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow
from OpenGL.GLUT import GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH
from OpenGL.GLUT import glutDisplayFunc, glutReshapeFunc, glutIdleFunc
from OpenGL.GLUT import glutMainLoop
from OpenGL.GLUT import glutSwapBuffers
from time import time, sleep
from sys import argv
def create_window(winname, size=(800, 600), display=None, resize=None):
    glutInit(argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(size[0], size[1])
    glutCreateWindow(winname.encode('ascii'))

    if display is not None:
        display_func = _display_wrapper(display)
        glutDisplayFunc(display_func)
        glutIdleFunc(display_func)

    if resize is not None:
        glutReshapeFunc(resize)

def main_loop():
    glutMainLoop()

_lastTime = 0
def _display_wrapper(display):
    def disp():
        global _lastTime
        display()
        tick = time()
        required_delta = (1/60) - (tick - _lastTime)
        if (required_delta > 0):
            sleep(required_delta)
        _lastTime = tick
        glutSwapBuffers()
    return disp
