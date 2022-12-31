# Contains classes and methods related to character (the Doodle)
from Platform import *
class Doodle(object):
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.face = 1
        self.jump = 0
        self.velocity = 0
        self.speedX = 0
        self.width = 20
        self.height = 25
        #self.color = color

    def fall(self):
        accel = 0.05
        if self.velocity < 20:
            self.velocity += accel
        self.posY += self.velocity

    def move(self):
        self.posX += self.speedX
        if self.speedX > -1e-1 and self.speedX < 1e-1:
            self.speedX = 0
        elif self.speedX > 0:
            self.speedX -= 0.05
        elif self.speedX < 0:
            self.speedX += 0.05

    def useJetPack(self):
        self.posY -= 20
        
    # only check if falling
    def checkHit(self, other):
        if (self.velocity > 4 and self.posX + self.width >= other.posX - 25
            and self.posX <= other.posX + other.width
            and self.posY+self.height>=other.posY
            and self.posY+self.height<=other.posY+other.height):
            return True
        return False
# based on course notes
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def makePlayerVisible(app):
    # scroll to make player visible as needed
    if (app.doodle.posY < app.scrollY + app.scrollMargin):
        app.scrollY = app.doodle.posY - app.scrollMargin
        app.doodle.posY -= app.scrollY
        for i in app.platforms:
            if isinstance(i[1], MovePlatform):
                i[1].cy -= app.scrollY

            i[1].posY -= app.scrollY
        for i in app.monsters:
            i.posY -= app.scrollY
        for i in app.powerups:
            i.posY -= app.scrollY
        app.scrollY = 0
        # app.level += 1

    # don't scroll down, because game over
    if (app.doodle.posY > app.scrollY + app.width):
        print('Game over')
        app.gameOver = True
    if (app.doodle.posX < 0):
        app.doodle.posX = app.width
    elif (app.doodle.posX > app.width):
        app.doodle.posX = 0

# update position of doodle
def updateDoodle(app):
    if app.powerupToggle:
        if app.powerupDuration > 0:
            app.doodle.useJetPack()
            app.powerupDuration -= 1
            app.score += 10
        elif app.powerupDuration <= 0:
            app.powerupDuration = 300
            app.powerupToggle = False
            app.doodle.jump = 20
            app.doodle.velocity = 0
    if app.doodle.jump > 0:
        app.doodle.posY -= app.doodle.jump
        app.doodle.jump -= 0.1
    if app.doodle.posY < app.height:
        if not app.powerupToggle:
            app.doodle.fall()
        makePlayerVisible(app)
    
    app.doodle.move()

    if app.doodle.speedX == 0:
        app.doodle.dir = 0