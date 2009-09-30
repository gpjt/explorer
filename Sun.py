from OpenGL.GL import *
from OpenGL.GLU import *

from WorldObject import WorldObject

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


