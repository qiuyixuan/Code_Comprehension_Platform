import pylint
import sys
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter

class PylintTest:
    def __init__():
        pylint_output = StringIO()
        reporter = TextReporter(pylint_output)
        Run(["connect-4_before"], reporter=reporter, do_exit=False)
        print(pylint_output.getvalue())
