# Contains powerup related class and functions
from Bullet import *
import pygame
class Powerups(object):
    def __init__(self, x, y, powerup):
        self.posX = x
        self.posY = y
        self.width = 30
        self.height = 30
        self.powerup = powerup
        
def updatePowerup(app):
    i = 0
    while i < len(app.powerups):
        if app.doodle.checkHit(app.powerups[i]):
            print('Picked up powerup!')
            if app.powerups[i].powerup == 0:
                app.powerupToggle = True
                pygame.mixer.Sound.play(app.jet)
                pygame.mixer.music.stop()
            else:
                pygame.mixer.Sound.play(app.pickup)
                pygame.mixer.music.stop()
                app.bullets += 1
            app.powerups.pop(i)
        elif ((app.powerups[i].posY - app.scrollY > app.height)):
            app.powerups.pop(i)
        else:
            i += 1