from . import meta_constructor as Meta
from . import level_constructor as Level
from . import reader_extensions as Ext
from io import BufferedReader
class LevelStudioMap():
    def __init__(self,file : BufferedReader):
        self.version : int = Ext.ReadByte(file)
        self.seed: int = Ext.Read64U(file)
        print(self.version,self.seed)
        self.metadata=Meta.MetaData(file)
        self.level=Level.Level(file)

