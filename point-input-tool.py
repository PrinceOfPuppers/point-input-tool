import pygame as pg
from config import config

#note, this application is ment for pygame, hence all if coordinates are
#inputted into any typical graphing softwear images will be flipped vertically

#controls:
#mouse 1 to place points, placing 2 points will make a line and add it to current line set
#mouse 2 to remove first point
#backspace to delete current line set
#enter to submit current lines and move on to next line set

gameDisplay = pg.display.set_mode((config.screenSize[0], config.screenSize[1]))

#pixles to grid
def convertCoords(coord):
    newCoordX=(coord[0]-config.origin[0])/config.gridSpaceing
    newCoordY=(coord[1]-config.origin[1])/config.gridSpaceing
    return([round(newCoordX),round(newCoordY)])

#grid to pixel
def inverseConvertCoords(coord):
    newCoordX=(coord[0])*config.gridSpaceing+config.origin[0]
    newCoordY=(coord[1])*config.gridSpaceing+config.origin[1]
    return([round(newCoordX),round(newCoordY)])

def drawGrid(gameDisplay):
    #vertical Lines

    #yAxis
    point1=(config.origin[0],0)
    point2=(config.origin[0],config.screenSize[1])
    pg.draw.aaline(gameDisplay,(0,0,255),point1,point2)
    
    #yGridLines
    #positive
    loopNumber=int(round((screenSize[0]-config.origin[0])/config.gridSpaceing))
    for lineValue in range(1,loopNumber+1):
        lineX=config.origin[0]+config.gridSpaceing*lineValue

        point1=(lineX,0)
        point2=(lineX,config.screenSize[1])
        pg.draw.aaline(gameDisplay,(255,0,0),point1,point2)

    #negative
    loopNumber=int(round(config.origin[0]/config.gridSpaceing))
    for lineValue in range(1,loopNumber+1):
        lineX=config.origin[0]-config.gridSpaceing*lineValue

        point1=(lineX,0)
        point2=(lineX,config.screenSize[1])
        pg.draw.aaline(gameDisplay,(255,0,0),point1,point2)

    #xAxis
    point1=(0,config.origin[1])
    point2=(config.screenSize[0],config.origin[1])
    pg.draw.aaline(gameDisplay,(0,0,255),point1,point2)
    
    #xGridLines
    #positive
    loopNumber=int(round((screenSize[1]-config.origin[1])/config.gridSpaceing))
    for lineValue in range(1,loopNumber+1):
        lineY=config.origin[1]+config.gridSpaceing*lineValue

        point1=(0,lineY)
        point2=(config.screenSize[0],lineY)
        pg.draw.aaline(gameDisplay,(255,0,0),point1,point2)
    
    #negative
    loopNumber=int(round(config.origin[1]/config.gridSpaceing))
    for lineValue in range(1,loopNumber+1):
        lineY=config.origin[1]-config.gridSpaceing*lineValue

        point1=(0,lineY)
        point2=(config.screenSize[0],lineY)
        pg.draw.aaline(gameDisplay,(255,0,0),point1,point2)

def convertToFontDict(listOfLineSets):
    fontDict={}
    if len(listOfLineSets)>len(config.alphabet):
        print('too many line sets for font conversion')
        print('you inputted',len(listOfLineSets))
        print('your require',len(config.alphabet))
    elif len(listOfLineSets)<len(config.alphabet):
        print('too few line sets for font conversion')
        print('you inputted',len(listOfLineSets))
        print('your require',len(config.alphabet))
    else:
        for i in range(0,len(config.alphabet)):
            lineSet=listOfLineSets[i]
            letter=config.alphabet[i]
            fontDict[letter]=lineSet
        return(fontDict)
