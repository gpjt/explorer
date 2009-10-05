from Earth import Earth
from Sun import Sun
from SurroundingSky import SurroundingSky
from UserSpaceship import UserSpaceship


class Universe(object):

    def __init__(self):
        self.sky = SurroundingSky()

        sun = Sun((0, 0, 0), (0, 0, 0))

        earth = Earth(sun.offset(79262956, -128906582, -13927363), (24.85, 15.34, 2.499))

        # Some interesting values:
        #  Distant orbit
        #self.userSpaceship = UserSpaceship(earth.offset(0, 0, 19999), earth.relativeVelocity(-4.4667, 0, 0))
        #  Roughly as high as the ISS
        self.userSpaceship = UserSpaceship(earth.offset(0, 0, earth.radius + 340), earth.relativeVelocity(-7.73, 0, 0))
        #  GEO
        # self.userSpaceship = UserSpaceship(earth.offset(0, 0, 42164), earth.relativeVelocity(-3.07, 0, 0))
        #  Here's a good resource for finding velocity for a circular orbit at a given altitude,
        #  though you need to remember that it's altitude and not distance from the centre of the
        #  Earth: <http://home.att.net/~ntdoug/UCM2.html>

        self.objects = []
        self.objects.append(sun)
        self.objects.append(earth)
        self.objects.append(self.userSpaceship)

        self.initialDashboardRelativeTo = earth


    def draw(self):
        # Draw the sky separately...
        if self.sky:
            self.sky.draw()
        
        # In a normal OpenGL scene, we'd now do something like this:
        #   glTranslatef(-cX, -cY, -cZ)
        # and then tell all of our objects to draw themselves at their
        # world location.  However, this leads to weird jiggling effects
        # because of rounding.  For example, if the universe has the Sun
        # at (0, 0, 0) and then the user's spaceship is at (0, 0, 93000000)
        # and all objects are posistioned with a fixed number of significant
        # figures, then the Sun is positioned precisely in the right place
        # but the spaceship might be misplaced by a meter or so -- so it
        # starts jiggling around.  It's better to have objects that are
        # close to the camera close to the origin so that nearby objects
        # are positioned accurately, and distant ones can be out.
        cX, cY, cZ = self.userSpaceship.location
        for obj in self.objects:
            obj.positionAndDraw(-cX, -cY, -cZ)

        
    def accelerateAndMove(self, time):
        for objectToMove in self.objects:
            objectToMove.accelerateAndMove(self.objects, time)

            
