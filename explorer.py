from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *


# Default window size
resolution = (1280, 1024)

# Vertical field of view
fovV = 45

minClipping = 0.1
maxClipping = 1000


class DoneException(Exception):
    pass


def resize(width, height):
    if height==0:
        height = 1.0
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width) / height, minClipping, maxClipping)
    glMatrixMode(GL_MODELVIEW)
    


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def handle_keys(key):
    pass        


def handle_event():
    event = pygame.event.poll()
    if event.type == NOEVENT:
        return
    if event.type == KEYDOWN:
        handle_keys(event.key)
    if event.type == QUIT:
        raise DoneException()


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def main():

    video_flags = OPENGL | DOUBLEBUF
    
    pygame.init()
    try:
        displayInfo = pygame.display.Info()
        width, height = resolution
        width = min(width, displayInfo.current_w)
        height = min(height, displayInfo.current_h - 20)
        
        pygame.display.set_mode((width, height), video_flags)
        pygame.key.set_repeat(100,0)

        resize(width, height)
        init()

        frames = 0
        ticks = pygame.time.get_ticks()
        while True:
            handle_event()
            draw()
            pygame.display.flip()
            frames += 1

    except DoneException:
        print "fps:  %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks))
        
    finally:
        pygame.quit()

if __name__ == '__main__': main()