#makes each set of lines into a single list of tups
#leaving you with a list of all the sets
#useful for inputting into graphing softwear
#does not mutate input
def convertLineListsToTups(listOfLineSets):
    tupSets=[]
    for lineSet in listOfLineSets:
        tupSet=[]
        for line in lineSet:
            point1=(line[0][0],line[0][1])
            point2=(line[1][0],line[1][1])
            tupSet.append(point1)
            tupSet.append(point2)
        tupSets.append(tupSet)
    return(tupSets)

def convertPointListsToTups(listOfPointLists):
    tupSets=[]
    for pointList in listOfPointLists:
        tupSet=[]
        for point in pointList:
            tupSet.append((point[0],point[1]))
        tupSets.append(tupSet)
    return(tupSets)

class Application:
    def __init__(self):
        self.hasQuit=False

class LineListApplication(Application):
    def __init__(self):
        super().__init__()
        
        self.graphGuides=config.lineListGraphGuides
        #all lines are unconverted and will be converted when applicaiton is closed
        #submitting lines with submit them in a set
        self.submittedLines=[]
        self.numberOfSubmittedLines=len(self.submittedLines)
        self.unsubmittedLines=[]
        self.point1=[]
        self.point2=[]
        self.currentPointNumber=1

    def getAndApplyControls(self,gameDisplay):
        for event in pg.event.get():
            # checks if player has quit
            if event.type == pg.QUIT:
                self.hasQuit=True

            #mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                mousePos=event.pos
                button=event.button
                #left click
                if button==1:
                    if self.currentPointNumber==1:
                        self.point1=convertCoords(mousePos)
                        self.currentPointNumber=2
                    else:
                        self.point2=convertCoords(mousePos)
                        self.currentPointNumber=1
                        self.unsubmittedLines.append([self.point1,self.point2])
                
                #right click
                elif button==3:
                    if self.currentPointNumber==2:
                        self.point1=[]
                        self.point2=[]
                        self.currentPointNumber=1

            #keyboard controls
            if event.type==pg.KEYDOWN:
                #backspace
                if event.key==pg.K_BACKSPACE:
                    self.unsubmittedLines=[]
                    self.point1=[]
                    self.point2=[]
                    self.currentPointNumber=1

                #enter
                if event.key==pg.K_RETURN:
                    self.numberOfSubmittedLines+=1
                    self.submittedLines.append(self.unsubmittedLines)
                    self.unsubmittedLines=[]
                    self.point1=[]
                    self.point2=[]
                    self.currentPointNumber=1
                    if config.convertToFontDict:
                        if self.numberOfSubmittedLines==len(config.alphabet):
                            appInstance.hasQuit=True
                        else:
                            print('Current Letter:',config.alphabet[self.numberOfSubmittedLines])
        
        mousePos=[pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]]
        if self.currentPointNumber==2:
            point1=inverseConvertCoords(self.point1)
            pg.draw.aaline(gameDisplay,(255,255,255),point1,mousePos)
    
    def renderUnsubmittedLines(self,gameDisplay):
        for line in self.unsubmittedLines:
            displayLine=(inverseConvertCoords(line[0]),inverseConvertCoords(line[1]))
            pg.draw.aaline(gameDisplay,(255,255,255),displayLine[0],displayLine[1])

    def renderGraphGuides(self,gameDisplay):
        for lineSet in self.graphGuides:
            for line in lineSet:
                displayLine=(inverseConvertCoords(line[0]),inverseConvertCoords(line[1]))
                
                pg.draw.aaline(gameDisplay,(0,255,0),displayLine[0],displayLine[1])
        
        if config.displayPrevious:
            for lineSet in self.submittedLines:
                for line in lineSet:
                    displayLine=(inverseConvertCoords(line[0]),inverseConvertCoords(line[1]))
                    
                    pg.draw.aaline(gameDisplay,(0,255,0),displayLine[0],displayLine[1])
    
    def printResults(self):
        print(self.submittedLines)
        if config.convertToTups:
            print(convertLineListsToTups(self.submittedLines))
        if config.convertToFontDict:
            print(convertToFontDict(self.submittedLines))    
