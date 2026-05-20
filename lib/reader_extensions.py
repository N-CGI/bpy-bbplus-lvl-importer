def ReadString(file):
    string : str =""
    while (True):
        length : int=file.read(1)[0]
        partstring : bytes = file.read(length)
        string+=partstring.decode('utf-8')
        if not length>>8:
            return string