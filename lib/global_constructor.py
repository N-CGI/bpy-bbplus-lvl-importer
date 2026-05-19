from . import meta_constructor as Meta

class LevelStudioMap():
    def __init__(self,file : bytes):
        self.version : int = file.read(1)[0]
        self.seed: int = int.from_bytes(file.read(8),byteorder="little")
        print(self.version,self.seed)
        self.metadata=Meta.MetaData(file)

