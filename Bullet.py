# Contains Bullet Class and related functions
import math
import pygame
class Bullet(object):
    def __init__(self, x, y, dx, dy):
        self.width = 5
        self.height = 5
        self.posX = x
        self.posY = y
        self.dx = dx
        self.dy = dy
    def move(self):
        self.posX += self.dx
        self.posY += self.dy 

    def checkHit(self, other):
        if (self.posX + self.width >= other.posX - 15
            and self.posX <= other.posX + other.width
            and self.posY+self.height>=other.posY
            and self.posY+self.height<=other.posY+other.height):
            return True
        return False

    
def fireBullet(app, doodleX, doodleY, clickX, clickY):
    r = math.sqrt((doodleX - clickX)**2 + (doodleY - clickY)**2)
    numMoves = r//10
    vx = (clickX-doodleX)//10
    vy = (clickY-doodleY)//10
    # adapted from ahaque's java doodle jump
    # https://github.com/ahaque/Doodle-Jump
    # set min bullet speed
    if vx > -6 and vx < 0:
        vx = -6
    if vx < 6 and vx > 0:
        vx = 6
    if vy > -6 and vy < 0:
        vy = -6
    if vy < 6 and vy > 0:
        vy = 6

    while (abs(vx) > 10):
        if (vy != 0):
            vy = vy / 2
        
        if (vx != 0): 
            vx = vx / 2


    while (abs(vy) > 10):
        if (vy != 0):
            vy = vy / 2;

        if (vx != 0):
            vx = vx / 2;
    app.firedBullets += [Bullet(doodleX, doodleY, vx, vy)]
    pygame.mixer.Sound.play(app.shoot)
    pygame.mixer.music.stop()
    
def updateBullet(app):
    i = 0
    while i < len(app.firedBullets):
        j = 0
        currLen = len(app.firedBullets)
        while j < len(app.monsters):
            if app.firedBullets[i].checkHit(app.monsters[j]):
                print('Enemy Hit!')
                app.score += 50000
                app.monsters.pop(j)
                app.firedBullets.pop(i)
                pygame.mixer.Sound.play(app.monsterHit)
                pygame.mixer.music.stop()
                break
            elif(app.firedBullets[i].posX < 0 
                or app.firedBullets[i].posX > app.width 
                or app.firedBullets[i].posY < -100 
                or app.firedBullets[i].posY > app.height):
                app.firedBullets.pop(i)
                break
            else:
                j += 1
        if currLen == len(app.firedBullets):
            app.firedBullets[i].move()
            i += 1