from . import reader_extensions as Ext

class MetaData():
    def __init__(self,file : bytes):
        version : int = file.read(1)[0]
        name : str = Ext.ReadString(file)
        author : str = Ext.ReadString(file)
        gamemode : str = Ext.ReadString(file)
        print(version,name,author,gamemode)