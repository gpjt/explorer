from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from os import path

import math
import locale

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


    def scalarDistanceRelativeTo(self, other):
        sX, sY, sZ = self.location
        oX, oY, oZ = other.location
        return math.sqrt((oX - sX) ** 2 + (oY - sY) ** 2 + (oZ - sZ) ** 2)


    def scalarVelocityRelativeTo(self, other):
        sX, sY, sZ = self.velocity
        oX, oY, oZ = other.velocity
        return math.sqrt((oX - sX) ** 2 + (oY - sY) ** 2 + (oZ - sZ) ** 2)


    def calculateAccelerationVector(self, restOfUniverse):
        acceleration = (0, 0, 0)
        for attractiveObject in restOfUniverse:
            if self == attractiveObject:
                continue

            # Calculate displacement in meters (for compatibility with G)
            displacement = (
                (self.location[0] - attractiveObject.location[0]) * 1000,
                (self.location[1] - attractiveObject.location[1]) * 1000,
                (self.location[2] - attractiveObject.location[2]) * 1000
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

        return aX, aY, aZ


    def accelerateAndMove(self, restOfUniverse, time):
        aX, aY, aZ = self.calculateAccelerationVector(restOfUniverse)
        x, y, z = self.location
        vX, vY, vZ = self.velocity
        
        # s = ut + 0.5at**2
        timeSquared = time ** 2
        self.location = (
            x + vX * time + 0.5 * aX * timeSquared,
            y + vY * time + 0.5 * aY * timeSquared,
            z + vZ * time + 0.5 * aZ * timeSquared
        )

        # v = u + at
        self.velocity = (
            vX + aX * time,
            vY + aY * time,
            vZ + aZ * time
        )



class Sun(WorldObject):

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 1.9891 * 10**30, location, velocity)
        self.radius = 1392000
        self.color = (1., 1., 0.5)
        self.lightNum = GL_LIGHT0
        self.name = "The Sun"


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
        self.name = "Earth"
        

    def draw(self):
        quad = gluNewQuadric()

        # By default we'd wind up with the north pole facing the +ve
        # Z axis, which would be toward us normally.
        glRotatef(-90, 1, 0, 0)

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
        self.thrust = 0
        self.pitch = 0
        self.yaw = 0


    def _selectColor(self, color):
        r, g, b = color
        glMaterialfv(GL_FRONT, GL_AMBIENT, (r * 0.2, g * 0.2, b * 0.2, 1));
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (r, g, b, 1));
        glMaterialfv(GL_FRONT, GL_SPECULAR, (r, g, b, 1));
        glMaterialf(GL_FRONT, GL_SHININESS, 0);
        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 0));


    def changeThrust(self, delta):
        self.thrust = max(0, self.thrust + delta)


    def calculateAccelerationVector(self, restOfUniverse):
        aX, aY, aZ = WorldObject.calculateAccelerationVector(self, restOfUniverse)
        return aZ, aY, aZ - self.thrust
        

    def draw(self):
        quad = gluNewQuadric()

        gluQuadricOrientation(quad, GLU_OUTSIDE)

        length = 0.1
        baseRadius = 0.02

        # Move to the centre of the spaceship
        glTranslatef(0, 0, -(length / 2))

        # ...and then in order to make it point away from us, we rotate
        # around by 180 degrees.
        glRotatef(180, 0, 1, 0)

        # Finally, we take account of pitch and yaw
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)

        # End-cap
        if self.thrust:
            color = (1, 0, 0)
        else:
            color = (1, 1, 1)

        self._selectColor(color)            
        gluDisk(quad, 0, baseRadius, 30, 30)

        # Cone
        self._selectColor((1, 1, 1))
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

        self.initialDashboardRelativeTo = earth


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
            objectToMove.accelerateAndMove(self.objects, time)

            

class Dashboard(object):

    def __init__(self, userSpaceship):
        self.userSpaceship = userSpaceship
        self.font = pygame.font.Font(None, 20)
    
    
    def _renderText(self, text):
        textSurface = self.font.render(text, True, (0, 255, 0, 255), (0, 0, 0, 0))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        return textSurface, textData        

    def _normalise(self, number):            
        if number < 0.1:
            return locale.format("%.1f", number * 1000, True)
        elif number < 1:
            return locale.format("%.0f", number * 1000, True)
        elif number < 10:
            return "%sk" % locale.format("%.2f", number, True)
        elif number < 100:
            return "%sk" % locale.format("%.1f", number, True)
        return "%sk" % locale.format("%.0f", number, True)


    def draw(self, screenWidth, screenHeight):
        topOffset = 10
        rightOffset = 10
        wGap = 10
        leading = 3

        data = [
            ("Relative to:", self.relativeTo.name),
            ("Distance:", "%sm" % self._normalise(self.userSpaceship.scalarDistanceRelativeTo(self.relativeTo))),
            ("Velocity:", "%sm/s" % self._normalise(self.userSpaceship.scalarVelocityRelativeTo(self.relativeTo))),
        ]

        # Draw text, adapted from http://code.activestate.com/recipes/115418/
        glPushMatrix()
        
        glViewport(0, 0, screenWidth, screenHeight)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, screenWidth - 1.0, 0.0, screenHeight - 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        renderedData = []
        maxLeft = 0
        maxRight = 0
        maxHeight = 0
        for leftLabel, rightLabel in data:
            leftRender = self._renderText(leftLabel)
            rightRender = self._renderText(rightLabel)
            renderedData.append((leftRender, rightRender))
            maxLeft = max(maxLeft, leftRender[0].get_width())
            maxRight = max(maxRight, rightRender[0].get_width())
            maxHeight = max(maxHeight, leftRender[0].get_height(), rightRender[0].get_height())

        for rowIndex, ((leftSurface, leftData), (rightSurface, rightData)) in enumerate(renderedData):
            glRasterPos2i(
                screenWidth - rightOffset - min(maxLeft, leftSurface.get_width()) - wGap - maxRight,
                screenHeight - topOffset - (rowIndex + 1) * (maxHeight + leading)
            )
            glDrawPixels(leftSurface.get_width(), leftSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, leftData)

            glRasterPos2i(
                screenWidth - rightOffset - maxRight,
                screenHeight - topOffset - (rowIndex + 1) * (maxHeight + leading)
            )
            glDrawPixels(rightSurface.get_width(), rightSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, rightData)

        glPopMatrix()
        


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
        if value > 180:
            value = -360 + value
        if value < -180:
            value = 360 + value
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
        if key == K_LESS or key == K_COMMA:
            self.universe.userSpaceship.changeThrust(-1)
        if key == K_GREATER or key == K_PERIOD:
            self.universe.userSpaceship.changeThrust(1)


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
            self.cameraPitch -= float(deltaY) / (360. / self.fovV)
            self.cameraYaw -= float(deltaX) / (360. / self.fovV)
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
        glRotatef(-self.cameraYaw, 0, 1, 0)
        glRotatef(-self.cameraPitch, 1, 0, 0)
        
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

