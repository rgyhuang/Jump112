# Contains backtracking algorithm for user movement suggestion
import math
def getDistance(a, b):
    ax, ay = a.posX, a.posY
    bx, by = b.posX, b.posY
    return math.sqrt((ax-bx)**2 + (ay-by)**2)
# wrapper function, sorts platforms based on height 
def getBestPath(app):
    tempL = []
    for i in app.platforms:
        tempL += [i[1]]
    tempL.sort(key=lambda x: x.posY)
    start = closeToDoodle(app, tempL)
    path = [start]
    return backtrack(app, tempL, path)
# return closests platform to doodle player
def closeToDoodle(app, L):
    bestPlat, bestDist = None, -1
    for i in L:
        tempDist = getDistance(app.doodle, i)
        if bestPlat == None or tempDist < bestDist:
            bestPlat = i
            bestDist = tempDist
    L.remove(bestPlat)
    return bestPlat
# checks if distances are legal between platform
# makes sure doodle can actually jump to platforms
def isLegalPath(path):
    for i in range(len(path)-1):
        if abs(path[i].posY- path[i+1].posY) > 330:
            return False
    return True
# check if there are monsters close to the platform
# avoid going to platforms close to monsters
def legalAroundMonsters(app, platform):
    if len(app.monsters) == 0: return True
    
    for i in app.monsters:
        if getDistance(i, platform) < 100:
            print("Monster nearby!")
            return False
    return True

# helper recursive backtracker, 
# finds path until path reaches top of screen 
def backtrack(app, L, path):
    if path[-1].posY <= 200 and len(path) > 1:
        return path
    else:
        for i in range(len(L)):
            currPlat = L[i]
            path += [currPlat]
            tempL = L[:i] + L[i+1:]
            
            # try path
            if isLegalPath(path) and legalAroundMonsters(app,currPlat):
                tempPath = backtrack(app, tempL, path)
                if tempPath != None:
                    return tempPath
            # backtrack if path doesn't work
            path.pop()