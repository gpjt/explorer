from OpenGL.GL import *


# We keep the current rotation state of the spaceship and the camera as a matrix;
# the following is a (doubtless poor) way of encapsulating this.     

class RotationHandler(object):

    def __init__(self, reverse=False):
        self.reverse = reverse
        glPushMatrix()
        glLoadIdentity()
        self.rotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

        
    def yawBy(self, degrees):
        glPushMatrix()
        if self.reverse:
            glLoadIdentity()
            glRotatef(degrees, 0, 1, 0)
            glMultMatrixf(self.rotationMatrix)            
        else:
            glLoadMatrixf(self.rotationMatrix)
            glRotatef(degrees, 0, 1, 0)
        self.rotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()


    def pitchBy(self, degrees):        
        glPushMatrix()
        if self.reverse:
            glLoadIdentity()
            glRotatef(degrees, 1, 0, 0)
            glMultMatrixf(self.rotationMatrix)            
        else:
            glLoadMatrixf(self.rotationMatrix)
            glRotatef(degrees, 1, 0, 0)
        self.rotationMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()


    def rotateVector(self, x, y, z):
        glPushMatrix()
        glLoadMatrixf(self.rotationMatrix)
        glTranslatef(x, y, z)
        rotated = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        rX, rY, rZ, _ = rotated[3]
        return rX, rY, rZ
        

    def rotateCurrentMatrix(self):
        glMultMatrixf(self.rotationMatrix)
