from io import BufferedReader
import struct
import math
def ReadByte(file : BufferedReader):
    return file.read(1)[0]

def Read16U(file : BufferedReader):
    return int.from_bytes(file.read(2),byteorder="little",signed=False)

def Read32S(file : BufferedReader):
    return int.from_bytes(file.read(4),byteorder="little",signed=True)

def Read64U(file : BufferedReader):
    return int.from_bytes(file.read(8),byteorder="little",signed=False)

def ReadSingle(file : BufferedReader):
    return struct.unpack('<f', file.read(4))

def ReadColor(file : BufferedReader):
    return (ReadSingle(file),ReadSingle(file),ReadSingle(file),ReadSingle(file))

def ReadVec3(file : BufferedReader):
    return [ReadSingle(file),ReadSingle(file),ReadSingle(file)]

def ReadNybbles(file : BufferedReader):
    count=Read32S(file)
    print("count",count)
    array : list[int] =[]
    rounded=math.ceil(count/2)
    for i in range(rounded):
        nybblepair : int=ReadByte(file)
        nybble1 : int = nybblepair&15
        nybble2 : int = nybblepair>>4
        array.append(nybble1)
        if (i!=rounded-1 or count%2==0):
            array.append(nybble2)
    return array
print(128>>7)
def ReadString(file : BufferedReader):
    string : str =""
    while (True):
        length : int=ReadByte(file)
        partstring : bytes = file.read(length)
        string+=partstring.decode('utf-8')
        if not length>>7:
            return string

class StringCompressor(): #this is such a dumb concept
    def __init__(self,file : BufferedReader):
        self.byteCount : int = file.read(1)[0]
        self.count : int
        match self.byteCount:
            case 1:
                self.count=file.read(1)[0]
            case 2:
                self.count : int = int.from_bytes(file.read(2),byteorder="little",signed=False)
            case _:
                self.count : int = int.from_bytes(file.read(4),byteorder="little",signed=True)
        self.storedStrings : list[str]=[]
        for i in range(self.count):
            addstr=ReadString(file)
            if not addstr in self.storedStrings:
                self.storedStrings.append(addstr)
