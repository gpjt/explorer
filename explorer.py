from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from os import path

import math


class WorldObject(object):

    def __init__(self, location):
        self.location = location

    def positionAndDraw(self):
        glPushMatrix()

        glTranslatef(*self.location)

        self.draw()

        glPopMatrix()



class Earth(WorldObject):

    def __init__(self, location):
        WorldObject.__init__(self, location)
        self.radius = 6371
        self.texture = self.loadTexture()       


    def loadTexture(self):
        textureSurface = pygame.image.load("envisat-earth.jpg")
        textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                          GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return texture
        

    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluQuadricTexture(quad, GL_TRUE)
        
        glColor3f(1., 1., 1.)
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(quad, self.radius, 40, 40)
        
        gluDeleteQuadric(quad)


class UserSpaceship(WorldObject):

    def __init__(self, location, cameraDistance, cameraYaw, cameraPitch):
        WorldObject.__init__(self, location)
        self.cameraDistance = cameraDistance
        self.cameraYaw = cameraYaw
        self.cameraPitch = cameraPitch

        
    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)

        glColor3f(1., 0., 0.)
        gluCylinder(quad, 0.02, 0, 0.1, 10, 10)
        
        gluDeleteQuadric(quad)


    def getCameraPos(self):
        x, y, z = self.location
        deltaX = self.cameraDistance * math.cos(self.cameraPitch) * math.sin(self.cameraYaw)
        deltaY = self.cameraDistance * math.sin(self.cameraPitch)
        deltaZ = self.cameraDistance * math.cos(self.cameraPitch) * math.cos(self.cameraYaw)
        return x + deltaX, y + deltaY, z + deltaZ
    


class UI(object):

    def __init__(self):
        self.userSpaceship = None
        self.universe = []

        self.resolution = (1280, 1024)

        # Vertical field of view
        self.fovV = 45

        self.minClipping = 0.1
        self.maxClipping = 100000

        self.done = False
        self.dragging = False
        self.dragLastEvent = None


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


    def initUniverse(self):
        self.userSpaceship = UserSpaceship((0, 0, 19999), 0.2, 0, 0)
        self.universe.append(self.userSpaceship)

        earth = Earth((0, 0, 0))    
        self.universe.append(earth)



    def handleKeys(self, key):
        pass        


    def handleMousedown(self, event):
        if event.button == 1:
            self.dragging = True
            self.dragLastEvent = pygame.mouse.get_pos()
        if event.button == 4:
            # Mouse wheel roll up
            self.userSpaceship.cameraDistance -= 0.01
        elif event.button == 5:
            # Mouse wheel roll down
            self.userSpaceship.cameraDistance += 0.01            


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
            self.userSpaceship.cameraPitch -= float(deltaY) / 100
            self.userSpaceship.cameraYaw -= float(deltaX) / 100
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
        cX, cY, cZ = self.userSpaceship.getCameraPos()
        glRotatef(math.degrees(-self.userSpaceship.cameraYaw), 0, 1, 0)
        glRotatef(math.degrees(self.userSpaceship.cameraPitch), 1, 0, 0)
        glTranslatef(-cX, -cY, -cZ)
        
        for obj in self.universe:
            obj.positionAndDraw()


    def main(self):

        video_flags = OPENGL | DOUBLEBUF
        
        pygame.init()
        try:
            displayInfo = pygame.display.Info()
            width, height = self.resolution
            width = min(width, displayInfo.current_w)
            height = min(height, displayInfo.current_h - 20)
            
            pygame.display.set_mode((width, height), video_flags)
            pygame.key.set_repeat(100,0)

            self.resize(width, height)
            self.initGL()
            self.initUniverse()

            frames = 0
            ticks = pygame.time.get_ticks()
            while not self.done:
                self.handleEvent()
                self.draw()
                pygame.display.flip()
                frames += 1

            print "fps:  %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks))

        finally:
            pygame.quit()

if __name__ == '__main__':
    UI().main()

