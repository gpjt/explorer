from OpenGL.GL import *

import math


# Gravitational constant
G = 6.67428 * 10**-11


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


    def relativeVelocity(self, offsetX, offsetY, offsetZ):
        x, y, z = self.velocity
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


