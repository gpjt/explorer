from OpenGL.GL import *

import pygame

import locale


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
        

