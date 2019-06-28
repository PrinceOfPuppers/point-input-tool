class Config:
    def __init__(self):
        #all in pixel counts
        self.screenSize=[1500,800]
        self.origin=[750,400]

        #0 for line list, 1 for point list
        self.mode=0

        #functions as a scaling factor so you can more accuratly place points
        #point lists will be outputted as if each grid intersection was one pixel
        self.gridSpaceing=50
        self.frameRate=60
        self.convertToTups=True

        #treates submitted line like graph guide
        self.displayPrevious=False

        #creates a dict containing each letter of the alphabet
        self.convertToFontDict=False
        self.alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','1','2']

        #displays guiding lines for graphing
        self.lineListGraphGuides=[]
        self.pointListGraphGuides=[]
config=Config()