class PointListApplication(Application):
    
    
    def __init__(self):
        super().__init__()
        self.graphGuides=config.pointListGraphGuides
        #all lines are unconverted and will be converted when applicaiton is closed
        #submitting lines with submit them in a set
        self.submittedPointLists=[]
        self.numberOfSubmittedPointLists=len(self.submittedPointLists)
        self.unsubmittedPointList=[]
        
        self.currentPointNumber=0
    
    def getAndApplyControls(self,gameDisplay):
        for event in pg.event.get():
            # checks if player has quit
            if event.type == pg.QUIT:
                self.hasQuit=True

            #mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                mousePos=event.pos
                button=event.button
                #left click
                if button==1:
                    point=convertCoords(mousePos)
                    self.unsubmittedPointList.append(point)
                    self.currentPointNumber+=1

                
                #right click
                elif button==3:
                    if self.currentPointNumber!=0:
                        del self.unsubmittedPointList[-1]
                        self.currentPointNumber-=1

            #keyboard controls
            if event.type==pg.KEYDOWN:
                #backspace
                if event.key==pg.K_BACKSPACE:
                    self.unsubmittedPointList=[]
                    self.currentPointNumber=0

                #enter
                if event.key==pg.K_RETURN:
                    self.numberOfSubmittedPointLists+=1
                    self.submittedPointLists.append(self.unsubmittedPointList)
                    self.unsubmittedPointList=[]
                    self.currentPointNumber=0
        
        mousePos=[pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]]
        if self.currentPointNumber!=0:
            point1=inverseConvertCoords(self.unsubmittedPointList[self.currentPointNumber-1])
            pg.draw.aaline(gameDisplay,(255,255,255),point1,mousePos)

    def renderUnsubmittedLines(self,gameDisplay):
        if self.currentPointNumber>=2:
            for i in range(0,len(self.unsubmittedPointList)-1):
                point1=self.unsubmittedPointList[i]
                point2=self.unsubmittedPointList[i+1]
                displayLine=(inverseConvertCoords(point1),inverseConvertCoords(point2))
                pg.draw.aaline(gameDisplay,(255,255,255),displayLine[0],displayLine[1])

    def renderGraphGuides(self,gameDisplay):
        for pointList in self.graphGuides:
            transformedPointList=[]
            for point in pointList:
                transformedPointList.append(inverseConvertCoords(point))
            pg.draw.aalines(gameDisplay,(0,255,0),True,transformedPointList)

        if config.displayPrevious:
            for pointList in self.submittedPointLists:
                transformedPointList=[]
                for point in pointList:
                    transformedPointList.append(inverseConvertCoords(point))
                pg.draw.aalines(gameDisplay,(0,255,0),True,transformedPointList)

    def printResults(self):
        print(self.submittedPointLists)
        if config.convertToTups:
            print(convertPointListsToTups(self.submittedPointLists))

if config.convertToFontDict:
    print('Current Letter: A')
frameRate=config.frameRate
screenSize=config.screenSize
gameDisplay = pg.display.set_mode((config.screenSize[0], config.screenSize[1]))
pg.init()
pg.display.set_caption("")
clock = pg.time.Clock()
if config.mode==0:
    appInstance=LineListApplication()
elif config.mode==1:
    appInstance=PointListApplication()
    if config.convertToFontDict:
        print("cannot make font dict with point list")
else:
    print("mode Error")

while not appInstance.hasQuit:
    pg.Surface.fill(gameDisplay,(0,0,0))
    drawGrid(gameDisplay)
    appInstance.renderGraphGuides(gameDisplay)
    appInstance.renderUnsubmittedLines(gameDisplay)
    appInstance.getAndApplyControls(gameDisplay)
    clock.tick_busy_loop(frameRate)
    pg.display.update()

appInstance.printResults()
