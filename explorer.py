from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from os import path

import math


class SurroundingSky(object):
    
    def __init__(self):
        self.radius = 10000000
        self.texture = LoadTexture("gigapixel-milky-way.jpg")    


    def draw(self):
        glPushMatrix()
        
        glDisable(GL_DEPTH_TEST) 

        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_INSIDE)
        gluQuadricTexture(quad, GL_TRUE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, (0, 0, 0, 0));
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (0, 0, 0, 0));
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0, 0, 0, 0));
        glMaterialf(GL_FRONT, GL_SHININESS, 0);
        glMaterialfv(GL_FRONT, GL_EMISSION, (1, 1, 1, 1));
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(quad, self.radius, 40, 40)
        
        gluDeleteQuadric(quad)

        glEnable(GL_DEPTH_TEST) 

        glPopMatrix()



def LoadTexture(filename):
    textureSurface = pygame.image.load(filename)
    textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                      GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    return texture    


class WorldObject(object):

    def __init__(self, location):
        self.location = location

    def positionAndDraw(self, offsetX, offsetY, offsetZ):
        glPushMatrix()

        x, y, z = self.location
        glTranslatef(x + offsetX, y + offsetY, z + offsetZ)

        self.draw()

        glPopMatrix()


    def offset(self, offsetX, offsetY, offsetZ):
        x, y, z = self.location
        return x + offsetX, y + offsetY, z + offsetZ



class Sun(WorldObject):

    def __init__(self, location, color=(1., 1., 0.5)):
        WorldObject.__init__(self, location)
        self.radius = 1392000
        self.color = color
        self.lightNum = GL_LIGHT0


    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluQuadricTexture(quad, GL_FALSE)
        glBindTexture(GL_TEXTURE_2D, 0)

        r, g, b = self.color
        
        lightAmbient = ((r / 3., g / 3., b / 3., 1.))
        lightDiffuse = ((r, g, b, 1.))
        lightPosition = ((0, 0, 0, 1.))
        glLightfv(self.lightNum, GL_AMBIENT, lightAmbient)
        glLightfv(self.lightNum, GL_DIFFUSE, lightDiffuse)
        glLightfv(self.lightNum, GL_POSITION, lightPosition)
        glEnable(self.lightNum)
        glEnable(GL_LIGHTING)

        glMaterialfv(GL_FRONT, GL_AMBIENT, self.color);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color);
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.color);
        glMaterialf(GL_FRONT, GL_SHININESS, 1);
        glMaterialfv(GL_FRONT, GL_EMISSION, self.color)

        gluSphere(quad, self.radius, 40, 40)
        
        gluDeleteQuadric(quad)


class Earth(WorldObject):

    def __init__(self, location):
        WorldObject.__init__(self, location)
        self.radius = 6371
        self.texture = LoadTexture("envisat-earth.jpg")
        

    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluQuadricTexture(quad, GL_TRUE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1));
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (1, 1, 1, 1));
        glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1));
        glMaterialf(GL_FRONT, GL_SHININESS, 0);
        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 0));
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(quad, self.radius, 40, 40)
        
        gluDeleteQuadric(quad)


class UserSpaceship(WorldObject):

    def __init__(self, location, cameraDistance, cameraYaw, cameraPitch):
        WorldObject.__init__(self, location)
        self.cameraDistance = cameraDistance
        self.cameraYaw = cameraYaw
        self.cameraPitch = cameraPitch


    def normaliseAngle(self, value):
        if value > math.pi:
            value = -((math.pi * 2) - value)
        if value < -math.pi:
            value = (math.pi * 2) + value
        return value        


    @property
    def cameraYaw(self):
        return self.__cameraYaw

    @cameraYaw.setter
    def cameraYaw(self, value):
        self.__cameraYaw = self.normaliseAngle(value)

        
    @property
    def cameraPitch(self):
        return self.__cameraPitch

    @cameraPitch.setter
    def cameraPitch(self, value):
        self.__cameraPitch = self.normaliseAngle(value)

        
    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)

        length = 0.1
        baseRadius = 0.02

        # Cones grow up the +Z axis, with the base at Z=0.  So in order
        # to make the centre of ours the centre of this object, we move
        # back half the length
        glTranslatef(0, 0, -(length / 2))

        glColor3f(1., 0., 0.)

        # End-cap
        gluDisk(quad, 0, baseRadius, 30, 30)

        # Cone
        gluCylinder(quad, baseRadius, 0, length, 30, 30)
        
        gluDeleteQuadric(quad)



class UI(object):

    def __init__(self):
        self.userSpaceship = None
        self.sky = None
        self.universe = []

        self.resolution = (1280, 1024)

        # Vertical field of view
        self.fovV = 45

        self.minClipping = 0.1
        self.maxClipping = 5000000000000

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
        self.sky = SurroundingSky()

        sun = Sun((0, 0, 0))

        earth = Earth(sun.offset(149600000, 0, 0))

        self.userSpaceship = UserSpaceship(earth.offset(0, 0, 19999), 0.6, 0, 0.0)

        self.universe.append(sun)
        self.universe.append(earth)
        self.universe.append(self.userSpaceship)
    


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
            self.userSpaceship.cameraPitch -= float(deltaY) / 300
            self.userSpaceship.cameraYaw -= float(deltaX) / 300
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
        glTranslatef(0, 0, -self.userSpaceship.cameraDistance)
        glRotatef(math.degrees(-self.userSpaceship.cameraYaw), 0, 1, 0)
        glRotatef(math.degrees(-self.userSpaceship.cameraPitch), 1, 0, 0)

        # Draw the sky separately...
        if self.sky:
            self.sky.draw()
        
        # In a normal OpenGL scene, we'd now do something like this:
        #   glTranslatef(-cX, -cY, -cZ)
        # and then tell all of our objects to draw themselves at their
        # world location.  However, this leads to weird jiggling effects
        # because of rounding.  For example, if the universe has the Sun
        # at (0, 0, 0) and then the user's spaceship is at (0, 0, 93000000)
        # and all objects are posistioned with a fixed number of significant
        # figures, then the Sun is positioned precisely in the right place
        # but the spaceship might be misplaced by a meter or so -- so it
        # starts jiggling around.  It's better to have objects that are
        # close to the camera close to the origin so that nearby objects
        # are positioned accurately, and distant ones can be out.
        cX, cY, cZ = self.userSpaceship.location
        for obj in self.universe:
            obj.positionAndDraw(-cX, -cY, -cZ)


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

