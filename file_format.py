import io
from datetime import datetime

class FileFormat:
    def __init__(self):
        pass

    def string_to_file(self, str):
        #put string in file
        #gen random filename
        filename = datetime.now().strftime("%H%M%S") + ".py"
        textfile = open(filename, "w")
        textfile.write(str)
        return filename
