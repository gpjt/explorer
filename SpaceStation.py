from OpenGL.GL import *
from OpenGL.GLU import *

from Utils import LoadTexture
from WorldObject import WorldObject

class SpaceStation(WorldObject):

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 1000000000, location, velocity)
        self.name = "Space Station"
        self.rotationPeriod = 5 * 60
        self.rotation = 0

        
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
        glRotatef(self.rotation, 0, 0, 1)
        
        self._selectColor((1, 1, 1), False)

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluCylinder(quad, 1, 1, 0.05, 30, 30)
        gluDeleteQuadric(quad)

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluCylinder(quad, 0.95, 0.95, 0.05, 30, 30)
        gluDeleteQuadric(quad)

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluCylinder(quad, 0.1, 0.1, 0.05, 30, 30)
        gluDeleteQuadric(quad)

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluDisk(quad, 0.95, 1, 30, 30)
        gluDeleteQuadric(quad)

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluDisk(quad, 0, 0.1, 30, 30)
        gluDeleteQuadric(quad)        

        glTranslate(0, 0, 0.05)

        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluDisk(quad, 0.95, 1, 30, 30)
        gluDeleteQuadric(quad)
        
        quad = gluNewQuadric()
        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluDisk(quad, 0, 0.1, 30, 30)
        gluDeleteQuadric(quad)        

        glTranslate(0, 0, -0.025)
        glRotatef(90, 1, 0, 0)
        for i in range(12):
            quad = gluNewQuadric()
            gluQuadricOrientation(quad, GLU_OUTSIDE)
            gluCylinder(quad, 0.01, 0.01, 1, 30, 30)
            gluDeleteQuadric(quad)
            glRotatef(30, 0, 1, 0)

            
    def accelerateAndMove(self, restOfUniverse, time):
        WorldObject.accelerateAndMove(self, restOfUniverse, time)
        self.rotation += 360 / (self.rotationPeriod / time)

