# main doodle jump file 
from cmu_112_graphics import *
import os
from Doodle import *
from Platform import * 
from Monster import *
from Powerups import *
from Backtracking import *
from Bullet import *
import shelve
import pygame

pygame.init()

# image assets from https://github.com/ahaque/Doodle-Jump/tree/master/images
# sound assets from https://www.sounds-resource.com/mobile/doodlejump/sound/1636/
def appStarted(app):
    app.doodleR = app.loadImage(os.path.dirname(__file__) + '\\doodleR.png')
    app.doodleL = app.loadImage(os.path.dirname(__file__) + '\\doodleL.png')
    app.greenPlat = app.loadImage(os.path.dirname(__file__)+ "\\p-green.png")
    app.springPlat0 = app.loadImage(os.path.dirname(__file__)+ "\\p-green-s0.png")
    app.springPlat1 = app.loadImage(os.path.dirname(__file__)+ "\\p-green-s1.png")
    app.movePlat = app.loadImage(os.path.dirname(__file__)+ "\\p-blue.png")
    app.brokenPlat = app.loadImage(os.path.dirname(__file__)+ "\\p-brown-1.png")
    app.monster = app.loadImage(os.path.dirname(__file__)+ "\\bat1.png")
    app.jetpack = app.loadImage(os.path.dirname(__file__)+ "\\jp.png")
    app.bullet = app.loadImage(os.path.dirname(__file__)+ "\\bullet.png")
    app.openScreen = app.loadImage(os.path.dirname(__file__)+"\\TitlePage.jpg")
    app.playButton = app.scaleImage(app.loadImage(os.path.dirname(__file__)+"\\playButton.png"), 0.5)
    app.leaderboard = app.scaleImage(app.loadImage(os.path.dirname(__file__)+"\\leaderboard.png"), 0.5)
    app.bg = app.scaleImage(app.loadImage(os.path.dirname(__file__)+"\\GameoverPage.jpg"), 2)
    app.gameoverText = app.loadImage(os.path.dirname(__file__)+"\\GameoverText.jpg")
    app.doodle = Doodle(app.width//2, 500) 
    app.platforms = [(1, Platform(app.width//2, app.height-50))]
    app.platformTypes = {1: app.greenPlat, 2: app.movePlat, 
                            3: app.springPlat0, 4: app.brokenPlat}
    #sound effects
    app.bounce = pygame.mixer.Sound("jump.wav")
    app.spring = pygame.mixer.Sound("feder.mp3")
    app.jet = pygame.mixer.Sound("jetpack.mp3")
    app.pickup = pygame.mixer.Sound("collect.mp3")
    app.brokenPlat = pygame.mixer.Sound("egg-crack.mp3")
    app.shoot = pygame.mixer.Sound("bullet.mp3")
    app.monsterHit = pygame.mixer.Sound("hit.mp3")
    
    app.testFeatures = False
    app.lastScreen = 0
    app.timerDelay = 1
    app.scrollY = 0
    app.scrollMargin = 50
    app.timerCounter = 0
    app.platformCount = 20
    app.platSpeed = 1

    app.pathHint = []
    app.showPathHint = False

    app.monsters = []
    app.monsterTimer = 0
    app.monsterInterval = 2000

    app.powerups = []
    app.powerupTimer = 0
    app.powerupInterval = 500
    app.powerupToggle = False
    app.powerupDuration = 300
    app.bullets = 0
    app.firedBullets = []

    app.level = 1
    app.scoreMultiplier = 1
    app.levelInterval = app.level*50000
    app.prob = 10
    app.score = 0

    app.player = None

    app.mainScreen = True
    app.gameOver = True
    app.scoreScreen = False
    app.highscores = shelve.open('score.text')
    # sorry for sketchy formatting here lol
    print("""WELCOME TO JUMP112!!!!!!!
USE RIGHT AND LEFT ARROW KEYS TO MOVE DOODLE
RIGHT CLICK MOUSE TO SHOOT BULLET
YOU CAN USE BACKSPACE OR ONSCREEN 
BUTTONS TO NAVIGATE BETWEEN PAGES
HAVE FUN!!!!!""")

def initLevel(app):
    app.doodle = Doodle(app.width//2, 500) 
    app.platforms = [(1, Platform(app.width//2, app.height-50))]
    app.timerDelay = 1
    app.scrollY = 0
    app.scrollMargin = 50
    app.timerCounter = 0
    app.platformCount = 20
    app.platSpeed = 1

    app.pathHint = []
    app.showPathHint = False

    app.monsters = []
    app.monsterTimer = 0
    app.monsterInterval = 2000

    app.testFeatures = False

    app.powerups = []
    app.powerupTimer = 0
    app.powerupInterval = 500
    app.powerupToggle = False
    app.powerupDuration = 300
    app.bullets = 0
    app.firedBullets = []

    app.level = 1
    app.scoreMultiplier = 1
    app.levelInterval = app.level*50000
    app.prob = 10
    app.score = 0
    app.mainScreen = False
    app.gameOver = False
    app.scoreScreen = False
    initPlatforms(app)

def mousePressed(app, event):
    if not app.gameOver and not app.scoreScreen:
        if app.bullets > 0:
            print("Fired Bullet")
            app.bullets -= 1
            fireBullet(app, app.doodle.posX, app.doodle.posY, event.x, event.y)
    elif app.mainScreen:
        if event.x > 170 and event.x < 450 and event.y > 405 and event.y < 515:
            app.player = app.getUserInput("Enter username: ")
            initLevel(app)
        elif event.x > 310 and event.x < 630 and event.y > 570 and event.y < 680:
            app.mainScreen = False
            app.scoreScreen = True
    elif app.gameOver:
        if event.x > 210 and event.x < 580 and event.y > 30 and event.y < 170:
            app.lastScreen = 1
            app.player = app.getUserInput("Enter username: ")
            initLevel(app)
        elif event.x > 200 and event.x < 600 and event.y > 530 and event.y < 680:
            app.scoreScreen = True

def keyPressed(app, event):
    if not app.gameOver and not app.scoreScreen:
        if (event.key == 'Right'):
            if app.doodle.speedX < 5:
                app.doodle.speedX += 3
            app.doodle.face = 1          
        elif (event.key == 'Left'):
            if app.doodle.speedX > -5:
                app.doodle.speedX -= 3
            app.doodle.face = 0
        # test features
        elif (event.key == 't'):
            app.testFeatures = not app.testFeatures
        elif (event.key == 'Up' and app.testFeatures):
            app.doodle.jump = 10
            app.doodle.velocity = 0
        elif (event.key == '+' and app.testFeatures):
            for i in app.platforms:
                print(getDistance(app.doodle, i[1]))
        elif (event.key == 'p' and app.testFeatures):
            print("Powerup Generated")
            powerUpType = random.randrange(0, 300)
            plat = random.choice(app.platforms)
            # generate jetpack or bullet
            if powerUpType > 250:
                app.powerups += [Powerups(plat[1].posX, plat[1].posY-30, 0)]
            else:
                app.powerups += [Powerups(plat[1].posX, plat[1].posY-30, 1)]
        elif (event.key == 'm' and app.testFeatures):
            print("Monster Generated")
            generateMonster(app)
        elif (event.key == 'd' and app.testFeatures):
            if len(app.monsters) > 0:
                print("Monster Deleted")
                app.monsters.pop()

        # backtracking hints
        elif (event.key == 'h'):
            if not app.showPathHint:
                # try backtracker
                # if error, just return closest platform to player
                try:
                    app.pathHint = getBestPath(app)
                except:
                    print("Error Encountered")
                    tempL = []
                    for i in app.platforms:
                        tempL += [i[1]]
                    app.pathHint = [closeToDoodle(app, tempL)]
                if app.pathHint == None:
                    tempL = []
                    for i in app.platforms:
                        tempL += [i[1]]
                    app.pathHint = [closeToDoodle(app, tempL)]
                app.showPathHint = True
                app.showPathHint = True

            elif app.showPathHint:
                app.showPathHint = False
    # switch between screens 
    if app.scoreScreen:
        if (event.key == 'Backspace'):
            if app.lastScreen == 0:
                app.mainScreen = True
                app.scoreScreen = False
            elif app.lastScreen == 1:
                app.scoreScreen = False
    elif app.gameOver:
        if (event.key == 'Backspace'):
                app.mainScreen = True
                app.scoreScreen = False
                app.lastScreen = 0

# intelligent map generation increases level difficulty
def changeLevel(app):
    print('next level')
    app.platformCount -= 1
    app.monsterInterval -= 10
    app.powerupInterval += 100
    if app.prob < 80:
        app.prob += 1
    if app.level % 5 == 0:
        app.platSpeed += 1
# add score to leaderboard    
def addScore(app):
    if (app.player != None and (app.player not in app.highscores 
        or app.highscores[app.player] < app.score)):
        app.highscores[app.player] = app.score

def timerFired(app):
    if not app.gameOver:
        updatePlatforms(app)
        updateDoodle(app)
        updateMonsters(app)
        updatePowerup(app)
        updateBullet(app)
        clearPlatforms(app)
        # generate monsters
        if app.monsterTimer == app.monsterInterval:
            print('Monster Generated')
            generateMonster(app)
            app.monsterTimer = 0
        clearMonsters(app)
        app.monsterTimer += 1
        app.powerupTimer += 1
        if app.score > app.levelInterval:
            app.level += 1
            app.levelInterval *= app.level
            changeLevel(app)
    if app.gameOver and not app.mainScreen:
        addScore(app)
        
def drawGameOver(app, canvas):
    canvas.create_image(0, 0, image=ImageTk.PhotoImage(app.bg))
    canvas.create_image(app.width/2, app.height/2-100, image=ImageTk.PhotoImage(app.gameoverText))
    canvas.create_text(app.width/2, app.height/2, text=str(app.score),font='Arial 20 bold')
    canvas.create_image(app.width//2, 100, image=ImageTk.PhotoImage(app.playButton))
    canvas.create_image(app.width//2, app.height-200, image=ImageTk.PhotoImage(app.leaderboard))


def drawScoreScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bg))
    canvas.create_image(app.width/2, 100, image=ImageTk.PhotoImage(app.leaderboard))
    temp = app.highscores
    sortedScores = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)}
    posY = 250
    for i in sortedScores:
        canvas.create_text(app.width//2, posY, text=i+": "+ str(sortedScores[i]),font='Arial 20 bold')
        posY += 50
        
def drawMainScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.openScreen))

def redrawAll(app, canvas):
    if not app.gameOver:
        if app.doodle.face == 1:
            canvas.create_image(app.doodle.posX, app.doodle.posY, 
                                image=ImageTk.PhotoImage(app.doodleR))
        else:
            canvas.create_image(app.doodle.posX, app.doodle.posY, 
                                image=ImageTk.PhotoImage(app.doodleL))
        for i in app.powerups:
            if i.powerup == 0:
                canvas.create_image(i.posX, i.posY, 
                                    image=ImageTk.PhotoImage(app.jetpack))  
            else:
                canvas.create_image(i.posX, i.posY, 
                                    image=ImageTk.PhotoImage(app.bullet)) 
        for i in app.platforms:
            canvas.create_image(i[1].posX, i[1].posY, 
                                image=ImageTk.PhotoImage(app.platformTypes[i[0]]))
        for i in app.monsters:
            canvas.create_image(i.posX, i.posY, 
                                image=ImageTk.PhotoImage(app.monster))
        for i in app.firedBullets:
            canvas.create_image(i.posX, i.posY, 
                                image=ImageTk.PhotoImage(app.bullet))
        if app.showPathHint:
            for i in app.pathHint:
                canvas.create_text(i.posX, i.posY, text="Jump Here", font='Arial 10 bold')
        if app.testFeatures:
            canvas.create_text(app.width/2, 50 , text="Test Features on", font='Arial 10 bold')

        canvas.create_text(app.width-100, 100, text=str(app.score),font='Arial 20 bold')
        canvas.create_text(100, 100, text="Bullets: "+str(app.bullets), font='Arial 20 bold')

    elif app.mainScreen:
        drawMainScreen(app, canvas)
    elif app.scoreScreen:
        drawScoreScreen(app, canvas)
    elif app.gameOver: 
        drawGameOver(app, canvas)

def appStopped(app):
    print("Game Closed")
    app.highscores.close()

runApp(width=800, height=800)