from . import reader_extensions as Ext
from io import BufferedReader
class Cell():
    def __init__(self):
        self.walls : int = 0
class Level():
    def generate_cells(self,w,h):
        self.cells : list[Cell]=[Cell() for _ in range(w*h)]

    def __init__(self,file : BufferedReader):
        self.version : int = Ext.ReadByte(file)
        self.roomcompress = Ext.StringCompressor(file) # i will change this comment when i figure out what this does
        self.objectcompress = Ext.StringCompressor(file) # i will change this comment when i figure out what this does
        self.title : str = Ext.ReadString(file) #elevator title
        self.timeLimit : float = Ext.ReadSingle(file) #time limit

        if self.version>=3:
            self.seed : int = Ext.Read32S(file)
        
        if self.version>=5:
            self.usesMap : bool = Ext.ReadByte(file)
        
        self.skybox : str = Ext.ReadString(file)
        self.minlight : tuple[float,float,float,float] = Ext.ReadColor(file)
        self.lightmode : int = Ext.ReadByte(file)
        self.initialREG : float = Ext.ReadSingle(file) # Initial Random Event Gap (REG)
        self.minREG : float = Ext.ReadSingle(file)
        self.maxREG : float = Ext.ReadSingle(file)
        eventcount : int = Ext.Read32S(file)
        self.events = []
        for i in range(eventcount):
            event=Ext.ReadString(file)
            print(event)
            self.events.append(event)
        self.spawnpoint = Ext.ReadVec3(file)
        self.spawndir : int = Ext.ReadByte(file)

        #Those settings were SO ANNOYING TO CODE OMG
        # IT WAS ALL JUST BACK AND FORTH AND BACK AND FORTH
        # I JUST WANT TO BE ABLE TO SEE WALLS RIGHT ABOUT NOW

        self.width=Ext.ReadByte(file)
        self.height=Ext.ReadByte(file)
        print("width and height ",self.width,self.height)
        self.generate_cells(self.width,self.height)
        wallnybbles=Ext.ReadNybbles(file)
        print(wallnybbles)
        for i in range(len(self.cells)):
            self.cells[i].walls=wallnybbles[i]





