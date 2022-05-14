import astroid
from astroid import nodes
from typing import TYPE_CHECKING, Optional

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


"""
Checks if a set method returns something
Put this file in <python directory>\Lib\site-packages\pylint\checkers
"""

def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(setReturns(linter))

class setReturns(BaseChecker):
    __implements__ = IAstroidChecker

    name = "set-returns"
    msgs = {
        "C1414": (
            "Set method returns something.",
            "set-returns",
            "A set method should not return anything.",
        ),
    }
    options = (
        (
            "set-returns",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Allow set methods to return things",
            },
        ),
    )
    def __init__(self, linter: Optional["PyLinter"] = None) -> None:
        super().__init__(linter)
        self._function_stack = []
        self.funcNames = []

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._function_stack.append([])
        self.funcNames.append(node.name)

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        self._function_stack.pop()
        self.funcNames.pop()
    
    def visit_return(self, node: nodes.Return) -> None:
        if(node.value!=None and self.funcNames[-1][:3]=="set"):
            self.add_message("set-returns",node = node)

        self._function_stack[-1].append(node)
    
