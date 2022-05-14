import pylint
import sys
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from src.file_format import FileFormat

class PylintTest:
    def __init__(self):
        self.pylint_output = StringIO()
        self.reporter = TextReporter(self.pylint_output)
        self.formatter = FileFormat()

    def analyze(self, input):
        
        file = self.formatter.string_to_file(input)
        Run([file], reporter=self.reporter, do_exit=False)
        return self.pylint_output.getvalue()
    
    """
    parses output into a dictionary
    @returns Dictionary (key == error code, value == # times it appears)
    """
    def parseOutput(self):

        #grabs the most recent submission and splits the string by line
        inputGetLast = self.pylint_output.getvalue().split("*************")[-1]
        inputSplitline = inputGetLast.split('\n')

        #go through each line and add each error line to a list
        errorLineList = []
        for i in range(len(inputSplitline)):
            if(len(inputSplitline[i])>0):
                if(inputSplitline[i][-1]==')'):
                    errorLineList.append(inputSplitline[i])
        
        #go through each line and parse out the error code
        errorsList = []
        for i in range(len(errorLineList)):
            line = errorLineList[i].split(':')
            errorsList.append(line[3].strip())
        
        #go through our error code list and add it to a dictionary
        #key == error code, value == number of times it appears
        errorsDict = {}
        for i in errorsList:
            if((i in errorsDict) == False):
                errorsDict[i]=1
            else:
                errorsDict[i]+=1
        
        return(errorsDict)

