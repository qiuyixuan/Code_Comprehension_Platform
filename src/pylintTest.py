import pylint
import sys
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter

class PylintTest:
    def __init__(self):
        self.pylint_output = StringIO()
        self.reporter = TextReporter(self.pylint_output)

    def analyze(self, input):
        Run(["connect-4_before"], reporter=self.reporter, do_exit=False)
        return self.pylint_output.getvalue()
