from OpenGL.GL import *
from OpenGL.GLU import *

from Utils import LoadTexture
from WorldObject import WorldObject

class Earth(WorldObject):

    def __init__(self, location, velocity):
        WorldObject.__init__(self, 5.9736 * 10**24, location, velocity)
        self.radius = 6371
        self.rotationPeriod = 3600 * 24
        self.rotation = 0
        self.texture = LoadTexture("envisat-earth.jpg")
        self.name = "Earth"
        

    def draw(self):
        quad = gluNewQuadric()

        # By default we'd wind up with the north pole facing the +ve
        # Z axis, which would be toward us normally.
        glRotatef(self.rotation, 0, 1, 0)
        glRotatef(-90, 1, 0, 0)        

        gluQuadricOrientation(quad, GLU_OUTSIDE)
        gluQuadricTexture(quad, GL_TRUE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (1, 1, 1, 1))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
        glMaterialf(GL_FRONT, GL_SHININESS, 0)
        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 0))
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(quad, self.radius, 40, 40)
        
        gluDeleteQuadric(quad)


    def accelerateAndMove(self, restOfUniverse, time):
        WorldObject.accelerateAndMove(self, restOfUniverse, time)
        self.rotation += 360 / (self.rotationPeriod / time)
