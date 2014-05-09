from OpenGL.GLUT import glutInit, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow
from OpenGL.GLUT import GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH
from sys import argv
def create_window(winname, size=(800, 600)):
    glutInit(argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(size[0], size[1])
    glutCreateWindow(winname.encode('ascii'))

from OpenGL.GLUT import glutMainLoop
def main_loop():
    glutMainLoop()

from OpenGL.GLUT import glutSwapBuffers
def swap_buffers():
    glutSwapBuffers()
