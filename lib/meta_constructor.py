from . import reader_extensions as Ext
from io import BufferedReader
class Mode_Settings():
    def __init__(self,file : BufferedReader,mode : str):
        self.version : int = Ext.ReadByte(file)
        match mode:
            case "standard":
                self.happy_baldi: bool = Ext.ReadByte(file)
            case "endless":
                
                self.items=[]
                for i in range(self.itemcount): #for johnnys shop i would presume
                    self.items.append({"id" : Ext.ReadByte(file),"weight" : Ext.Read32S(file)})
            case "stealthy":
                self.givechalk : bool = Ext.ReadByte(file)

class CustomContentEntry():
    def __init__(self,file : BufferedReader,eversion : int,isfilepath : bool): #lol version is just never used
        self.content_type=Ext.ReadString(file)
        self.content_id=Ext.ReadString(file)
        print("content type"+str(self.content_type))
        print("content id"+str(self.content_id))
        if isfilepath:
            self.data=Ext.ReadString(file)
        else:
            self.length=Ext.Read32S(file)
            self.data=file.read(self.length)
            


class CustomContentPackage():
    def __init__(self,file : BufferedReader):
        print("Initialising and Reading Package")
        self.version : int = Ext.ReadByte(file)
        #dont ask me what this entry version does im assuming it dictates the version of the entries
        self.entryversion : int = Ext.ReadByte(file)
        #check if file paths are allowed
        self.isfilepath : int = Ext.ReadByte(file)
        self.streamcount : int = Ext.Read32S(file)
        print("version"+str(self.version))
        print("entryversion"+str(self.entryversion))
        print("filepaths allowed"+str(self.isfilepath))
        print("streamcount"+str(self.streamcount))
        self.entries=[]
        for i in range(self.streamcount):
            if self.version==0 or not self.isfilepath:
                print("Initialising and Reading Entry")
                entry = CustomContentEntry(file,self.entryversion,self.isfilepath)
                if entry.content_id=="thumbnail":
                    self.thumbEntry = entry
                self.entries.append(entry)



class MetaData():
    def __init__(self,file : bytes):
        self.version : int = Ext.ReadByte(file)
        self.name : str = Ext.ReadString(file)
        self.author : str = Ext.ReadString(file)
        self.mode : str = Ext.ReadString(file)
        print("version"+str(self.version))
        print("name"+self.name)
        print("author"+self.author)
        print("mode"+self.mode)
        if Ext.ReadByte(file):
            self.modeset=Mode_Settings(file,self.mode)
        self.package=CustomContentPackage(file)