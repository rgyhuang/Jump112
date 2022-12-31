# Contains all platform classes and functions 
import random
import pygame
from Powerups import *
class Platform(object):
    def __init__ (self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.width = 40
        self.height = 10


class MovePlatform(Platform):
    def __init__(self, posX, posY, upOrDown, velocity):
        super().__init__(posX, posY)
        self.cx = posX
        self.cy = posY
        if upOrDown == 1:
            self.dirX = velocity
            self.dirY = 0
        else:
            self.dirX = 0
            self.dirY = velocity
    def move(self):
        if abs(self.posX-self.cx) > 50:
            self.dirX *= -1
        self.posX += self.dirX
        if abs(self.posY-self.cy) > 50:
            self.dirY *= -1
        self.posY += self.dirY

# if use == 0, platform disappears
class BrokenPlatform(Platform):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.use = 1

class SpringPlatform(Platform):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.boost = 15

def generatePlatform(app):
    plats = app.platformCount - len(app.platforms)
    i = 0
    while i < plats - 1:
        platX, platY = (random.randrange(50, app.width-50), 
                        random.randrange(-app.height, 50))
        # generate platforms with powerups
        if app.powerupTimer >= app.powerupInterval:
            print("powerup generated")
            powerUpType = random.randrange(0, 300)
            # generate jetpack or bullet
            if powerUpType > 250:
                app.powerups += [Powerups(platX, platY-30, 0)]
            else:
                app.powerups += [Powerups(platX, platY-30, 1)]
            app.powerupTimer = 0
        platType = random.randrange(100, 600)
        if platType >= 600-(round((app.prob-5)//100*600)):
            app.platforms.append((3, SpringPlatform(platX, platY)))
        elif platType >= 550-(round(app.prob//100*550)):
            app.platforms.append((4, BrokenPlatform(platX, platY)))
        elif platType >= 400-(round(app.prob//100*400)):
            app.platforms.append((2, MovePlatform(platX, platY, 
                                        random.randrange(1,3), app.platSpeed)))
        else:
            app.platforms.append((1,Platform(platX, platY)))
        i += 1
    app.scoreMultiplier += 1
    # make sure there is always a reachable platform
    app.platforms.append((1, Platform(random.randrange(50, app.width-50), 
                            random.randrange(-app.height+200, 50))))
# initialize platforms
def initPlatforms(app):
    plats = app.platformCount - len(app.platforms)
    i = 0
    while i < plats-1:

        platX, platY = (random.randrange(50, app.width-50), 
                        random.randrange(-app.height//2, app.height-50))
        app.platforms.append((1, Platform(platX, platY)))
        i += 1
    # make sure there is always a reachable platform
    app.platforms.append((1, Platform(random.randrange(50, app.width-50), 
                        random.randrange(-app.height+100, app.height-50))))


# check platform hits, update special platforms
def updatePlatforms(app):
    for i in range (len(app.platforms)):
        if app.doodle.checkHit(app.platforms[i][1]) and not app.powerupToggle:
            pygame.mixer.Sound.play(app.bounce)
            pygame.mixer.music.stop()
            app.doodle.jump = 10
            app.doodle.velocity = 0
            app.score += app.scoreMultiplier*25
            if isinstance(app.platforms[i][1], SpringPlatform):
                app.doodle.jump += app.platforms[i][1].boost
                app.score += app.scoreMultiplier*100
                pygame.mixer.Sound.play(app.spring)
                pygame.mixer.music.stop()
            elif isinstance(app.platforms[i][1], BrokenPlatform):
                app.platforms[i][1].use -= 1
                app.score -= 50
                pygame.mixer.Sound.play(app.brokenPlat)
                pygame.mixer.music.stop()
            break
        if isinstance(app.platforms[i][1], MovePlatform):
            app.platforms[i][1].move()
# get rid of offscreen platforms
def clearPlatforms(app):
    i = 0
    while i < len(app.platforms):
        if ((app.platforms[i][1].posY - app.scrollY > app.height) 
                or (isinstance(app.platforms[i][1], BrokenPlatform) 
                                and app.platforms[i][1].use == 0)):
            app.platforms.pop(i)
        else:
            i += 1
    if len(app.platforms) < app.platformCount:
        generatePlatform(app)