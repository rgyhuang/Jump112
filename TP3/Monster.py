# Contains Monster class and related functions
import random
class Monster(object):
    def __init__(self, posX, posY, speedX):
        self.cx = posX
        self.cy = posY
        self.posX = posX
        self.posY = posY
        self.width = 90
        self.height = 70
        self.dirX = speedX

    def move(self):
        if abs(self.posX-self.cx) > 60:
            self.dirX *= -1
        self.posX += self.dirX


def generateMonster(app):
    x, y =  (random.randrange(50, app.width-50), 
                    random.randrange(-app.height, -200))   
    app.monsters.append(Monster(x, y, 0.5))


def updateMonsters(app):
    for i in app.monsters:
        if app.doodle.checkHit(i) and not app.powerupToggle:
            print('Game Over')
            app.gameOver = True
        i.move()

def clearMonsters(app):
    i = 0
    while i < len(app.monsters):
        if (app.monsters[i].posY - app.scrollY > app.height):
            app.monsters.pop(i)
        else:
            i += 1