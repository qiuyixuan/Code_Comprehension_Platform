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
