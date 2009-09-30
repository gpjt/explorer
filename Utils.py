from OpenGL.GL import *
from OpenGL.GLU import *

import pygame


def NormaliseAngle(value):
    if value > 180:
        value = -360 + value
    if value < -180:
        value = 360 + value
    return value        


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
