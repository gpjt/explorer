from OpenGL.GL import *
from OpenGL.GLU import *

from Utils import LoadTexture

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


