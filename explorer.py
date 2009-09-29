from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from os import path

import math


# Gravitational constant
G = 6.67428 * 10**-11



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

    def __init__(self, mass, location, velocity):
        self.mass = mass
        self.location = location
        self.velocity = velocity

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

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 1.9891 * 10**30, location, velocity)
        self.radius = 1392000
        self.color = (1., 1., 0.5)
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

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 5.9736 * 10**24, location, velocity)
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

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 1000000, location, velocity)


    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)

        length = 0.1
        baseRadius = 0.02

        # Cones grow up the +Z axis, with the base at Z=0.  So in order
        # to make the centre of ours the centre of this object, we move
        # back half the length
        glTranslatef(0, 0, -(length / 2))

        # ...and then in order to make it point away from us, we rotate
        # around by 180 degrees.
        glRotatef(180, 0, 1, 0)

        glColor3f(1., 0., 0.)

        # End-cap
        gluDisk(quad, 0, baseRadius, 30, 30)

        # Cone
        gluCylinder(quad, baseRadius, 0, length, 30, 30)
        
        gluDeleteQuadric(quad)



class Universe(object):

    def __init__(self):
        self.sky = SurroundingSky()

        sun = Sun((0, 0, 0), (0, 0, 0))

        earth = Earth(sun.offset(149600000, 0, 0), (0, 0, 0))

        # Some interesting values:
        #  Distant orbit
        self.userSpaceship = UserSpaceship(earth.offset(0, 0, 19999), (-4.4667, 0, 0))
        #  Roughly as high as the ISS
        # self.userSpaceship = UserSpaceship(earth.offset(0, 0, earth.radius + 340), (-7.73, 0, 0))
        #  GEO
        # self.userSpaceship = UserSpaceship(earth.offset(0, 0, 42164), (-3.07, 0, 0))
        #  Here's a good resource for finding velocity for a circular orbit at a given altitude,
        #  though you need to remember that it's altitude and not distance from the centre of the
        #  Earth: <http://home.att.net/~ntdoug/UCM2.html>

        self.objects = []
        self.objects.append(sun)
        self.objects.append(earth)
        self.objects.append(self.userSpaceship)
            

    def draw(self):
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
        for obj in self.objects:
            obj.positionAndDraw(-cX, -cY, -cZ)


    def accelerateAndMove(self, time):
        for objectToMove in self.objects:
            acceleration = (0, 0, 0)
            for attractiveObject in self.objects:
                if objectToMove == attractiveObject:
                    continue

                # Calculate displacement in meters (for compatibility with G)
                displacement = (
                    (objectToMove.location[0] - attractiveObject.location[0]) * 1000,
                    (objectToMove.location[1] - attractiveObject.location[1]) * 1000,
                    (objectToMove.location[2] - attractiveObject.location[2]) * 1000
                )
                distanceSquared = displacement[0] ** 2 + displacement[1] ** 2 + displacement[2] ** 2
                # F=ma => a = F/m, and F = -GMm/r**2, so we can cancel out m to get acceleration
                scalarAcceleration = - (G * attractiveObject.mass) / distanceSquared
                distance = math.sqrt(distanceSquared)
                unitDisplacement = (
                    displacement[0] / distance,
                    displacement[1] / distance,
                    displacement[2] / distance,
                )
                aX, aY, aZ = acceleration
                acceleration = (
                    aX + scalarAcceleration * unitDisplacement[0],
                    aY + scalarAcceleration * unitDisplacement[1],
                    aZ + scalarAcceleration * unitDisplacement[2]
                )             

            # Because all of the calculations above were in meters, we now have acceleration in
            # ms**-2.  Convert to km to fit our normal units...
            aX, aY, aZ = acceleration
            aX /= 1000
            aY /= 1000
            aZ /= 1000

            x, y, z = objectToMove.location
            vX, vY, vZ = objectToMove.velocity

            
            # s = ut + 0.5at**2
            timeSquared = time ** 2
            objectToMove.location = (
                x + vX * time + 0.5 * aX * timeSquared,
                y + vY * time + 0.5 * aY * timeSquared,
                z + vZ * time + 0.5 * aZ * timeSquared
            )

            # v = u + at
            objectToMove.velocity = (
                vX + aX * time,
                vY + aY * time,
                vZ + aZ * time
            )
                
                

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
        self.cameraYaw = 0
        self.cameraPitch = 0


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


    def handleKeys(self, key):
        pass        


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
            self.cameraPitch -= float(deltaY) / 300
            self.cameraYaw -= float(deltaX) / 300
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
        
        glTranslatef(0, 0, -self.cameraDistance)
        glRotatef(math.degrees(-self.cameraYaw), 0, 1, 0)
        glRotatef(math.degrees(-self.cameraPitch), 1, 0, 0)
        
        self.universe.draw()


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
            self.universe = Universe()

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

