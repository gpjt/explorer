import math

from OpenGL.GL import *
from OpenGL.GLU import *

from RotationHandler import RotationHandler
from WorldObject import WorldObject


class UserSpaceship(WorldObject):

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 1000000, location, velocity)
        self.thrust = 0
        
        glPushMatrix()
        glLoadIdentity()
        self.rotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()


    def yawBy(self, degrees):
        glPushMatrix()
        glLoadMatrixf(self.rotationMatrix)
        glRotatef(degrees, 0, 1, 0)
        self.rotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()


    def pitchBy(self, degrees):        
        glPushMatrix()
        glLoadMatrixf(self.rotationMatrix)
        glRotatef(degrees, 1, 0, 0)
        self.rotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
    

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

        glPushMatrix()
        glLoadMatrixf(self.rotationMatrix)
        glTranslatef(0, 0, -self.thrust)
        rotated = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        rX, rY, rZ, _ = rotated[3]

        return aX + rX, aY + rY, aZ + rZ
        

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

        glMultMatrixf(self.rotationMatrix)
        
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


