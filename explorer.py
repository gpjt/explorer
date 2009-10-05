import locale

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from Dashboard import Dashboard
from RotationHandler import RotationHandler
from Universe import Universe
from Utils import LoadTexture


class UI(object):

    def __init__(self):
        self.resolution = (1280, 1024)

        # Vertical field of view
        self.fovV = 45

        self.minClipping = 0.1
        self.maxClipping = 5000000000000

        self.done = False
        self.dragging = False
        self.dragLastEvent = None

        self.cameraDistance = 0.6


    def resize(self, width, height):
        if height == 0:
            height = 1.0
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovV, float(width) / height, self.minClipping, self.maxClipping)
        glMatrixMode(GL_MODELVIEW)
        

    def initGL(self):
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_TEXTURE_2D)

        glPushMatrix()
        glLoadIdentity()
        self.cameraRotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()


    def handleKeys(self, key):
        if key == K_LESS or key == K_COMMA:
            self.universe.userSpaceship.thrust -= 1
        elif key == K_GREATER or key == K_PERIOD:
            self.universe.userSpaceship.thrust += 1
        elif key == K_SLASH:
            self.universe.userSpaceship.thrust = 0
        elif key == K_s:
            self.universe.userSpaceship.rotateBy(3, (1, 0, 0))
        elif key == K_w:
            self.universe.userSpaceship.rotateBy(-3, (1, 0, 0))
        elif key == K_q:
            self.universe.userSpaceship.rotateBy(3, (0, 1, 0))
        elif key == K_e:
            self.universe.userSpaceship.rotateBy(-3, (0, 1, 0))
        elif key == K_a:
            self.universe.userSpaceship.rotateBy(3, (0, 0, 1))
        elif key == K_d:
            self.universe.userSpaceship.rotateBy(-3, (0, 0, 1))
        elif key == K_j:
            self.universe.userSpaceship.jump()


    def handleMousedown(self, event):
        if event.button == 1:
            self.dragging = True
            self.dragLastEvent = pygame.mouse.get_pos()
        if event.button == 4:
            # Mouse wheel roll up
            self.cameraDistance -= 0.01
        elif event.button == 5:
            # Mouse wheel roll down
            self.cameraDistance += 0.01


    def handleMouseup(self, event):
        if event.button == 1:
            if self.dragging:
                self.dragging = False            
                self.dragLastEvent = None

    def handleMousemove(self, event):
        if self.dragging:
            nowX, nowY = pygame.mouse.get_pos()
            thenX, thenY = self.dragLastEvent
            deltaX = nowX - thenX
            deltaY = nowY - thenY

            glPushMatrix()
            glLoadIdentity()
            glRotatef(float(deltaX) / (360. / self.fovV), 0, 1, 0)
            glRotatef(float(deltaY) / (360. / self.fovV), 1, 0, 0)
            glMultMatrixf(self.cameraRotationMatrix)            
            self.cameraRotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
            glPopMatrix()

            self.dragLastEvent = nowX, nowY


    def handleEvent(self):
        event = pygame.event.poll()
        if event.type == NOEVENT:
            return
        elif event.type == KEYDOWN:
            self.handleKeys(event.key)
        elif event.type == MOUSEBUTTONDOWN:
            self.handleMousedown(event)
        elif event.type == MOUSEBUTTONUP:
            self.handleMouseup(event)
        elif event.type == MOUSEMOTION:
            self.handleMousemove(event)
        elif event.type == QUIT:
            self.done = True


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.resize(*self.resolution)
        
        glTranslatef(0, 0, -self.cameraDistance)
        glMultMatrixf(self.cameraRotationMatrix)
        
        self.universe.draw()
        self.dashboard.draw(*self.resolution)


    def main(self):

        video_flags = OPENGL | DOUBLEBUF
        
        pygame.init()
        locale.setlocale(locale.LC_ALL, "")
        try:
            displayInfo = pygame.display.Info()
            width, height = self.resolution
            width = min(width, displayInfo.current_w)
            height = min(height, displayInfo.current_h - 20)
            self.resolution = width, height
            
            pygame.display.set_mode(self.resolution, video_flags)
            pygame.key.set_repeat(100,0)

            self.resize(*self.resolution)
            self.initGL()
            self.universe = Universe()
            self.dashboard = Dashboard(self.universe.userSpaceship)
            self.dashboard.relativeTo = self.universe.initialDashboardRelativeTo

            frames = 0
            ticks = pygame.time.get_ticks()
            lastTicks = ticks
            while not self.done:
                self.handleEvent()
                self.draw()
                currentTicks = pygame.time.get_ticks()
                self.universe.accelerateAndMove(float(currentTicks - lastTicks) / 1000)
                pygame.display.flip()
                frames += 1
                lastTicks = currentTicks

            print "fps:  %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks))

        finally:
            pygame.quit()

if __name__ == '__main__':
    UI().main()

