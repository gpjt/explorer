import math

from OpenGL.GL import *
from OpenGL.GLU import *

from Utils import NormaliseAngle
from WorldObject import WorldObject


class UserSpaceship(WorldObject):

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 1000000, location, velocity)
        self.thrust = 0
        self.pitch = 0
        self.yaw = 0

    @property
    def yaw(self):
        return self.__yaw

    @yaw.setter
    def yaw(self, value):
        self.__yaw = NormaliseAngle(value)

        
    @property
    def pitch(self):
        return self.__pitch

    @pitch.setter
    def pitch(self, value):
        self.__pitch = NormaliseAngle(value)


    @property
    def thrust(self):
        return self.__thrust

    @thrust.setter
    def thrust(self, value):
        self.__thrust = value
        if self.__thrust < 0:
            self.__thrust = 0


    def calculateAccelerationVector(self, restOfUniverse):
        aX, aY, aZ = WorldObject.calculateAccelerationVector(self, restOfUniverse)

        pitch = math.radians(self.pitch)
        yaw = math.radians(self.yaw)
        tX = -self.thrust * math.cos(pitch) * math.sin(yaw)
        tY = self.thrust * math.sin(pitch)
        tZ = -self.thrust * math.cos(pitch) * math.cos(yaw)
        
        return aX + tX, aY + tY, aZ + tZ
        

    def _selectColor(self, color, emission):
        r, g, b = color
        glMaterialfv(GL_FRONT, GL_AMBIENT, (r * 0.2, g * 0.2, b * 0.2, 1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (r, g, b, 1))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (r, g, b, 1))
        glMaterialf(GL_FRONT, GL_SHININESS, 0);
        if emission:
            glMaterialfv(GL_FRONT, GL_EMISSION, (r, g, b, 1))
        else:
            glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 0))


    def draw(self):
        length = 0.1
        baseRadius = 0.02

        # Move to the centre of the spaceship
        glTranslatef(0, 0, -(length / 2))

        # Finally, we take account of pitch and yaw
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)

        # End-cap
        if self.thrust:
            color = (1, 0, 0)
            emission = True
        else:
            color = (1, 1, 1)
            emission = False

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        self._selectColor(color, emission)
        gluDisk(quad, 0, baseRadius, 30, 30)
        gluDeleteQuadric(quad)

        # Tailfins

        self._selectColor((1, 1, 1), False)
        
        for angle in (0, 100, 260):
            glPushMatrix()
            glRotatef(angle, 0, 0, 1)
            glBegin(GL_TRIANGLES)
            # Back
            glNormal3f(0, 0, 1)
            glVertex3f(0, baseRadius * 2.5, -0.0001)
            glVertex3f(-0.001, 0, -0.0001)
            glVertex3f(0.001, 0, -0.0001)
            # Left
            glNormal3f(-1, 0, 0)
            glVertex3f(0, baseRadius * 2.5, -0.0001)
            glVertex3f(-0.001, 0, -0.0001)
            glVertex3f(0, 0, -length / 2)
            # Right
            glNormal3f(1, 0, 0)
            glVertex3f(0, baseRadius * 2.5, -0.0001)
            glVertex3f(0.001, 0, -0.0001)
            glVertex3f(0, 0, -length / 2)
            glEnd()
            glPopMatrix()
    
        # Cone
        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        self._selectColor((1, 1, 1), False)
        # Make it face away from us
        glRotatef(180, 0, 1, 0)
        gluCylinder(quad, baseRadius, 0, length, 30, 30)
        gluDeleteQuadric(quad)


