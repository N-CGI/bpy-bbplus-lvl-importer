from . import reader_extensions as Ext
import imbuf
import bpy
import os

class Mode_Settings():
    def __init__(self,file):
        self.version : int = file.read(1)[0]
        self.happy_baldi: bool = file.read(1)[0]

class CustomContentEntry():
    def __init__(self,file,eversion,isfilepath):
        self.content_type=Ext.ReadString(file)
        self.content_id=Ext.ReadString(file)
        print("content type"+str(self.content_type))
        print("content id"+str(self.content_id))
        if isfilepath:
            self.data=Ext.ReadString(file)
        else:
            self.length=int.from_bytes(file.read(4),byteorder="little",signed=True) #dont ask why its signed, idk
            self.data=file.read(self.length)
            


class CustomContentPackage():
    def __init__(self,file):
        print("Initialising and Reading Package")
        self.version : int = file.read(1)[0]
        #dont ask me what this entry version does im assuming it dictates the version of the entries
        self.entryversion : int = file.read(1)[0]
        #check if file paths are allowed
        self.isfilepath : int = file.read(1)[0]
        self.streamcount : int = int.from_bytes(file.read(4),byteorder="little",signed=True) #dont ask why its signed, idk
        print("version"+str(self.version))
        print("entryversion"+str(self.entryversion))
        print("filepaths allowed"+str(self.isfilepath))
        print("streamcount"+str(self.streamcount))
        self.entries=[]
        for i in range(self.streamcount):
            if self.version==0 or not self.isfilepath:
                print("Initialising and Reading Entry")
                self.entries.append(CustomContentEntry(file,self.entryversion,self.isfilepath))



class MetaData():
    def __init__(self,file : bytes):
        self.version : int = file.read(1)[0]
        self.name : str = Ext.ReadString(file)
        self.author : str = Ext.ReadString(file)
        self.mode : str = Ext.ReadString(file)
        print("version"+str(self.version))
        print("name"+self.name)
        print("author"+self.author)
        print("mode"+self.mode)
        if file.read(1)[0]:
            self.modeset=Mode_Settings(file)
        self.package=CustomContentPackage(file)