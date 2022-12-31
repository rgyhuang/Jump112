from cmu_112_graphics import *
import random
import math
from PIL import ImageColor
from audioData import *
from slider import*
from colorConvert import*
class Circle(object):
    
    def __init__(self, posX, posY, radius, color):
        self.x = posX
        self.y = posY
        self.r = radius
        self.color = color

    def moveCircle(self, dx, dy):
        self.x += dx
        self.y += dy

    def changeColor(self, tintOrShade):
        if tintOrShade == 0:
            newColor = list(fromHex(self.color)) 
            newColor[0] = int(newColor[0]+(255-newColor[0]) * (1/2))
            newColor[1] = int(newColor[1]+(255-newColor[1]) * (1/2))
            newColor[2] = int(newColor[2]+(255-newColor[2]) * (1/2))
            newColor = fromrgb(tuple(newColor))

        else:
            newColor = list(fromHex(self.color)) 
            newColor[0] = int(newColor[0]*0.5)
            newColor[1] = int(newColor[1]*0.5)
            newColor[2] = int(newColor[2]*0.5)
            newColor = fromrgb(tuple(newColor))



class CircleFractal(object):

    def __init__(self, levels, x, y, r, color):
        self.levels = levels
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.pattern = []
        self.makeFractal(levels, self.x, self.y, self.r, self.color)


    def makeFractal(self, levels, x, y, r, color):
        if levels == 0:
            self.pattern += [Circle(x, y, r, color)]
        else:
            newColor = list(fromHex(color)) 
            newColor[0] = int(newColor[0]+(255-newColor[0]) * (1/2))
            newColor[1] = int(newColor[1]+(255-newColor[1]) * (1/2))
            newColor[2] = int(newColor[2]+(255-newColor[2]) * (1/2))
            newColor = fromrgb(tuple(newColor))
            for i in range(5):
                angle = (i+1)*72* (math.pi/180)
                dx, dy = (math.cos(angle)*1.5*r), (math.sin(angle)*r*1.5)
                self.makeFractal(levels-1, x+dx, y+dy, r/2, newColor)

            self.pattern += [Circle(x, y, r, newColor)]


def appStarted(app):
    app.patterns = []
    app.color = '#FF8000'
    app.audioStream = AudioStream()


def moveFract(app, dx, dy):
    for elem in app.patterns:
        for circle in elem.pattern:
            circle.moveCircle(dx, dy)

def keyPressed(app, event):
    if event.key == 'Enter':
        newX, newY = random.randrange(0, app.width), random.randrange(0, app.height)
        levels = random.randrange(1,5)
        app.patterns+=[CircleFractal(levels, newX, newY, 100, app.color)]
    elif (event.key == 'Backspace' and len(app.patterns) > 0):
        app.patterns.pop()
    elif (event.key == 'Right'):
        moveFract(app, 5, 0)
    elif (event.key == 'Left'):
        moveFract(app, -5, 0)
    elif (event.key == 'Up'):
        moveFract(app, 0, -5)
    elif (event.key == 'Down'):
        moveFract(app, 0, 5)
        
        

def drawButton(app, canvas):
    Slider(canvas, 0, 100,'horizontal')



def timerFired(app):
    app.data = app.audioStream.getData()
    print(app.data)


def redrawAll(app, canvas):
    #drawButton(app,canvas)
    for elem in app.patterns:
        for circle in elem.pattern:
            canvas.create_oval(circle.x-circle.r, circle.y-circle.r, circle.x+circle.r, circle.y+circle.r, fill=circle.color)

runApp(width=800, height=800)